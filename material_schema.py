# This will be imported from app.py
db = None

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # e.g., RCC, Electrical
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    price = db.Column(db.Float)
