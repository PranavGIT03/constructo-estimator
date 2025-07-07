import firebase_admin
from firebase_admin import credentials, firestore

def check_firebase():
    try:
        # Try to initialize Firebase
        if not firebase_admin._apps:
            # Try with service account key
            try:
                cred = credentials.Certificate("firebase-key.json")
                firebase_admin.initialize_app(cred)
                print("✅ Firebase initialized with service account key")
            except FileNotFoundError:
                print("❌ firebase-key.json not found")
                # Try with default credentials
                try:
                    firebase_admin.initialize_app()
                    print("✅ Firebase initialized with default credentials")
                except Exception as e:
                    print(f"❌ Firebase initialization failed: {e}")
                    return False
        
        # Test Firestore connection
        db = firestore.client()
        
        # Try to write test data
        test_ref = db.collection('test').document('connection')
        test_ref.set({'status': 'connected', 'timestamp': firestore.SERVER_TIMESTAMP})
        print("✅ Firestore write test successful")
        
        # Try to read test data
        doc = test_ref.get()
        if doc.exists:
            print("✅ Firestore read test successful")
            print(f"   Data: {doc.to_dict()}")
        
        # Clean up test data
        test_ref.delete()
        print("✅ Firestore delete test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Checking Firebase connection...")
    if check_firebase():
        print("\n🎉 Firebase is properly configured!")
    else:
        print("\n⚠️  Firebase not configured - using mock database")