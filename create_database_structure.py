import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Clear existing materials
materials = db.collection('materials').stream()
for material in materials:
    material.reference.delete()

# RCC Data
rcc_data = [
    # Sand, Aggregate, Brick - blank rates for admin input
    {'category': 'RCC', 'subcategory': 'Sand', 'name': 'Standard Sand', 'brand': '', 'price': 0, 'unit': 'cft'},
    {'category': 'RCC', 'subcategory': 'Aggregate', 'name': 'Standard Aggregate', 'brand': '', 'price': 0, 'unit': 'cft'},
    {'category': 'RCC', 'subcategory': 'Brick', 'name': 'Standard Brick', 'brand': '', 'price': 0, 'unit': 'piece'},
    
    # Cement brands
    {'category': 'RCC', 'subcategory': 'Cement', 'name': 'Cement', 'brand': 'UltraTech', 'price': 360, 'unit': 'bag'},
    {'category': 'RCC', 'subcategory': 'Cement', 'name': 'Cement', 'brand': 'Birla', 'price': 320, 'unit': 'bag'},
    {'category': 'RCC', 'subcategory': 'Cement', 'name': 'Cement', 'brand': 'JK', 'price': 320, 'unit': 'bag'},
    
    # Steel brands
    {'category': 'RCC', 'subcategory': 'Steel', 'name': 'Steel', 'brand': 'Tata', 'price': 65, 'unit': 'kg'},
    {'category': 'RCC', 'subcategory': 'Steel', 'name': 'Steel', 'brand': 'Moyra', 'price': 63, 'unit': 'kg'},
    {'category': 'RCC', 'subcategory': 'Steel', 'name': 'Steel', 'brand': 'Ikon', 'price': 63, 'unit': 'kg'},
]

# Electrical Data
electrical_data = [
    # MS Box
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '2-module', 'brand': '', 'price': 25, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '3-module', 'brand': '', 'price': 30, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '4-module', 'brand': '', 'price': 38, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '6-module', 'brand': '', 'price': 55, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '8-module', 'brand': '', 'price': 63, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'MS.Box', 'name': '12-module', 'brand': '', 'price': 71, 'unit': 'piece'},
    
    # Electrical Conduit
    {'category': 'Electrical', 'subcategory': 'Electrical Conduit', 'name': '1-inch H.M.S', 'brand': 'Precision', 'price': 72, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Electrical Conduit', 'name': '1-inch H.M.S', 'brand': 'Polycab', 'price': 74, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Electrical Conduit', 'name': '1-inch M.M.S', 'brand': 'Precision', 'price': 56, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Electrical Conduit', 'name': '1-inch M.M.S', 'brand': 'Polycab', 'price': 58, 'unit': 'piece'},
    
    # Wire (per 100mm bundle)
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '0.75mm', 'brand': 'KEI', 'price': 1077, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '0.75mm', 'brand': 'Polycab', 'price': 1126, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '1.00mm', 'brand': 'KEI', 'price': 1389, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '1.00mm', 'brand': 'Polycab', 'price': 1436, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '1.5mm', 'brand': 'KEI', 'price': 2064, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '1.5mm', 'brand': 'Polycab', 'price': 2064, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '2.5mm', 'brand': 'KEI', 'price': 3310, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '2.5mm', 'brand': 'Polycab', 'price': 3398, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '4.0mm', 'brand': 'KEI', 'price': 4913, 'unit': '100mm bundle'},
    {'category': 'Electrical', 'subcategory': 'Wire', 'name': '4.0mm', 'brand': 'Polycab', 'price': 5216, 'unit': '100mm bundle'},
    
    # Switches & Sockets - L&T variants
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Basic Switch', 'brand': 'L&T Engem', 'price': 30, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Basic Switch', 'brand': 'L&T Entice', 'price': 60, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Basic Switch', 'brand': 'L&T Englaze', 'price': 90, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Fan Regulator (2-module)', 'brand': 'L&T Engem', 'price': 383, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Fan Regulator (2-module)', 'brand': 'L&T Entice', 'price': 696, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'Fan Regulator (2-module)', 'brand': 'L&T Englaze', 'price': 765, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'USB Socket', 'brand': 'L&T Engem', 'price': 824, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'USB Socket', 'brand': 'L&T Entice', 'price': 1243, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'USB Socket', 'brand': 'L&T Englaze', 'price': 1369, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'USB Type-C Socket', 'brand': 'L&T Entice', 'price': 1700, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'USB Type-C Socket', 'brand': 'L&T Englaze', 'price': 1809, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Power Switch', 'brand': 'L&T Engem', 'price': 108, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Power Switch', 'brand': 'L&T Entice', 'price': 191, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Power Switch', 'brand': 'L&T Englaze', 'price': 245, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '6A Socket', 'brand': 'L&T Engem', 'price': 97, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '6A Socket', 'brand': 'L&T Entice', 'price': 142, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '6A Socket', 'brand': 'L&T Englaze', 'price': 196, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Socket', 'brand': 'L&T Engem', 'price': 156, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Socket', 'brand': 'L&T Entice', 'price': 311, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': '16A Socket', 'brand': 'L&T Englaze', 'price': 323, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'CAT-6 Jack', 'brand': 'L&T Engem', 'price': 498, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'CAT-6 Jack', 'brand': 'L&T Entice', 'price': 723, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switches&Sockets', 'name': 'CAT-6 Jack', 'brand': 'L&T Englaze', 'price': 736, 'unit': 'piece'},
    
    # Switch Plates
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '2-module', 'brand': 'L&T Engem', 'price': 80, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '2-module', 'brand': 'L&T Entice', 'price': 150, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '2-module', 'brand': 'L&T Englaze', 'price': 173, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '3-module', 'brand': 'L&T Engem', 'price': 104, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '3-module', 'brand': 'L&T Entice', 'price': 194, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '3-module', 'brand': 'L&T Englaze', 'price': 201, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '4-module', 'brand': 'L&T Engem', 'price': 122, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '4-module', 'brand': 'L&T Entice', 'price': 222, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '4-module', 'brand': 'L&T Englaze', 'price': 230, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '6-module', 'brand': 'L&T Engem', 'price': 180, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '6-module', 'brand': 'L&T Entice', 'price': 300, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '6-module', 'brand': 'L&T Englaze', 'price': 356, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '8-module', 'brand': 'L&T Engem', 'price': 213, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '8-module', 'brand': 'L&T Entice', 'price': 353, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '8-module', 'brand': 'L&T Englaze', 'price': 423, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '12-module', 'brand': 'L&T Engem', 'price': 288, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '12-module', 'brand': 'L&T Entice', 'price': 479, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Switch Plate', 'name': '12-module', 'brand': 'L&T Englaze', 'price': 570, 'unit': 'piece'},
    
    # Downlights
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '12W', 'brand': 'Jaguar', 'price': 645, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '12W', 'brand': 'Phillips', 'price': 689, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '12W', 'brand': 'Orient', 'price': 345, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '15W', 'brand': 'Jaguar', 'price': 719, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '15W', 'brand': 'Phillips', 'price': 749, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Downlights', 'name': '15W', 'brand': 'Orient', 'price': 399, 'unit': 'piece'},
    
    # Fans
    {'category': 'Electrical', 'subcategory': 'Fans', 'name': '48-inch', 'brand': 'Crompton', 'price': 2679, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Fans', 'name': '48-inch', 'brand': 'Havells', 'price': 2129, 'unit': 'piece'},
    {'category': 'Electrical', 'subcategory': 'Fans', 'name': '48-inch', 'brand': 'Orient', 'price': 1499, 'unit': 'piece'},
]

# Fall Ceiling Data
fall_ceiling_data = [
    # Interior
    {'category': 'Fall Ceiling', 'subcategory': 'Interior', 'name': 'PVC', 'brand': '', 'price': 200, 'unit': 'sq ft'},
    {'category': 'Fall Ceiling', 'subcategory': 'Interior', 'name': 'WPC', 'brand': '', 'price': 220, 'unit': 'sq ft'},
    {'category': 'Fall Ceiling', 'subcategory': 'Interior', 'name': 'Gypsum', 'brand': '', 'price': 110, 'unit': 'sq ft'},
    {'category': 'Fall Ceiling', 'subcategory': 'Interior', 'name': 'Cement Board', 'brand': '', 'price': 110, 'unit': 'sq ft'},
    
    # Exterior
    {'category': 'Fall Ceiling', 'subcategory': 'Exterior', 'name': 'Cement Board', 'brand': '', 'price': 110, 'unit': 'sq ft'},
    {'category': 'Fall Ceiling', 'subcategory': 'Exterior', 'name': 'ACP', 'brand': '', 'price': 150, 'unit': 'sq ft'},
    {'category': 'Fall Ceiling', 'subcategory': 'Exterior', 'name': 'HPL', 'brand': '', 'price': 550, 'unit': 'sq ft'},
]

# Add all data to Firebase
all_data = rcc_data + electrical_data + fall_ceiling_data

for item in all_data:
    db.collection('materials').add(item)

print(f"✅ Added {len(all_data)} items to Firebase database!")
print("Categories created: RCC, Electrical, Fall Ceiling")