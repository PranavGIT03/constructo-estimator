from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# This will be imported from app.py
db = None

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    premium_expiry = db.Column(db.DateTime)
    estimations_left = db.Column(db.Integer, default=0)
    subscription_type = db.Column(db.String(20), default='free')  # free, standard, eco_plus, premium
