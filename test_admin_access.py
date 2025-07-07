from app import app, User
from werkzeug.security import check_password_hash

with app.app_context():
    # Check if admin user exists
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin:
        print("Admin user exists:")
        print(f"Email: {admin.email}")
        print(f"ID: {admin.id}")
        
        # Test password
        test_password = "admin123"
        if check_password_hash(admin.password, test_password):
            print("Password is correct")
        else:
            print("Password is incorrect")
    else:
        print("Admin user does not exist")
        
    # List all users
    users = User.query.all()
    print(f"\nAll users ({len(users)}):")
    for user in users:
        print(f"- {user.email} (ID: {user.id})")