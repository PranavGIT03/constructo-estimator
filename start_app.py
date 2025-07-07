from app import app

if __name__ == '__main__':
    print("=== Constructo Application ===")
    print("Main app: http://localhost:5001")
    print("Test page: http://localhost:5001/test")
    print("Dashboard: http://localhost:5001/dashboard")
    print("")
    print("Your data is stored in these tables:")
    print("- user: User accounts (email, password, estimations_left)")
    print("- material: Construction materials (name, category, price, unit)")
    print("- estimation: Cost estimates (user_id, total_cost, details, created_at)")
    print("")
    print("Pre-created test user:")
    print("Email: test@example.com")
    print("Password: password123")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5001)