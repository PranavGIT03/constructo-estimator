import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Update RCC items with fixed rates
rcc_updates = [
    {'name': 'Standard Sand', 'price': 45, 'unit': 'cft'},
    {'name': 'Standard Aggregate', 'price': 60, 'unit': 'cft'},
    {'name': 'Standard Brick', 'price': 8, 'unit': 'piece'}
]

# Find and update RCC items
materials = db.collection('materials').where('category', '==', 'RCC').stream()

for material in materials:
    data = material.to_dict()
    
    # Update Sand
    if data.get('subcategory') == 'Sand':
        material.reference.update({'price': 45, 'unit': 'cft'})
        print("Updated Sand: ₹45/cft")
    
    # Update Aggregate
    elif data.get('subcategory') == 'Aggregate':
        material.reference.update({'price': 60, 'unit': 'cft'})
        print("Updated Aggregate: ₹60/cft")
    
    # Update Brick
    elif data.get('subcategory') == 'Brick':
        material.reference.update({'price': 8, 'unit': 'piece'})
        print("Updated Brick: ₹8/piece")

print("✅ RCC rates updated with fixed pricing!")