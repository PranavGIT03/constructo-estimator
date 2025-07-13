import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Plumbing Data
plumbing_data = [
    # CPVC Pipes
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '½" (15mm)', 'brand': 'Kasta', 'price': 42, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '½" (15mm)', 'brand': 'Finolex', 'price': 35, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '½" (15mm)', 'brand': 'Ashirvad', 'price': 40, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '¾" (20mm)', 'brand': 'Kasta', 'price': 58, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '¾" (20mm)', 'brand': 'Finolex', 'price': 45, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '¾" (20mm)', 'brand': 'Ashirvad', 'price': 52, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1" (25mm)', 'brand': 'Kasta', 'price': 70, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1" (25mm)', 'brand': 'Finolex', 'price': 55, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1" (25mm)', 'brand': 'Ashirvad', 'price': 65, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1¼" (32mm)', 'brand': 'Kasta', 'price': 98, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1¼" (32mm)', 'brand': 'Finolex', 'price': 80, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1¼" (32mm)', 'brand': 'Ashirvad', 'price': 90, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1½" (40mm)', 'brand': 'Kasta', 'price': 120, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1½" (40mm)', 'brand': 'Finolex', 'price': 100, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '1½" (40mm)', 'brand': 'Ashirvad', 'price': 110, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2" (50mm)', 'brand': 'Kasta', 'price': 150, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2" (50mm)', 'brand': 'Finolex', 'price': 125, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2" (50mm)', 'brand': 'Ashirvad', 'price': 140, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2½" (63mm)', 'brand': 'Kasta', 'price': 210, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2½" (63mm)', 'brand': 'Finolex', 'price': 180, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '2½" (63mm)', 'brand': 'Ashirvad', 'price': 200, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3" (75mm)', 'brand': 'Kasta', 'price': 265, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3" (75mm)', 'brand': 'Finolex', 'price': 230, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3" (75mm)', 'brand': 'Ashirvad', 'price': 250, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3½" (90mm)', 'brand': 'Kasta', 'price': 310, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3½" (90mm)', 'brand': 'Finolex', 'price': 280, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Pipes', 'name': '3½" (90mm)', 'brand': 'Ashirvad', 'price': 295, 'unit': 'meter'},
    
    # CPVC Fittings
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Elbow 90°', 'brand': 'Kasta', 'price': 8, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Elbow 90°', 'brand': 'Finolex', 'price': 6, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Elbow 90°', 'brand': 'Ashirvad', 'price': 7, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Tee', 'brand': 'Kasta', 'price': 10, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Tee', 'brand': 'Finolex', 'price': 8, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Tee', 'brand': 'Ashirvad', 'price': 9, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Coupler', 'brand': 'Kasta', 'price': 7, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Coupler', 'brand': 'Finolex', 'price': 6, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Coupler', 'brand': 'Ashirvad', 'price': 6.5, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Reducer', 'brand': 'Kasta', 'price': 12, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Reducer', 'brand': 'Finolex', 'price': 10, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Reducer', 'brand': 'Ashirvad', 'price': 11, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'End Cap', 'brand': 'Kasta', 'price': 6, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'End Cap', 'brand': 'Finolex', 'price': 5, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'End Cap', 'brand': 'Ashirvad', 'price': 5.5, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass FTA', 'brand': 'Kasta', 'price': 35, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass FTA', 'brand': 'Finolex', 'price': 30, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass FTA', 'brand': 'Ashirvad', 'price': 33, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass MTA', 'brand': 'Kasta', 'price': 30, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass MTA', 'brand': 'Finolex', 'price': 28, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Brass MTA', 'brand': 'Ashirvad', 'price': 29, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Union', 'brand': 'Kasta', 'price': 25, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Union', 'brand': 'Finolex', 'price': 22, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Union', 'brand': 'Ashirvad', 'price': 24, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Ball Valve', 'brand': 'Kasta', 'price': 70, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Ball Valve', 'brand': 'Finolex', 'price': 60, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Ball Valve', 'brand': 'Ashirvad', 'price': 65, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Pipe Clamp', 'brand': 'Kasta', 'price': 3, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Pipe Clamp', 'brand': 'Finolex', 'price': 2.5, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'CPVC Fittings', 'name': 'Pipe Clamp', 'brand': 'Ashirvad', 'price': 3, 'unit': 'piece'},
    
    # Fire Safety Plumbing
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Fire Hose Reel (30m)', 'brand': '', 'price': 3250, 'unit': 'reel'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Riser Pipe GI/CPVC 2"', 'brand': '', 'price': 180, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Hydrant Valve 63mm', 'brand': '', 'price': 4500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Sprinkler Head 68°C', 'brand': '', 'price': 350, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'CPVC Fire Pipe SDR 13.5', 'brand': '', 'price': 140, 'unit': 'meter'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Fire Water Tank (per litre)', 'brand': 'Sintex/HDPE', 'price': 8.5, 'unit': 'litre'},
    {'category': 'Plumbing', 'subcategory': 'Fire Safety Plumbing', 'name': 'Pressure Switch with Alarm', 'brand': '', 'price': 5750, 'unit': 'unit'},
    
    # Sanitary Fittings
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wall Hung WC', 'brand': 'Jaquar', 'price': 10500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wall Hung WC', 'brand': 'Jaquar Essco', 'price': 6300, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wall Hung WC', 'brand': 'Kohler', 'price': 15000, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wall Hung WC', 'brand': 'Hindware', 'price': 8200, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wash Basin', 'brand': 'Jaquar', 'price': 3500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wash Basin', 'brand': 'Essco', 'price': 2200, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wash Basin', 'brand': 'Kohler', 'price': 5000, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Wash Basin', 'brand': 'Hindware', 'price': 2800, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Single Lever Basin Mixer', 'brand': 'Jaquar', 'price': 3700, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Single Lever Basin Mixer', 'brand': 'Essco', 'price': 1900, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Single Lever Basin Mixer', 'brand': 'Kohler', 'price': 4800, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Single Lever Basin Mixer', 'brand': 'Hindware', 'price': 2500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Overhead Shower with Arm', 'brand': 'Jaquar', 'price': 2400, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Overhead Shower with Arm', 'brand': 'Essco', 'price': 1450, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Overhead Shower with Arm', 'brand': 'Kohler', 'price': 3200, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Overhead Shower with Arm', 'brand': 'Hindware', 'price': 1800, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Health Faucet', 'brand': 'Jaquar', 'price': 950, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Health Faucet', 'brand': 'Essco', 'price': 550, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Health Faucet', 'brand': 'Kohler', 'price': 1100, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Health Faucet', 'brand': 'Hindware', 'price': 700, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Concealed Flush Tank', 'brand': 'Jaquar', 'price': 6200, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Concealed Flush Tank', 'brand': 'Essco', 'price': 3300, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Concealed Flush Tank', 'brand': 'Kohler', 'price': 7500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Concealed Flush Tank', 'brand': 'Geberit', 'price': 8000, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Concealed Flush Tank', 'brand': 'Hindware', 'price': 4100, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Angle Valve', 'brand': 'Jaquar', 'price': 750, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Angle Valve', 'brand': 'Essco', 'price': 400, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Angle Valve', 'brand': 'Kohler', 'price': 850, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Angle Valve', 'brand': 'Hindware', 'price': 500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Bib Cock', 'brand': 'Jaquar', 'price': 800, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Bib Cock', 'brand': 'Essco', 'price': 500, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Bib Cock', 'brand': 'Kohler', 'price': 950, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Bib Cock', 'brand': 'Hindware', 'price': 600, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Diverter (2-inlet)', 'brand': 'Jaquar', 'price': 2800, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Diverter (2-inlet)', 'brand': 'Essco', 'price': 1600, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Diverter (2-inlet)', 'brand': 'Kohler', 'price': 3600, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Sanitary Fittings', 'name': 'Diverter (2-inlet)', 'brand': 'Hindware', 'price': 2000, 'unit': 'piece'},
    
    # Manhole & Inspection Chamber
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'Precast Concrete Ring 2-3ft', 'brand': '', 'price': 1150, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'Brickwork 9" (1m x 1m)', 'brand': '', 'price': 2000, 'unit': 'chamber'},
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'RCC Cover with Frame 18-24"', 'brand': '', 'price': 1175, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'CI Cover Heavy Duty', 'brand': '', 'price': 3150, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'Chamber Footrest Steps', 'brand': '', 'price': 200, 'unit': 'piece'},
    {'category': 'Plumbing', 'subcategory': 'Manhole & Inspection Chamber', 'name': 'HDPE Modular Manhole Kit', 'brand': '', 'price': 6000, 'unit': 'set'},
]

# Add plumbing data to Firebase
for item in plumbing_data:
    db.collection('materials').add(item)

print(f"✅ Added {len(plumbing_data)} plumbing items to Firebase!")
print("Plumbing category created with 6 subcategories")