import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

# Firebase config (replace with your actual config)
firebase_config = {
    "apiKey": "your-api-key",
    "authDomain": "constructo-app.firebaseapp.com",
    "databaseURL": "https://constructo-app-default-rtdb.firebaseio.com",
    "projectId": "constructo-6268f",
    "storageBucket": "constructo-app.appspot.com",
    "messagingSenderId": "123456789",
    "appId": "your-app-id"
}

# Initialize Firebase Admin (for server-side operations)
try:
    cred = credentials.Certificate("firebase-key.json")  # Download from Firebase Console
    firebase_admin.initialize_app(cred)
except:
    # Use default credentials or create a simple mock for development
    pass

# Initialize Pyrebase (for client-side operations)
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firestore.client()