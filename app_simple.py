from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock Firebase database
class MockDB:
    def __init__(self):
        self.users = {}
        self.materials = {
            '1': {'category': 'RCC', 'name': 'Cement', 'unit': 'bag', 'price': 350},
            '2': {'category': 'RCC', 'name': 'Steel Rebar', 'unit': 'kg', 'price': 65},
            '3': {'category': 'Electrical', 'name': 'Copper Wire', 'unit': 'meter', 'price': 12},
            '4': {'category': 'Plumbing', 'name': 'PVC Pipe', 'unit': 'meter', 'price': 45}
        }
        self.estimations = {}
        self.counter = 5

db = MockDB()

class User(UserMixin):
    def __init__(self, user_id, email, estimations_left=3):
        self.id = user_id
        self.email = email
        self.estimations_left = estimations_left

@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.get(user_id)
    if user_data:
        return User(user_id, user_data['email'], user_data.get('estimations_left', 3))
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
        
        for user_data in db.users.values():
            if user_data.get('email') == email:
                return jsonify({'error': 'Email already exists'}), 400
        
        user_id = str(len(db.users) + 1)
        db.users[user_id] = {
            'email': email,
            'password': generate_password_hash(password),
            'estimations_left': 3
        }
        return jsonify({'message': 'User created successfully'}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email')
        password = data.get('password')
        
        for user_id, user_data in db.users.items():
            if user_data.get('email') == email:
                if check_password_hash(user_data['password'], password):
                    user = User(user_id, email, user_data.get('estimations_left', 3))
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
    materials = []
    for mat_id, mat_data in db.materials.items():
        mat_data['id'] = mat_id
        materials.append(mat_data)
    return jsonify(materials)

@app.route('/api/estimate', methods=['POST'])
@login_required
def create_estimate():
    if current_user.estimations_left <= 0:
        return jsonify({'error': 'No estimations left'}), 403
    
    data = request.get_json()
    materials_list = data.get('materials', [])
    
    total_cost = 0
    details = []
    
    for item in materials_list:
        material = db.materials.get(item['material_id'])
        if material:
            quantity = item['quantity']
            cost = material['price'] * quantity
            total_cost += cost
            details.append({
                'material': material['name'],
                'quantity': quantity,
                'unit_price': material['price'],
                'total': cost
            })
    
    est_id = str(len(db.estimations) + 1)
    db.estimations[est_id] = {
        'user_id': current_user.id,
        'total_cost': total_cost,
        'details': details,
        'created_at': datetime.utcnow().isoformat()
    }
    
    db.users[current_user.id]['estimations_left'] -= 1
    current_user.estimations_left -= 1
    
    return jsonify({
        'total_cost': total_cost,
        'details': details,
        'estimations_left': current_user.estimations_left
    })

@app.route('/api/my-estimates')
@login_required
def get_my_estimates():
    estimates = []
    for est_id, est_data in db.estimations.items():
        if est_data['user_id'] == current_user.id:
            est_data['id'] = est_id
            estimates.append(est_data)
    return jsonify(estimates)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_simple.html')

@app.route('/api/admin/materials', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def admin_materials():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        return jsonify(list(db.materials.values()))
    
    elif request.method == 'POST':
        data = request.get_json()
        mat_id = str(db.counter)
        db.materials[mat_id] = {
            'category': data.get('category'),
            'name': data.get('name'),
            'unit': data.get('unit'),
            'price': float(data.get('price', 0))
        }
        db.counter += 1
        return jsonify({'success': True, 'id': mat_id})
    
    elif request.method == 'PUT':
        data = request.get_json()
        mat_id = data.get('id')
        if mat_id in db.materials:
            db.materials[mat_id].update({
                'category': data.get('category'),
                'name': data.get('name'),
                'unit': data.get('unit'),
                'price': float(data.get('price', 0))
            })
            return jsonify({'success': True})
        return jsonify({'error': 'Material not found'}), 404
    
    elif request.method == 'DELETE':
        mat_id = request.args.get('id')
        if mat_id in db.materials:
            del db.materials[mat_id]
            return jsonify({'success': True})
        return jsonify({'error': 'Material not found'}), 404

if __name__ == '__main__':
    # Create admin user
    db.users['admin'] = {
        'email': 'admin@example.com',
        'password': generate_password_hash('admin123'),
        'estimations_left': 999
    }
    
    app.run(debug=True, port=5002)