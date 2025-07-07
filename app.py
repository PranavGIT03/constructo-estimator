from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///constructo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    estimations_left = db.Column(db.Integer, default=3)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    price = db.Column(db.Float)

class Estimation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    total_cost = db.Column(db.Float)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            email=email,
            password=generate_password_hash(password),
            estimations_left=3
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User created successfully'}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/materials')
def get_materials():
    materials = Material.query.all()
    return jsonify([{
        'id': m.id,
        'category': m.category,
        'name': m.name,
        'unit': m.unit,
        'price': m.price
    } for m in materials])

@app.route('/api/estimate', methods=['POST'])
@login_required
def create_estimate():
    if current_user.estimations_left <= 0:
        return jsonify({'error': 'No estimations left'}), 403
    
    data = request.get_json()
    materials = data.get('materials', [])
    
    total_cost = 0
    details = []
    
    for item in materials:
        material = Material.query.get(item['material_id'])
        if material:
            quantity = item['quantity']
            cost = material.price * quantity
            total_cost += cost
            details.append({
                'material': material.name,
                'quantity': quantity,
                'unit_price': material.price,
                'total': cost
            })
    
    estimation = Estimation(
        user_id=current_user.id,
        total_cost=total_cost,
        details=details
    )
    
    current_user.estimations_left -= 1
    db.session.add(estimation)
    db.session.commit()
    
    return jsonify({
        'id': estimation.id,
        'total_cost': total_cost,
        'details': details,
        'estimations_left': current_user.estimations_left
    })

@app.route('/api/my-estimates')
@login_required
def get_my_estimates():
    estimates = Estimation.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': e.id,
        'total_cost': e.total_cost,
        'details': e.details,
        'created_at': e.created_at.isoformat()
    } for e in estimates])

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    print(f"Admin access attempt by: {current_user.email}")
    if current_user.email != 'admin@example.com':
        print("Access denied - not admin")
        return redirect(url_for('index'))
    print("Admin access granted")
    return render_template('admin_excel.html')

@app.route('/admin-test')
@login_required
def admin_test():
    if current_user.email != 'admin@example.com':
        return "Access denied"
    return render_template('admin_test.html')

@app.route('/api/admin/excel-data')
@login_required
def get_excel_data():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    excel_file = 'Constructo.xlsx'
    print(f"Looking for Excel file: {os.path.abspath(excel_file)}")
    
    if not os.path.exists(excel_file):
        print("Excel file not found, creating sample data")
        # Create sample data if file doesn't exist
        sample_data = {
            'ID': [1, 2, 3],
            'Category': ['RCC', 'Electrical', 'Plumbing'],
            'Material': ['Cement', 'Wire', 'Pipe'],
            'Unit': ['bag', 'meter', 'meter'],
            'Price': [350, 12, 45]
        }
        df = pd.DataFrame(sample_data)
        df.to_excel(excel_file, index=False)
    
    try:
        df = pd.read_excel(excel_file)
        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return jsonify({
            'columns': df.columns.tolist(),
            'data': df.to_dict('records')
        })
    except Exception as e:
        print(f"Error reading Excel: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/excel-update', methods=['POST'])
@login_required
def update_excel_data():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    excel_file = 'Constructo.xlsx'
    
    try:
        df = pd.DataFrame(data['data'])
        df.to_excel(excel_file, index=False)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create sample materials if none exist
        if not Material.query.first():
            materials = [
                Material(category='RCC', name='Cement', unit='bag', price=350),
                Material(category='RCC', name='Steel Rebar', unit='kg', price=65),
                Material(category='RCC', name='Sand', unit='cubic_ft', price=45),
                Material(category='Electrical', name='Copper Wire', unit='meter', price=12),
                Material(category='Electrical', name='Switch', unit='piece', price=85),
                Material(category='Plumbing', name='PVC Pipe', unit='meter', price=45),
            ]
            for material in materials:
                db.session.add(material)
            db.session.commit()
            print("Sample materials created!")
    
    app.run(debug=True, port=5002)