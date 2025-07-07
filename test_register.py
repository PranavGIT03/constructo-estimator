from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Test user registration
    email = "test@example.com"
    password = "password123"
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print(f"User {email} already exists")
    else:
        # Create new user
        user = User(
            email=email,
            password=generate_password_hash(password),
            estimations_left=3
        )
        db.session.add(user)
        db.session.commit()
        print(f"User {email} created successfully")
    
    # Show all users
    users = User.query.all()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"- {user.email} (ID: {user.id}, Estimates left: {user.estimations_left})")