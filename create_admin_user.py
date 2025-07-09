import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Create admin user
admin_data = {
    'email': 'admin@example.com',
    'password': generate_password_hash('admin123'),
    'estimations_left': 999,
    'created_at': datetime.utcnow()
}

# Check if admin exists
users = db.collection('users').where('email', '==', 'admin@example.com').stream()
admin_exists = len(list(users)) > 0

if not admin_exists:
    db.collection('users').add(admin_data)
    print("✅ Admin user created!")
    print("Email: admin@example.com")
    print("Password: admin123")
else:
    print("Admin user already exists")