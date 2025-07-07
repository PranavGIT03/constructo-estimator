from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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
            users = db.collection('users').where('email', '==', email).stream()
            if list(users):
                return jsonify({'error': 'Email already exists'}), 400
            
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
            users = db.collection('users').where('email', '==', email).stream()
            for user_doc in users:
                user_data = user_doc.to_dict()
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

@app.route('/api/categories')
def get_categories():
    try:
        materials = db.collection('materials').stream()
        categories = {}
        
        for material in materials:
            data = material.to_dict()
            category = data.get('category')
            subcategory = data.get('subcategory')
            
            if category not in categories:
                categories[category] = {}
            
            if subcategory not in categories[category]:
                categories[category][subcategory] = []
            
            item = {
                'id': material.id,
                'name': data.get('name'),
                'brand': data.get('brand', ''),
                'price': data.get('price'),
                'unit': data.get('unit')
            }
            categories[category][subcategory].append(item)
        
        return jsonify(categories)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estimate', methods=['POST'])
@login_required
def create_estimate():
    if current_user.estimations_left <= 0:
        return jsonify({'error': 'No estimations left'}), 403
    
    data = request.get_json()
    selected_items = data.get('items', [])
    
    total_cost = 0
    details = []
    
    try:
        for item in selected_items:
            material_doc = db.collection('materials').document(item['id']).get()
            if material_doc.exists:
                material = material_doc.to_dict()
                quantity = float(item['quantity'])
                cost = material['price'] * quantity
                total_cost += cost
                
                details.append({
                    'category': material.get('category'),
                    'subcategory': material.get('subcategory'),
                    'name': material['name'],
                    'brand': material.get('brand', ''),
                    'quantity': quantity,
                    'unit_price': material['price'],
                    'unit': material['unit'],
                    'total': cost
                })
        
        estimate_data = {
            'user_id': current_user.id,
            'total_cost': total_cost,
            'details': details,
            'created_at': datetime.utcnow()
        }
        db.collection('estimations').add(estimate_data)
        
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
    return render_template('dashboard_new.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)