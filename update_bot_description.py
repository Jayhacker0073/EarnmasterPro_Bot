#!/usr/bin/env python3
"""
Update Bot Description with Total Users Count
"""

import os
import telebot
import firebase_admin
from firebase_admin import credentials, firestore

BOT_TOKEN = "8425583035:AAFgItKbdTj_rpxQ4FUVID6gfMo2A79Duls"

# Get paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(CURRENT_DIR, 'firebase-credentials.json')

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    USE_FIREBASE = True
    print("✅ Firebase initialized successfully!")
except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
    USE_FIREBASE = False
    db = None

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

def get_total_users():
    """Get total users count"""
    try:
        if USE_FIREBASE:
            users_ref = db.collection('users')
            users_count = len(list(users_ref.stream()))
            return users_count
        else:
            return 0
    except:
        return 0

def update_bot_description():
    """Update bot description with total users"""
    try:
        total_users = get_total_users()
        
        # New description with user count
        description = f"""💰 EarnMaster Pro - Your Money Making Assistant

👥 {total_users:,} Active Users
📺 Watch Ads & Earn Real Money
🎁 Refer Friends & Get Bonuses
💸 Instant Withdrawals

Join thousands of users earning daily!"""
        
        # Update bot description
        bot.set_my_description(description)
        
        print(f"\n✅ Bot description updated!")
        print(f"👥 Total Users: {total_users:,}")
        print(f"\n📝 New Description:")
        print("━" * 50)
        print(description)
        print("━" * 50)
        
        # Also update short description
        short_description = f"💰 Earn money by watching ads! 👥 {total_users:,} users earning daily"
        bot.set_my_short_description(short_description)
        
        print(f"\n✅ Short description updated!")
        print(f"📝 {short_description}")
        
    except Exception as e:
        print(f"❌ Failed to update description: {e}")
        print("\n⚠️ Alternative: Use BotFather manually")
        print("Send to @BotFather:")
        print("/setdescription")
        print("Then paste:")
        print(f"\n💰 EarnMaster Pro - Your Money Making Assistant\n\n👥 {total_users:,} Active Users\n📺 Watch Ads & Earn Real Money\n🎁 Refer Friends & Get Bonuses\n💸 Instant Withdrawals\n\nJoin thousands of users earning daily!")

if __name__ == "__main__":
    print("╔══════════════════════════════╗")
    print("   📝 Bot Description Updater   ")
    print("╚══════════════════════════════╝")
    print()
    
    update_bot_description()
    
    print("\n╔══════════════════════════════╗")
    print("   ✅ Done!                     ")
    print("╚══════════════════════════════╝")
    print("\n📱 Check your bot profile in Telegram!")
    print("🔄 Run this script regularly to update user count")
