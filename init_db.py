from app import app, db, User, Material, Estimation

with app.app_context():
    # Create all tables
    db.create_all()
    
    # Check what tables exist
    print("Tables created:")
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print(inspector.get_table_names())
    
    # Create sample materials if none exist
    if not Material.query.first():
        materials = [
            Material(category='RCC', name='Cement', unit='bag', price=350),
            Material(category='RCC', name='Steel Rebar', unit='kg', price=65),
            Material(category='RCC', name='Sand', unit='cubic_ft', price=45),
            Material(category='Electrical', name='Copper Wire', unit='meter', price=12),
            Material(category='Electrical', name='Switch', unit='piece', price=85),
            Material(category='Plumbing', name='PVC Pipe', unit='meter', price=45),
        ]
        for material in materials:
            db.session.add(material)
        db.session.commit()
        print(f"Created {len(materials)} sample materials")
    
    # Show current data
    print(f"Users: {User.query.count()}")
    print(f"Materials: {Material.query.count()}")
    print(f"Estimations: {Estimation.query.count()}")