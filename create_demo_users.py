#!/usr/bin/env python3
"""
Create Demo Users in Firebase
"""

import os
import random
import string
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Get paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(CURRENT_DIR, 'firebase-credentials.json')

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    exit(1)

# Demo names - Expanded for 150+ users
first_names = [
    "Raj", "Priya", "Amit", "Sneha", "Rahul", "Pooja", "Arjun", "Kavya",
    "Vikram", "Ananya", "Rohan", "Neha", "Karan", "Ishita", "Aditya",
    "Riya", "Sanjay", "Diya", "Nikhil", "Shreya", "Akash", "Meera",
    "Varun", "Sakshi", "Manish", "Tanvi", "Kunal", "Ayesha", "Vishal",
    "Nisha", "Yash", "Kritika", "Mohit", "Shivani", "Aarav", "Sara",
    "Vivaan", "Aadhya", "Aryan", "Kiara", "Reyansh", "Advika", "Ayaan",
    "Navya", "Krishna", "Pari", "Shaurya", "Anvi", "Atharv", "Ira",
    "Vihaan", "Myra", "Aditya", "Saanvi", "Kabir", "Aarohi", "Dhruv",
    "Ahana", "Arnav", "Zara", "Rudra", "Mishti", "Shivansh", "Aanya",
    "Arjun", "Avni", "Aadhyan", "Pihu", "Advait", "Riya", "Veer",
    "Mira", "Dev", "Khushi", "Aarush", "Siya", "Kabir", "Ananya",
    "Reyansh", "Aadhya", "Lakshay", "Navya", "Om", "Tara"
]

last_names = [
    "Sharma", "Patel", "Singh", "Kumar", "Reddy", "Verma", "Gupta",
    "Yadav", "Joshi", "Mehta", "Shah", "Kapoor", "Malhotra", "Agarwal",
    "Chopra", "Nair", "Iyer", "Desai", "Rao", "Kulkarni", "Sinha",
    "Pandey", "Mishra", "Bhat", "Pillai", "Menon", "Das", "Ghosh",
    "Banerjee", "Chatterjee", "Roy", "Sengupta", "Mukherjee", "Bhatt",
    "Trivedi", "Shukla", "Tiwari", "Dubey", "Chauhan", "Rajput",
    "Thakur", "Saxena", "Jain", "Bhatia", "Arora", "Sethi", "Khanna",
    "Sood", "Bakshi", "Kohli"
]

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_random_user_id():
    """Generate realistic looking Telegram user ID"""
    return str(random.randint(100000000, 999999999))

def create_demo_users(count=25):
    print(f"\n🎯 Creating {count} demo users...\n")
    
    created = 0
    skipped = 0
    
    for i in range(count):
        # Generate random user details
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        full_name = f"{first_name} {last_name}"
        
        user_id = generate_random_user_id()
        
        # Check if user already exists
        user_ref = db.collection('users').document(user_id)
        if user_ref.get().exists:
            skipped += 1
            print(f"⏭️  Skipped: {user_id} (already exists)")
            continue
        
        # Generate random join date (last 30 days)
        days_ago = random.randint(1, 30)
        join_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Create demo user with all stats at 0
        demo_user = {
            "name": full_name,
            "email": "",
            "referral_code": generate_referral_code(),
            "referred_by": None,
            "total_clicks": 0,
            "total_earnings": 0.0,
            "daily_earnings": 0.0,
            "referral_count": 0,
            "referral_earnings": 0.0,
            "join_date": join_date,
            "last_click_date": None
        }
        
        # Save to Firebase
        user_ref.set(demo_user)
        created += 1
        print(f"✅ Created: {full_name} (ID: {user_id})")
    
    print(f"\n╔══════════════════════════════╗")
    print(f"   ✅ Demo Users Created!      ")
    print(f"╚══════════════════════════════╝")
    print(f"\n📊 Summary:")
    print(f"   Created: {created} users")
    print(f"   Skipped: {skipped} users")
    print(f"\n🎉 All done! Check Firebase Console or Admin Panel!")

if __name__ == "__main__":
    print("╔══════════════════════════════╗")
    print("   🎭 Demo User Generator      ")
    print("╚══════════════════════════════╝")
    
    # Create 150 demo users
    create_demo_users(150)
