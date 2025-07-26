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
    subscription_type = db.Column(db.String(20), default='free')  # free, premium

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    subcategory = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    price = db.Column(db.Float)
    tier = db.Column(db.String(20))  # eco, standard, premium
    labor_cost_percentage = db.Column(db.Float, default=0)
    tips = db.Column(db.Text)

class Estimation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plot_area = db.Column(db.Float)
    built_up_area = db.Column(db.Float)
    floors = db.Column(db.Integer)
    dining_rooms = db.Column(db.Integer)
    drawing_rooms = db.Column(db.Integer)
    lounges = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    kitchens = db.Column(db.Integer)
    utility_rooms = db.Column(db.Integer)
    car_parking = db.Column(db.Integer)
    two_wheeler_parking = db.Column(db.Integer)
    lift = db.Column(db.Boolean, default=False)
    total_cost = db.Column(db.Float)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SamplePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_width = db.Column(db.Float)
    max_width = db.Column(db.Float)
    min_length = db.Column(db.Float)
    max_length = db.Column(db.Float)
    floors = db.Column(db.Integer)
    file_path = db.Column(db.String(255))
    thumbnail_path = db.Column(db.String(255))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # construction, budget, materials, mistakes
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
            estimations_left=3,
            subscription_type='free'
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

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Create Estimate Routes
@app.route('/create-estimate')
@login_required
def create_estimate_form():
    return render_template('create_estimate.html')

@app.route('/api/estimate', methods=['POST'])
@login_required
def create_estimate():
    if current_user.estimations_left <= 0 and current_user.subscription_type == 'free':
        return jsonify({'error': 'No estimations left. Please upgrade to premium.'}), 403
    
    data = request.get_json()
    
    # Extract building details
    plot_area = data.get('plot_area', 0)
    built_up_area = data.get('built_up_area', 0)
    floors = data.get('floors', 1)
    dining_rooms = data.get('dining_rooms', 0)
    drawing_rooms = data.get('drawing_rooms', 0)
    lounges = data.get('lounges', 0)
    bedrooms = data.get('bedrooms', 0)
    bathrooms = data.get('bathrooms', 0)
    kitchens = data.get('kitchens', 0)
    utility_rooms = data.get('utility_rooms', 0)
    car_parking = data.get('car_parking', 0)
    two_wheeler_parking = data.get('two_wheeler_parking', 0)
    lift = data.get('lift', False)
    
    # Calculate costs for each category
    categories = ['Civil Work', 'Electrical', 'Plumbing', 'Sanitation', 'Steel Roofing', 
                 'Windows', 'Tiling', 'Kitchen', 'Furniture', 'Paint', 'Fall Ceiling', 
                 'Doors', 'Solar', 'HVAC', 'Waterproofing']
    
    details = {}
    total_cost = 0
    
    # Simple calculation based on built-up area and number of rooms
    # In a real app, this would be much more sophisticated
    for category in categories:
        # Calculate costs for each tier
        eco_cost = calculate_category_cost(category, 'eco', built_up_area, bedrooms, bathrooms)
        standard_cost = calculate_category_cost(category, 'standard', built_up_area, bedrooms, bathrooms)
        premium_cost = calculate_category_cost(category, 'premium', built_up_area, bedrooms, bathrooms)
        
        # Default to standard tier
        selected_tier = data.get(f'{category.lower().replace(" ", "_")}_tier', 'standard')
        selected_cost = standard_cost
        
        if selected_tier == 'eco':
            selected_cost = eco_cost
        elif selected_tier == 'premium':
            selected_cost = premium_cost
        
        details[category] = {
            'eco': eco_cost,
            'standard': standard_cost,
            'premium': premium_cost,
            'selected_tier': selected_tier,
            'selected_cost': selected_cost
        }
        
        total_cost += selected_cost
    
    # Create estimation record
    estimation = Estimation(
        user_id=current_user.id,
        plot_area=plot_area,
        built_up_area=built_up_area,
        floors=floors,
        dining_rooms=dining_rooms,
        drawing_rooms=drawing_rooms,
        lounges=lounges,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        kitchens=kitchens,
        utility_rooms=utility_rooms,
        car_parking=car_parking,
        two_wheeler_parking=two_wheeler_parking,
        lift=lift,
        total_cost=total_cost,
        details=details
    )
    
    # Reduce estimation count for free users
    if current_user.subscription_type == 'free':
        current_user.estimations_left -= 1
    
    db.session.add(estimation)
    db.session.commit()
    
    return jsonify({
        'id': estimation.id,
        'total_cost': total_cost,
        'details': details,
        'estimations_left': current_user.estimations_left
    })

# Helper function to calculate category costs
def calculate_category_cost(category, tier, built_up_area, bedrooms, bathrooms):
    # Base rates per square foot for different categories and tiers
    base_rates = {
        'Civil Work': {'eco': 1200, 'standard': 1500, 'premium': 2000},
        'Electrical': {'eco': 100, 'standard': 150, 'premium': 250},
        'Plumbing': {'eco': 80, 'standard': 120, 'premium': 200},
        'Sanitation': {'eco': 70, 'standard': 100, 'premium': 180},
        'Steel Roofing': {'eco': 150, 'standard': 250, 'premium': 400},
        'Windows': {'eco': 200, 'standard': 350, 'premium': 600},
        'Tiling': {'eco': 80, 'standard': 150, 'premium': 300},
        'Kitchen': {'eco': 500, 'standard': 1000, 'premium': 2000},
        'Furniture': {'eco': 300, 'standard': 600, 'premium': 1200},
        'Paint': {'eco': 30, 'standard': 50, 'premium': 90},
        'Fall Ceiling': {'eco': 100, 'standard': 150, 'premium': 250},
        'Doors': {'eco': 150, 'standard': 300, 'premium': 600},
        'Solar': {'eco': 50, 'standard': 100, 'premium': 200},
        'HVAC': {'eco': 100, 'standard': 200, 'premium': 400},
        'Waterproofing': {'eco': 30, 'standard': 50, 'premium': 80}
    }
    
    # Get base rate for this category and tier
    base_rate = base_rates.get(category, {'eco': 100, 'standard': 150, 'premium': 250}).get(tier, 150)
    
    # Calculate based on area and add room-specific costs
    cost = base_rate * built_up_area
    
    # Add room-specific costs for certain categories
    if category == 'Plumbing' or category == 'Sanitation':
        cost += (bathrooms * base_rate * 20)  # Additional cost per bathroom
    
    if category == 'Kitchen':
        cost += (base_rate * 50)  # Fixed additional cost for kitchen
    
    return cost

@app.route('/api/my-estimates')
@login_required
def get_my_estimates():
    estimates = Estimation.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': e.id,
        'plot_area': e.plot_area,
        'built_up_area': e.built_up_area,
        'floors': e.floors,
        'total_cost': e.total_cost,
        'details': e.details,
        'created_at': e.created_at.isoformat()
    } for e in estimates])

@app.route('/api/estimate/<int:estimate_id>')
@login_required
def get_estimate_detail(estimate_id):
    estimate = Estimation.query.get_or_404(estimate_id)
    
    # Check if the estimate belongs to the current user
    if estimate.user_id != current_user.id and current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': estimate.id,
        'plot_area': estimate.plot_area,
        'built_up_area': estimate.built_up_area,
        'floors': estimate.floors,
        'dining_rooms': estimate.dining_rooms,
        'drawing_rooms': estimate.drawing_rooms,
        'lounges': estimate.lounges,
        'bedrooms': estimate.bedrooms,
        'bathrooms': estimate.bathrooms,
        'kitchens': estimate.kitchens,
        'utility_rooms': estimate.utility_rooms,
        'car_parking': estimate.car_parking,
        'two_wheeler_parking': estimate.two_wheeler_parking,
        'lift': estimate.lift,
        'total_cost': estimate.total_cost,
        'details': estimate.details,
        'created_at': estimate.created_at.isoformat()
    })

# Sample Plan Routes
@app.route('/sample-plans')
@login_required
def sample_plans():
    return render_template('sample_plans.html')

@app.route('/api/sample-plans')
def get_sample_plans():
    width = request.args.get('width', type=float)
    length = request.args.get('length', type=float)
    floors = request.args.get('floors', type=int)
    
    query = SamplePlan.query
    
    if width:
        query = query.filter(SamplePlan.min_width <= width, SamplePlan.max_width >= width)
    
    if length:
        query = query.filter(SamplePlan.min_length <= length, SamplePlan.max_length >= length)
    
    if floors:
        query = query.filter(SamplePlan.floors == floors)
    
    plans = query.all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'min_width': p.min_width,
        'max_width': p.max_width,
        'min_length': p.min_length,
        'max_length': p.max_length,
        'floors': p.floors,
        'thumbnail_path': p.thumbnail_path
    } for p in plans])

@app.route('/api/sample-plan/<int:plan_id>')
def get_sample_plan(plan_id):
    plan = SamplePlan.query.get_or_404(plan_id)
    return send_file(plan.file_path, as_attachment=True)

# Detailed BOQ Routes
@app.route('/detailed-boq')
@login_required
def detailed_boq():
    estimate_id = request.args.get('estimate')
    return render_template('detailed_boq.html', estimate_id=estimate_id)

@app.route('/api/materials')
def get_materials():
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    tier = request.args.get('tier')
    
    query = Material.query
    
    if category:
        query = query.filter(Material.category == category)
    
    if subcategory:
        query = query.filter(Material.subcategory == subcategory)
    
    if tier:
        query = query.filter(Material.tier == tier)
    
    materials = query.all()
    
    return jsonify([{
        'id': m.id,
        'category': m.category,
        'subcategory': m.subcategory,
        'name': m.name,
        'brand': m.brand,
        'unit': m.unit,
        'price': m.price,
        'tier': m.tier,
        'labor_cost_percentage': m.labor_cost_percentage,
        'tips': m.tips
    } for m in materials])

@app.route('/api/categories')
def get_categories():
    categories = db.session.query(Material.category).distinct().all()
    return jsonify([c[0] for c in categories])

@app.route('/api/subcategories')
def get_subcategories():
    category = request.args.get('category')
    query = db.session.query(Material.subcategory).distinct()
    
    if category:
        query = query.filter(Material.category == category)
    
    subcategories = query.all()
    return jsonify([s[0] for s in subcategories if s[0]])

# Guide to Building a Home Routes
@app.route('/guides')
def guides():
    return render_template('guides.html')

@app.route('/api/articles')
def get_articles():
    category = request.args.get('category')
    
    query = Article.query
    
    if category:
        query = query.filter(Article.category == category)
    
    articles = query.all()
    
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'category': a.category,
        'created_at': a.created_at.isoformat()
    } for a in articles])

@app.route('/api/article/<int:article_id>')
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'category': article.category,
        'created_at': article.created_at.isoformat()
    })

# Subscription Routes
@app.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html')

@app.route('/api/upgrade-subscription', methods=['POST'])
@login_required
def upgrade_subscription():
    # In a real app, this would handle payment processing
    current_user.subscription_type = 'premium'
    current_user.estimations_left = 999  # Unlimited for premium
    db.session.commit()
    
    return jsonify({'message': 'Subscription upgraded successfully'})

# FAQ, Testimonials, Contact Routes
@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

# Admin Routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

@app.route('/admin/materials')
@login_required
def admin_materials():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_materials.html')

@app.route('/admin/sample-plans')
@login_required
def admin_sample_plans():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_sample_plans.html')

@app.route('/admin/articles')
@login_required
def admin_articles():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_articles.html')

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.email != 'admin@example.com':
        return redirect(url_for('index'))
    return render_template('admin_users.html')

# Admin API Routes
@app.route('/api/admin/materials')
@login_required
def admin_get_materials():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    materials = Material.query.all()
    return jsonify([{
        'id': m.id,
        'category': m.category,
        'subcategory': m.subcategory,
        'name': m.name,
        'brand': m.brand,
        'unit': m.unit,
        'price': m.price,
        'tier': m.tier,
        'labor_cost_percentage': m.labor_cost_percentage,
        'tips': m.tips
    } for m in materials])

@app.route('/api/admin/material/<int:material_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def admin_manage_material(material_id):
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        material = Material.query.get_or_404(material_id)
        return jsonify({
            'id': material.id,
            'category': material.category,
            'subcategory': material.subcategory,
            'name': material.name,
            'brand': material.brand,
            'unit': material.unit,
            'price': material.price,
            'tier': material.tier,
            'labor_cost_percentage': material.labor_cost_percentage,
            'tips': material.tips
        })
    
    elif request.method == 'PUT':
        material = Material.query.get_or_404(material_id)
        data = request.get_json()
        
        material.category = data.get('category', material.category)
        material.subcategory = data.get('subcategory', material.subcategory)
        material.name = data.get('name', material.name)
        material.brand = data.get('brand', material.brand)
        material.unit = data.get('unit', material.unit)
        material.price = data.get('price', material.price)
        material.tier = data.get('tier', material.tier)
        material.labor_cost_percentage = data.get('labor_cost_percentage', material.labor_cost_percentage)
        material.tips = data.get('tips', material.tips)
        
        db.session.commit()
        return jsonify({'message': 'Material updated successfully'})
    
    elif request.method == 'DELETE':
        material = Material.query.get_or_404(material_id)
        db.session.delete(material)
        db.session.commit()
        return jsonify({'message': 'Material deleted successfully'})

@app.route('/api/admin/material', methods=['POST'])
@login_required
def admin_add_material():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    material = Material(
        category=data.get('category'),
        subcategory=data.get('subcategory'),
        name=data.get('name'),
        brand=data.get('brand'),
        unit=data.get('unit'),
        price=data.get('price'),
        tier=data.get('tier'),
        labor_cost_percentage=data.get('labor_cost_percentage', 0),
        tips=data.get('tips')
    )
    
    db.session.add(material)
    db.session.commit()
    
    return jsonify({
        'id': material.id,
        'message': 'Material added successfully'
    })

@app.route('/api/admin/sample-plans')
@login_required
def admin_get_sample_plans():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    plans = SamplePlan.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'min_width': p.min_width,
        'max_width': p.max_width,
        'min_length': p.min_length,
        'max_length': p.max_length,
        'floors': p.floors,
        'file_path': p.file_path,
        'thumbnail_path': p.thumbnail_path
    } for p in plans])

@app.route('/api/admin/sample-plan/<int:plan_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def admin_manage_sample_plan(plan_id):
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        plan = SamplePlan.query.get_or_404(plan_id)
        return jsonify({
            'id': plan.id,
            'name': plan.name,
            'min_width': plan.min_width,
            'max_width': plan.max_width,
            'min_length': plan.min_length,
            'max_length': plan.max_length,
            'floors': plan.floors,
            'file_path': plan.file_path,
            'thumbnail_path': plan.thumbnail_path
        })
    
    elif request.method == 'PUT':
        plan = SamplePlan.query.get_or_404(plan_id)
        data = request.get_json()
        
        plan.name = data.get('name', plan.name)
        plan.min_width = data.get('min_width', plan.min_width)
        plan.max_width = data.get('max_width', plan.max_width)
        plan.min_length = data.get('min_length', plan.min_length)
        plan.max_length = data.get('max_length', plan.max_length)
        plan.floors = data.get('floors', plan.floors)
        
        db.session.commit()
        return jsonify({'message': 'Sample plan updated successfully'})
    
    elif request.method == 'DELETE':
        plan = SamplePlan.query.get_or_404(plan_id)
        db.session.delete(plan)
        db.session.commit()
        return jsonify({'message': 'Sample plan deleted successfully'})

@app.route('/api/admin/sample-plan', methods=['POST'])
@login_required
def admin_add_sample_plan():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Handle file upload in a real app
    # For now, just save the data
    data = request.get_json()
    
    plan = SamplePlan(
        name=data.get('name'),
        min_width=data.get('min_width'),
        max_width=data.get('max_width'),
        min_length=data.get('min_length'),
        max_length=data.get('max_length'),
        floors=data.get('floors'),
        file_path=data.get('file_path', ''),
        thumbnail_path=data.get('thumbnail_path', '')
    )
    
    db.session.add(plan)
    db.session.commit()
    
    return jsonify({
        'id': plan.id,
        'message': 'Sample plan added successfully'
    })

@app.route('/api/admin/articles')
@login_required
def admin_get_articles():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    articles = Article.query.all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'category': a.category,
        'created_at': a.created_at.isoformat()
    } for a in articles])

@app.route('/api/admin/article/<int:article_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def admin_manage_article(article_id):
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        article = Article.query.get_or_404(article_id)
        return jsonify({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'category': article.category,
            'created_at': article.created_at.isoformat()
        })
    
    elif request.method == 'PUT':
        article = Article.query.get_or_404(article_id)
        data = request.get_json()
        
        article.title = data.get('title', article.title)
        article.content = data.get('content', article.content)
        article.category = data.get('category', article.category)
        
        db.session.commit()
        return jsonify({'message': 'Article updated successfully'})
    
    elif request.method == 'DELETE':
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': 'Article deleted successfully'})

@app.route('/api/admin/article', methods=['POST'])
@login_required
def admin_add_article():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    article = Article(
        title=data.get('title'),
        content=data.get('content'),
        category=data.get('category')
    )
    
    db.session.add(article)
    db.session.commit()
    
    return jsonify({
        'id': article.id,
        'message': 'Article added successfully'
    })

@app.route('/api/admin/users')
@login_required
def admin_get_users():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'email': u.email,
        'estimations_left': u.estimations_left,
        'subscription_type': u.subscription_type
    } for u in users])

@app.route('/api/admin/recent-estimates')
@login_required
def admin_recent_estimates():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get the 10 most recent estimates
    estimates = db.session.query(Estimation, User.email).join(User).order_by(Estimation.created_at.desc()).limit(10).all()
    
    return jsonify([{
        'id': e.Estimation.id,
        'user_email': e.email,
        'total_cost': e.Estimation.total_cost,
        'built_up_area': e.Estimation.built_up_area,
        'floors': e.Estimation.floors,
        'created_at': e.Estimation.created_at.isoformat()
    } for e in estimates])

@app.route('/api/admin/user-stats')
@login_required
def admin_user_stats():
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    total_users = User.query.count()
    premium_users = User.query.filter_by(subscription_type='premium').count()
    total_estimates = Estimation.query.count()
    
    # Get new users today
    from datetime import datetime, timedelta
    today = datetime.utcnow().date()
    new_users_today = 0  # Placeholder since we don't have a created_at field for users
    
    return jsonify({
        'total_users': total_users,
        'premium_users': premium_users,
        'total_estimates': total_estimates,
        'new_users_today': new_users_today
    })

@app.route('/api/admin/user/<int:user_id>', methods=['GET', 'PUT'])
@login_required
def admin_manage_user(user_id):
    if current_user.email != 'admin@example.com':
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return jsonify({
            'id': user.id,
            'email': user.email,
            'estimations_left': user.estimations_left,
            'subscription_type': user.subscription_type
        })
    
    elif request.method == 'PUT':
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        user.estimations_left = data.get('estimations_left', user.estimations_left)
        user.subscription_type = data.get('subscription_type', user.subscription_type)
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create sample materials if none exist
        if not Material.query.first():
            materials = [
                Material(category='Civil Work', subcategory='Cement', name='Cement', brand='UltraTech', unit='bag', price=350, tier='standard'),
                Material(category='Civil Work', subcategory='Steel', name='Steel Rebar', brand='Tata', unit='kg', price=65, tier='standard'),
                Material(category='Civil Work', subcategory='Sand', name='Sand', brand='', unit='cubic_ft', price=45, tier='standard'),
                Material(category='Electrical', subcategory='Wire', name='Copper Wire', brand='Havells', unit='meter', price=12, tier='standard'),
                Material(category='Electrical', subcategory='Switches', name='Switch', brand='Anchor', unit='piece', price=85, tier='standard'),
                Material(category='Plumbing', subcategory='Pipes', name='PVC Pipe', brand='Astral', unit='meter', price=45, tier='standard'),
                
                # Add some eco and premium options
                Material(category='Civil Work', subcategory='Cement', name='Cement', brand='Ambuja', unit='bag', price=320, tier='eco'),
                Material(category='Civil Work', subcategory='Cement', name='Cement', brand='JK', unit='bag', price=380, tier='premium'),
                
                Material(category='Windows', subcategory='Sliding', name='Sliding Window', brand='Standard', unit='sq ft', price=250, tier='standard', 
                       labor_cost_percentage=15, tips='Ensure proper sealing around the frame to prevent water leakage.'),
                Material(category='Windows', subcategory='Sliding', name='Sliding Window', brand='Economy', unit='sq ft', price=180, tier='eco', 
                       labor_cost_percentage=15, tips='Economy windows may have thinner frames and glass.'),
                Material(category='Windows', subcategory='Sliding', name='Sliding Window', brand='Premium', unit='sq ft', price=350, tier='premium', 
                       labor_cost_percentage=20, tips='Premium windows offer better insulation and noise reduction.'),
                
                Material(category='Doors', subcategory='Main Door', name='Solid Wood Door', brand='Standard', unit='piece', price=12000, tier='standard', 
                       labor_cost_percentage=10, tips='Treat wood doors with anti-termite solution before installation.'),
                Material(category='Doors', subcategory='Main Door', name='Engineered Wood Door', brand='Economy', unit='piece', price=8000, tier='eco', 
                       labor_cost_percentage=10, tips='Engineered wood is more resistant to warping than solid wood.'),
                Material(category='Doors', subcategory='Main Door', name='Teak Wood Door', brand='Premium', unit='piece', price=25000, tier='premium', 
                       labor_cost_percentage=15, tips='Teak wood offers excellent durability and natural resistance to weather.')
            ]
            for material in materials:
                db.session.add(material)
            db.session.commit()
            print("Sample materials created!")
            
        # Create sample articles if none exist
        if not Article.query.first():
            articles = [
                Article(
                    title="Understanding Construction Stages",
                    category="construction",
                    content="<h3>Foundation</h3><p>The foundation is the most critical part of your home. It supports the entire structure and ensures stability.</p><h3>Framing</h3><p>Once the foundation is complete, the framing creates the skeleton of your home.</p><h3>Plumbing and Electrical</h3><p>These systems are installed before the walls are closed up.</p><h3>Finishing</h3><p>The final stage includes flooring, painting, fixtures, and appliances.</p>"
                ),
                Article(
                    title="Budget Management Tips",
                    category="budget",
                    content="<h3>Set Priorities</h3><p>Decide which areas of your home deserve more investment.</p><h3>Get Multiple Quotes</h3><p>Always compare prices from different vendors and contractors.</p><h3>Buffer Fund</h3><p>Always keep a 10-15% buffer in your budget for unexpected expenses.</p><h3>Track Expenses</h3><p>Maintain a detailed record of all expenses to avoid overspending.</p>"
                ),
                Article(
                    title="Choosing the Right Materials",
                    category="materials",
                    content="<h3>Quality vs. Cost</h3><p>Sometimes investing in higher quality materials can save money in the long run.</p><h3>Local Availability</h3><p>Consider materials that are readily available in your area to reduce transportation costs.</p><h3>Durability</h3><p>Choose materials that can withstand your local climate conditions.</p><h3>Maintenance Requirements</h3><p>Consider the long-term maintenance needs and costs of different materials.</p>"
                ),
                Article(
                    title="Common Construction Mistakes to Avoid",
                    category="mistakes",
                    content="<h3>Poor Planning</h3><p>Rushing into construction without proper planning can lead to costly mistakes.</p><h3>Ignoring Building Codes</h3><p>Always ensure your construction complies with local building codes and regulations.</p><h3>Hiring Unqualified Contractors</h3><p>Always check references and credentials before hiring contractors.</p><h3>Overlooking Drainage</h3><p>Proper drainage is essential to prevent water damage to your home.</p>"
                )
            ]
            for article in articles:
                db.session.add(article)
            db.session.commit()
            print("Sample articles created!")
            
        # Create sample plans if none exist
        if not SamplePlan.query.first():
            plans = [
                SamplePlan(
                    name="Compact 2BHK",
                    min_width=20,
                    max_width=25,
                    min_length=30,
                    max_length=35,
                    floors=1,
                    file_path="/static/plans/compact_2bhk.pdf",
                    thumbnail_path="/static/thumbnails/compact_2bhk.jpg"
                ),
                SamplePlan(
                    name="Spacious 3BHK",
                    min_width=25,
                    max_width=30,
                    min_length=35,
                    max_length=40,
                    floors=2,
                    file_path="/static/plans/spacious_3bhk.pdf",
                    thumbnail_path="/static/thumbnails/spacious_3bhk.jpg"
                ),
                SamplePlan(
                    name="Luxury 4BHK",
                    min_width=30,
                    max_width=40,
                    min_length=40,
                    max_length=50,
                    floors=3,
                    file_path="/static/plans/luxury_4bhk.pdf",
                    thumbnail_path="/static/thumbnails/luxury_4bhk.jpg"
                )
            ]
            for plan in plans:
                db.session.add(plan)
            db.session.commit()
            print("Sample plans created!")
    
    # No app.run() here - this is handled in run.py