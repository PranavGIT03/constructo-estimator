from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Create admin user
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    existing_admin = User.query.filter_by(email=admin_email).first()
    if existing_admin:
        print(f"Admin user {admin_email} already exists")
    else:
        admin_user = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            estimations_left=999
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created: {admin_email}")
        print(f"Password: {admin_password}")
        print("Access admin dashboard at: /admin")