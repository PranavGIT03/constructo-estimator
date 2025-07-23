#!/usr/bin/env python3
from app import app

if __name__ == '__main__':
    print("Starting Constructo application...")
    print("Visit: http://localhost:5001")
    
    # Initialize the database
    with app.app_context():
        from app import db
        db.create_all()
        
        # Check if admin user exists
        from app import User
        from werkzeug.security import generate_password_hash
        
        admin_email = "admin@example.com"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            print("Creating admin user...")
            admin = User(
                email=admin_email,
                password=generate_password_hash("admin123"),
                estimations_left=999,
                subscription_type="premium"
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: {admin_email}")
    
    app.run(debug=True, host='0.0.0.0', port=5001)