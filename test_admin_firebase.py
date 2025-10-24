#!/usr/bin/env python3
"""
Quick test to verify admin panel can connect to Firebase
"""

import os
import firebase_admin
from firebase_admin import credentials, firestore

# Get paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(CURRENT_DIR, 'firebase-credentials.json')

print("╔══════════════════════════════╗")
print("   🧪 Testing Firebase Setup   ")
print("╚══════════════════════════════╝")
print()

# Check if credentials file exists
print(f"📁 Looking for: {FIREBASE_CREDS_PATH}")
if os.path.exists(FIREBASE_CREDS_PATH):
    print("✅ Credentials file found!")
else:
    print("❌ Credentials file NOT found!")
    print(f"   Expected location: {FIREBASE_CREDS_PATH}")
    exit(1)

print()

# Try to initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
    print()
    
    # Try to read users
    print("📊 Testing database access...")
    users_ref = db.collection('users')
    users = list(users_ref.stream())
    
    print(f"✅ Found {len(users)} users in database")
    print()
    
    if len(users) > 0:
        print("👥 Sample users:")
        for doc in users[:3]:  # Show first 3 users
            user_data = doc.to_dict()
            print(f"   - {doc.id}: {user_data.get('name', 'No name')}")
    
    print()
    print("╔══════════════════════════════╗")
    print("   ✅ ALL TESTS PASSED! 🎉    ")
    print("╚══════════════════════════════╝")
    print()
    print("Admin panel should work now!")
    
except Exception as e:
    print(f"❌ Firebase initialization failed!")
    print(f"   Error: {e}")
    print()
    print("Please check:")
    print("1. Firebase credentials file is correct")
    print("2. Firebase project is active")
    print("3. Internet connection is working")
