from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import pandas as pd
import os
from firebase_admin import firestore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Firebase setup
try:
    db = firestore.client()
except:
    # Mock database for development
    class MockDB:
        def collection(self, name):
            return MockCollection()
    
    class MockCollection:
        def document(self, doc_id=None):
            return MockDocument()
        def stream(self):
            return []
        def add(self, data):
            return None, None
    
    class MockDocument:
        def set(self, data):
            pass
        def get(self):
            return MockDocSnapshot()
        def update(self, data):
            pass
        def delete(self):
            pass
    
    class MockDocSnapshot:
        def exists(self):
            return False
        def to_dict(self):
            return {}
    
    db = MockDB()

class User(UserMixin):
    def __init__(self, user_id, email, estimations_left=3):
        self.id = user_id
        self.email = email
        self.estimations_left = estimations_left

@login_manager.user_loader
def load_user(user_id):
    try:
        doc = db.collection('users').document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            return User(user_id, data['email'], data.get('estimations_left', 3))
    except:
        pass
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        try:
            # Check if user exists
            users = db.collection('users').stream()
            for user in users:
                if user.to_dict().get('email') == email:
                    return jsonify({'error': 'Email already exists'}), 400
            
            # Create user
            user_data = {
                'email': email,
                'password': generate_password_hash(password),
                'estimations_left': 3,
                'created_at': datetime.utcnow()
            }
            db.collection('users').add(user_data)
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        try:
            users = db.collection('users').stream()
            for user_doc in users:
                user_data = user_doc.to_dict()
                if user_data.get('email') == email:
                    if check_password_hash(user_data['password'], password):
                        user = User(user_doc.id, email, user_data.get('estimations_left', 3))
                        login_user(user)
                        return jsonify({'message': 'Login successful'}), 200
            
            return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/api/materials')
def get_materials():
    try:
        materials = []
        docs = db.collection('materials').stream()
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id
            materials.append(data)
        return jsonify(materials)
    except:
        # Fallback to sample data
        return jsonify([
            {'id': '1', 'category': 'RCC', 'name': 'Cement', 'unit': 'bag', 'price': 350},
            {'id': '2', 'category': 'RCC', 'name': 'Steel Rebar', 'unit': 'kg', 'price': 65},
            {'id': '3', 'category': 'Electrical', 'name': 'Copper Wire', 'unit': 'meter', 'price': 12}
        ])

@app.route('/api/estimate', methods=['POST'])
@login_required
def create_estimate():
    if current_user.estimations_left <= 0:
        return jsonify({'error': 'No estimations left'}), 403
    
    data = request.get_json()
    materials_list = data.get('materials', [])
    
    total_cost = 0
    details = []
    
    try:
        for item in materials_list:
            material_doc = db.collection('materials').document(item['material_id']).get()
            if material_doc.exists:
                material = material_doc.to_dict()
                quantity = item['quantity']
                cost = material['price'] * quantity
                total_cost += cost
                details.append({
                    'material': material['name'],
                    'quantity': quantity,
                    'unit_price': material['price'],
                    'total': cost
                })
        
        # Save estimate
        estimate_data = {
            'user_id': current_user.id,
            'total_cost': total_cost,
            'details': details,
            'created_at': datetime.utcnow()
        }
        db.collection('estimations').add(estimate_data)
        
        # Update user's remaining estimates
        current_user.estimations_left -= 1
        db.collection('users').document(current_user.id).update({
            'estimations_left': current_user.estimations_left
        })
        
        return jsonify({
            'total_cost': total_cost,
            'details': details,
            'estimations_left': current_user.estimations_left
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_excel.html')

@app.route('/api/admin/excel-data')
@login_required
def get_excel_data():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    excel_file = 'Constructo.xlsx'
    if not os.path.exists(excel_file):
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
        return jsonify({
            'columns': df.columns.tolist(),
            'data': df.to_dict('records')
        })
    except Exception as e:
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
        
        # Also sync to Firebase
        try:
            # Clear existing materials
            materials = db.collection('materials').stream()
            for material in materials:
                material.reference.delete()
            
            # Add new materials from Excel
            for _, row in df.iterrows():
                material_data = {
                    'category': str(row.get('Category', '')),
                    'name': str(row.get('Material', '')),
                    'unit': str(row.get('Unit', '')),
                    'price': float(row.get('Price', 0))
                }
                db.collection('materials').add(material_data)
        except:
            pass  # Continue even if Firebase sync fails
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize sample data
    try:
        # Create admin user if not exists
        users = db.collection('users').stream()
        admin_exists = False
        for user in users:
            if user.to_dict().get('email') == 'admin@example.com':
                admin_exists = True
                break
        
        if not admin_exists:
            admin_data = {
                'email': 'admin@example.com',
                'password': generate_password_hash('admin123'),
                'estimations_left': 999,
                'created_at': datetime.utcnow()
            }
            db.collection('users').add(admin_data)
            print("Admin user created")
        
        # Create sample materials
        materials = list(db.collection('materials').stream())
        if len(materials) == 0:
            sample_materials = [
                {'category': 'RCC', 'name': 'Cement', 'unit': 'bag', 'price': 350},
                {'category': 'RCC', 'name': 'Steel Rebar', 'unit': 'kg', 'price': 65},
                {'category': 'Electrical', 'name': 'Copper Wire', 'unit': 'meter', 'price': 12}
            ]
            for material in sample_materials:
                db.collection('materials').add(material)
            print("Sample materials created")
    except:
        print("Using mock database - Firebase not configured")
    
    app.run(debug=True, port=5002)