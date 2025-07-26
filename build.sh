#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Create a directory for static files if it doesn't exist
mkdir -p static/plans static/thumbnails

# Create the database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Create admin user and sample data
python -c "
from app import app, db, User, Material, Article, SamplePlan;
from werkzeug.security import generate_password_hash;
from datetime import datetime;

app.app_context().push();

# Create admin user if not exists
admin_email = 'admin@example.com';
admin = User.query.filter_by(email=admin_email).first();
if not admin:
    admin = User(
        email=admin_email,
        password=generate_password_hash('admin123'),
        estimations_left=999,
        subscription_type='premium'
    );
    db.session.add(admin);
    db.session.commit();
    print('Admin user created');
"