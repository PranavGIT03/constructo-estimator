import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Paint Data
paint_data = [
    # Exterior Paints
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Ace', 'brand': 'Asian Paints', 'price': 320, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Apex', 'brand': 'Asian Paints', 'price': 692, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Ultima', 'brand': 'Asian Paints', 'price': 922, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Exterior Promise', 'brand': 'Nerolac', 'price': 250, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Weathershield', 'brand': 'Nerolac', 'price': 450, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Paints', 'name': 'Weathershield Dustproof', 'brand': 'Nerolac', 'price': 775, 'unit': 'litre'},
    
    # Exterior Texture
    {'category': 'Paint', 'subcategory': 'Exterior Texture', 'name': 'DuraTex', 'brand': '', 'price': 115, 'unit': 'kg'},
    {'category': 'Paint', 'subcategory': 'Exterior Texture', 'name': 'Dholpur', 'brand': '', 'price': 115, 'unit': 'kg'},
    {'category': 'Paint', 'subcategory': 'Exterior Texture', 'name': 'Roller Finish', 'brand': '', 'price': 75, 'unit': 'kg'},
    
    # Interior Texture
    {'category': 'Paint', 'subcategory': 'Interior Texture', 'name': 'Archi Concrete', 'brand': '', 'price': 115, 'unit': 'kg'},
    {'category': 'Paint', 'subcategory': 'Interior Texture', 'name': 'Stucco', 'brand': '', 'price': 110, 'unit': 'kg'},
    {'category': 'Paint', 'subcategory': 'Interior Texture', 'name': 'Roller Finish', 'brand': '', 'price': 75, 'unit': 'kg'},
    
    # Interior Paints
    {'category': 'Paint', 'subcategory': 'Interior Paints', 'name': 'Lustre', 'brand': 'Asian Paints', 'price': 367, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Paints', 'name': 'Apcolite Protek Matt', 'brand': 'Asian Paints', 'price': 506, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Paints', 'name': 'Apcolite Shyne Premium', 'brand': 'Asian Paints', 'price': 498, 'unit': 'litre'},
    
    # Putty
    {'category': 'Paint', 'subcategory': 'Putty', 'name': 'Putty', 'brand': 'Birla', 'price': 520, 'unit': '20kg'},
    
    # Exterior Primer
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'Sparc Trucare', 'brand': 'Asian Paints', 'price': 164, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'Advanced', 'brand': 'Asian Paints', 'price': 233, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'Primero', 'brand': 'Asian Paints', 'price': 258, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'Promise Exterior', 'brand': 'Dulux', 'price': 236, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'Standard', 'brand': 'Dulux', 'price': 299, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Exterior Primer', 'name': 'WeatherShield Powerflexx', 'brand': 'Dulux', 'price': 618, 'unit': 'litre'},
    
    # Interior Primer
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'Sparc Trucare', 'brand': 'Asian Paints', 'price': 120, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'Trucare Interior', 'brand': 'Asian Paints', 'price': 201, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'Royale', 'brand': 'Asian Paints', 'price': 276, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'Promise Interior', 'brand': 'Dulux', 'price': 236, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'Standard', 'brand': 'Dulux', 'price': 299, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Interior Primer', 'name': 'WeatherShield Interior', 'brand': 'Dulux', 'price': 618, 'unit': 'litre'},
    
    # Red Oxide
    {'category': 'Paint', 'subcategory': 'Red Oxide', 'name': 'Sparc Trucare', 'brand': 'Asian Paints', 'price': 181, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Red Oxide', 'name': 'Trucare Yellow', 'brand': 'Asian Paints', 'price': 299, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Red Oxide', 'name': 'Apcolite Advanced', 'brand': 'Asian Paints', 'price': 488, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Red Oxide', 'name': 'Zinc Yellow', 'brand': 'Dulux', 'price': 345, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Red Oxide', 'name': 'Red Primer', 'brand': 'Dulux', 'price': 269, 'unit': 'litre'},
    
    # Wood PU Exterior
    {'category': 'Paint', 'subcategory': 'Wood PU Exterior', 'name': 'PU Exterior Palette', 'brand': 'Asian Paints', 'price': 1402, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Wood PU Exterior', 'name': 'PU Exterior Luxury', 'brand': 'Asian Paints', 'price': 1135, 'unit': 'litre'},
    
    # Wood PU Interior
    {'category': 'Paint', 'subcategory': 'Wood PU Interior', 'name': 'PU Interior Palette', 'brand': 'Asian Paints', 'price': 1199, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Wood PU Interior', 'name': 'PU Interior Luxury', 'brand': 'Asian Paints', 'price': 1022, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Wood PU Interior', 'name': 'Sadolin Melamine Sealer', 'brand': 'Dulux', 'price': 474, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Wood PU Interior', 'name': 'PU Interior Luxury', 'brand': 'Dulux', 'price': 1105, 'unit': 'litre'},
    
    # Oil Paint
    {'category': 'Paint', 'subcategory': 'Oil Paint', 'name': 'Apcolite Enamel Gloss', 'brand': 'Asian Paints', 'price': 369, 'unit': 'litre'},
    {'category': 'Paint', 'subcategory': 'Oil Paint', 'name': 'Apcolite RustShield', 'brand': 'Asian Paints', 'price': 413, 'unit': 'litre'},
]

# Add paint data to Firebase
for item in paint_data:
    db.collection('materials').add(item)

print(f"✅ Added {len(paint_data)} paint items to Firebase!")
print("Paint category created with 11 subcategories")