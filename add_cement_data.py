import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Cement data
cements = [
    {'name': 'Ultratech', 'price': 360, 'unit': 'bag'},
    {'name': 'Birla', 'price': 320, 'unit': 'bag'},
    {'name': 'JK', 'price': 320, 'unit': 'bag'}
]

# Add to Firebase
for cement in cements:
    cement['category'] = 'Cement'
    db.collection('materials').add(cement)
    print(f"Added: {cement['name']}")

print("✅ Cement data added to Firebase!")