"""
EarnMaster Bot - Render Compatible Version
This file wraps the main bot with keep-alive functionality for 24/7 hosting
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import keep_alive first to start web server
from keep_alive import keep_alive

# Start the web server in background
print("🌐 Starting web server...")
keep_alive()
print("✅ Web server started on port 8080")

# Now import and run the main bot
print("🤖 Starting Telegram bot...")

# Import the main bot code
import telebot
from telebot import types
import json
import os
from datetime import datetime
import random
import string
import time
import threading
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Bot Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8425583035:AAFgItKbdTj_rpxQ4FUVID6gfMo2A79Duls")
DEVELOPER_CONTACT = "@noxlooters_0073"

# RichAds Configuration
SSP_ID = "975562"
PUBLISHER_ID = "975562"

# Bot Settings
MIN_WITHDRAWAL = 5000
AD_EARNING = 0.50
REFERRAL_BONUS_DISPLAY = 5999
REFERRAL_BONUS_ACTUAL = 2
MAX_DAILY_INCOME = 2000
AD_COOLDOWN = 15

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(CURRENT_DIR, 'firebase-credentials.json')

# Initialize Firebase
try:
    cred = credentials.Certificate(FIREBASE_CREDS_PATH)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
    USE_FIREBASE = True
except Exception as e:
    print(f"⚠️ Firebase initialization failed: {e}")
    print("📝 Using JSON file as fallback...")
    USE_FIREBASE = False
    db = None

bot = telebot.TeleBot(BOT_TOKEN)

# Track users watching ads
user_ad_timers = {}
user_ad_clicks = {}

# Production mode setting
PRODUCTION_MODE = True

# Function to get real ad from RichAds
def get_richad(telegram_id):
    if not PRODUCTION_MODE:
        return get_demo_ad()
    
    url = f"http://{SSP_ID}.xml.adx1.com/telegram-mb"
    data = {
        "language_code": "en",
        "publisher_id": PUBLISHER_ID,
        "telegram_id": telegram_id,
        "production": True
    }
    try:
        res = requests.post(url, json=data, timeout=10)
        if res.status_code == 200:
            response_data = res.json()
            if response_data and len(response_data) > 0:
                return response_data[0]
    except Exception as e:
        print(f"❌ RichAds Error: {e}")
    return None

def get_demo_ad():
    demo_ads = [
        {
            "title": "🎁 Special Offer - Limited Time!",
            "message": "Get amazing deals on premium products. Shop now and save big!",
            "image": "https://via.placeholder.com/800x400/FF6B6B/FFFFFF?text=Special+Offer",
            "link": "https://telegram.org",
            "button": "🛍️ Shop Now"
        },
        {
            "title": "💎 Premium Services Available",
            "message": "Upgrade your experience with our premium features. Try it today!",
            "image": "https://via.placeholder.com/800x400/4ECDC4/FFFFFF?text=Premium+Service",
            "link": "https://telegram.org",
            "button": "✨ Learn More"
        }
    ]
    return random.choice(demo_ads)

USER_DATA_FILE = "users_data.json"

def load_users_json():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users_json(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

users = load_users_json() if not USE_FIREBASE else {}

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def get_user_firebase(user_id):
    user_ref = db.collection('users').document(str(user_id))
    user_doc = user_ref.get()
    
    if user_doc.exists:
        return user_doc.to_dict()
    else:
        new_user = {
            "name": "",
            "email": "",
            "referral_code": generate_referral_code(),
            "referred_by": None,
            "total_clicks": 0,
            "total_earnings": 0,
            "daily_earnings": 0,
            "referral_count": 0,
            "referral_earnings": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_click_date": None
        }
        user_ref.set(new_user)
        return new_user

def save_user_firebase(user_id, user_data):
    user_ref = db.collection('users').document(str(user_id))
    user_ref.set(user_data, merge=True)

def get_all_users_firebase():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    return {doc.id: doc.to_dict() for doc in docs}

def get_user_json(user_id):
    user_id = str(user_id)
    if user_id not in users:
        users[user_id] = {
            "name": "",
            "email": "",
            "referral_code": generate_referral_code(),
            "referred_by": None,
            "total_clicks": 0,
            "total_earnings": 0,
            "daily_earnings": 0,
            "referral_count": 0,
            "referral_earnings": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_click_date": None
        }
        save_users_json(users)
    return users[user_id]

def save_user_json(user_id, user_data):
    users[str(user_id)] = user_data
    save_users_json(users)

def get_user(user_id):
    if USE_FIREBASE:
        return get_user_firebase(user_id)
    else:
        return get_user_json(user_id)

def save_user(user_id, user_data):
    if USE_FIREBASE:
        save_user_firebase(user_id, user_data)
    else:
        save_user_json(user_id, user_data)

def get_all_users():
    if USE_FIREBASE:
        return get_all_users_firebase()
    else:
        return users

def get_total_users_count():
    try:
        if USE_FIREBASE:
            users_ref = db.collection('users')
            users_count = len(list(users_ref.stream()))
            return users_count
        else:
            return len(users)
    except:
        return 0

def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📺 WATCH ADS")
    btn2 = types.KeyboardButton("👤 PROFILE")
    btn3 = types.KeyboardButton("💸 WITHDRAWAL")
    btn4 = types.KeyboardButton("🎁 REFERRAL")
    btn5 = types.KeyboardButton("🆘 SUPPORT")
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    if not user.get("name") or user["name"] == "":
        telegram_name = message.from_user.first_name
        if message.from_user.last_name:
            telegram_name += " " + message.from_user.last_name
        user["name"] = telegram_name
        save_user(user_id, user)
    
    if message.text.startswith('/start '):
        referral_code = message.text.split()[1]
        if user["referred_by"] is None:
            all_users = get_all_users()
            
            for uid, udata in all_users.items():
                if udata["referral_code"] == referral_code and uid != user_id:
                    user["referred_by"] = referral_code
                    save_user(user_id, user)
                    referrer = get_user(uid)
                    referrer["referral_count"] += 1
                    referrer["referral_earnings"] += REFERRAL_BONUS_ACTUAL
                    referrer["total_earnings"] += REFERRAL_BONUS_ACTUAL
                    save_user(uid, referrer)
                    bot.send_message(uid, f"🎉 New referral! You earned ₹{REFERRAL_BONUS_ACTUAL}!")
                    break
    
    total_users = get_total_users_count()
    
    welcome_text = f"""╔══════════════════════╗
   💰 EARNMASTER BOT 💰
╚══════════════════════╝

👥 Total Users: {total_users:,}
👋 Welcome {message.from_user.first_name}!

🎯 Your Personal Money Making Assistant

━━━━━━━━━━━━━━━━━━━━━━
💎 EARNING OPPORTUNITIES
━━━━━━━━━━━━━━━━━━━━━━

📺 Watch Ads → ₹{AD_EARNING} per ad
👥 Refer Friends → ₹{REFERRAL_BONUS_DISPLAY} bonus
💰 Daily Limit → Up to ₹{MAX_DAILY_INCOME}

━━━━━━━━━━━━━━━━━━━━━━
⚡ INSTANT FEATURES
━━━━━━━━━━━━━━━━━━━━━━

✅ Real-time earnings tracking
✅ Multiple withdrawal methods
✅ 24/7 support available
✅ Unlimited referral potential

🚀 Start earning NOW! Choose an option below 👇"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "👤 PROFILE")
def profile(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    profile_text = f"""╔══════════════════════╗
      👤 YOUR PROFILE
╚══════════════════════╝

📝 Name: {user['name'] if user['name'] else 'Not set'}
📧 Email: {user['email'] if user['email'] else 'Not set'}
🔑 Referral Code: `{user['referral_code']}`

━━━━━━━━━━━━━━━━━━━━━━
💰 EARNINGS DASHBOARD
━━━━━━━━━━━━━━━━━━━━━━

💎 Total Balance: ₹{user['total_earnings']:.2f}
📅 Today's Earning: ₹{user['daily_earnings']:.2f}
📺 Total Ads Watched: {user['total_clicks']}
👥 Total Referrals: {user['referral_count']}
🎁 Referral Earnings: ₹{user['referral_earnings']:.2f}

━━━━━━━━━━━━━━━━━━━━━━
📆 Member Since: {user['join_date'].split()[0]}

💡 Keep watching ads & referring friends!"""
    
    markup = types.InlineKeyboardMarkup()
    btn_update = types.InlineKeyboardButton("✏️ Update Profile", callback_data="update_profile")
    markup.add(btn_update)
    
    bot.send_message(message.chat.id, profile_text, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💸 WITHDRAWAL")
def withdrawal(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    if user['total_earnings'] >= MIN_WITHDRAWAL:
        withdrawal_text = f"""╔══════════════════════╗
   💸 WITHDRAWAL CENTER
╚══════════════════════╝

💰 Your Balance: ₹{user['total_earnings']:.2f}
💵 Minimum Required: ₹{MIN_WITHDRAWAL}

━━━━━━━━━━━━━━━━━━━━━━
✅ ELIGIBLE FOR WITHDRAWAL!
━━━━━━━━━━━━━━━━━━━━━━

Choose your payment method:"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_upi = types.InlineKeyboardButton("📱 UPI", callback_data="withdraw_upi")
        btn_bank = types.InlineKeyboardButton("🏦 Bank", callback_data="withdraw_bank")
        btn_paytm = types.InlineKeyboardButton("💳 Paytm", callback_data="withdraw_paytm")
        markup.add(btn_upi, btn_bank)
        markup.add(btn_paytm)
    else:
        remaining = MIN_WITHDRAWAL - user['total_earnings']
        withdrawal_text = f"""╔══════════════════════╗
   💸 WITHDRAWAL CENTER
╚══════════════════════╝

💰 Current Balance: ₹{user['total_earnings']:.2f}
💵 Minimum Required: ₹{MIN_WITHDRAWAL}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ INSUFFICIENT BALANCE
━━━━━━━━━━━━━━━━━━━━━━

You need ₹{remaining:.2f} more!

📺 Watch more ads to earn
🎁 Refer friends for bonus

━━━━━━━━━━━━━━━━━━━━━━
🚨 EMERGENCY WITHDRAWAL?
━━━━━━━━━━━━━━━━━━━━━━

Need urgent payment?
Contact developer for instant approval!

Developer: {DEVELOPER_CONTACT}"""
        
        markup = types.InlineKeyboardMarkup()
        btn_contact = types.InlineKeyboardButton("📞 Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT.replace('@', '')}")
        markup.add(btn_contact)
    
    bot.send_message(message.chat.id, withdrawal_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🎁 REFERRAL")
def referral(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    bot_username = bot.get_me().username
    referral_link = f"https://t.me/{bot_username}?start={user['referral_code']}"
    
    referral_text = f"""╔══════════════════════╗
    🎁 REFERRAL PROGRAM
╚══════════════════════╝

🔑 Your Referral Code:
{user['referral_code']}

🔗 Your Referral Link:
{referral_link}

━━━━━━━━━━━━━━━━━━━━━━
💰 EARN BIG REWARDS!
━━━━━━━━━━━━━━━━━━━━━━

🎉 Referral Bonus: ₹{REFERRAL_BONUS_DISPLAY}

━━━━━━━━━━━━━━━━━━━━━━
📊 YOUR REFERRAL STATS
━━━━━━━━━━━━━━━━━━━━━━

👥 Total Referrals: {user['referral_count']}
💎 Referral Earnings: ₹{user['referral_earnings']:.2f}

━━━━━━━━━━━━━━━━━━━━━━
🚀 HOW IT WORKS
━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Share your link with friends
2️⃣ They join using your link
3️⃣ You get instant bonus!

💡 More friends = More money!"""
    
    markup = types.InlineKeyboardMarkup()
    btn_share = types.InlineKeyboardButton("📤 Share Link", 
                                          url=f"https://t.me/share/url?url={referral_link}&text=Join EarnMaster Bot and start earning money! 💰")
    btn_copy = types.InlineKeyboardButton("📋 Copy Link", callback_data=f"copy_link_{user['referral_code']}")
    markup.add(btn_share)
    markup.add(btn_copy)
    
    bot.send_message(message.chat.id, referral_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "📺 WATCH ADS")
def watch_ads(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    if user_id in user_ad_clicks:
        bot.send_message(message.chat.id, 
                        "⚠️ You already have an active ad!\n\n"
                        "Please complete the current ad first.")
        return
    
    if user_id in user_ad_timers:
        remaining = AD_COOLDOWN - (time.time() - user_ad_timers[user_id])
        if remaining > 0:
            bot.send_message(message.chat.id, 
                           f"⏳ Please wait {int(remaining)} seconds before watching the next ad!")
            return
    
    today = datetime.now().strftime("%Y-%m-%d")
    if user['last_click_date'] != today:
        user['daily_earnings'] = 0
        user['last_click_date'] = today
    
    if user['daily_earnings'] >= MAX_DAILY_INCOME:
        bot.send_message(message.chat.id, 
                        f"🎉 Daily limit reached!\n\n"
                        f"You've earned ₹{MAX_DAILY_INCOME} today.\n"
                        f"Come back tomorrow for more! 💰")
        return
    
    loading_msg = bot.send_message(message.chat.id, "⏳ Loading ad...")
    ad = get_richad(message.chat.id)
    
    try:
        bot.delete_message(message.chat.id, loading_msg.message_id)
    except:
        pass
    
    if not ad:
        bot.send_message(message.chat.id, 
                        "⚠️ No ads available right now.\n\n"
                        "Please try again in a few moments!")
        return
    
    ad_caption = f"""╔══════════════════════╗
      📺 SPONSORED AD
╚══════════════════════╝

🔥 {ad['title']}

{ad['message']}

━━━━━━━━━━━━━━━━━━━━━━
💰 EARN: ₹{AD_EARNING}
━━━━━━━━━━━━━━━━━━━━━━

👇 Click the button below to view offer!"""
    
    markup = types.InlineKeyboardMarkup()
    btn_ad = types.InlineKeyboardButton(
        text="✨ " + ad.get("button", "Learn More"), 
        url=ad["link"]
    )
    markup.add(btn_ad)
    
    try:
        msg = bot.send_photo(
            message.chat.id, 
            ad["image"], 
            caption=ad_caption, 
            reply_markup=markup
        )
    except:
        msg = bot.send_message(message.chat.id, ad_caption, reply_markup=markup)
    
    instruction_text = "👇 **Click the button above to view offer!**\n⏱️ Timer will start automatically..."
    instruction_msg = bot.send_message(message.chat.id, instruction_text, parse_mode="Markdown")
    
    user_ad_clicks[user_id] = {
        'msg_id': msg.message_id,
        'chat_id': message.chat.id,
        'ad': ad,
        'instruction_msg_id': instruction_msg.message_id,
        'timer_started': False,
        'user': user
    }
    
    def auto_start_timer():
        time.sleep(5)
        
        if user_id not in user_ad_clicks:
            return
        
        try:
            bot.delete_message(message.chat.id, instruction_msg.message_id)
        except:
            pass
        
        timer_text = "⏱️ **Timer: 15 seconds remaining...**"
        timer_msg = bot.send_message(message.chat.id, timer_text, parse_mode="Markdown")
        
        user_ad_clicks[user_id]['timer_msg_id'] = timer_msg.message_id
        user_ad_clicks[user_id]['timer_started'] = True
        
        for remaining in range(14, 0, -1):
            time.sleep(1)
            
            if user_id not in user_ad_clicks:
                return
            
            try:
                countdown_text = f"⏱️ **Timer: {remaining} seconds remaining...**"
                bot.edit_message_text(
                    countdown_text,
                    message.chat.id,
                    timer_msg.message_id,
                    parse_mode="Markdown"
                )
            except:
                pass
        
        time.sleep(1)
        
        try:
            bot.edit_message_text(
                "✅ **Timer Complete! Claiming reward...**",
                message.chat.id,
                timer_msg.message_id,
                parse_mode="Markdown"
            )
        except:
            pass
        
        time.sleep(1)
        
        if user_id not in user_ad_clicks:
            return
        
        user['total_clicks'] += 1
        user['total_earnings'] += AD_EARNING
        user['daily_earnings'] += AD_EARNING
        save_user(user_id, user)
        
        ad_info = user_ad_clicks[user_id]
        new_markup = types.InlineKeyboardMarkup()
        btn_claimed = types.InlineKeyboardButton("✅ Claimed!", callback_data="ad_claimed")
        new_markup.add(btn_claimed)
        
        try:
            bot.edit_message_reply_markup(ad_info['chat_id'], ad_info['msg_id'], reply_markup=new_markup)
        except:
            pass
        
        try:
            bot.delete_message(message.chat.id, timer_msg.message_id)
        except:
            pass
        
        if user_id in user_ad_clicks:
            del user_ad_clicks[user_id]
        
        user_ad_timers[user_id] = time.time()
        
        reward_text = f"""╔══════════════════════╗
     ✅ AD COMPLETED!
╚══════════════════════╝

🎉 Congratulations!

💰 You earned: ₹{AD_EARNING}
💎 Total Balance: ₹{user['total_earnings']:.2f}
📅 Today's Earning: ₹{user['daily_earnings']:.2f}

━━━━━━━━━━━━━━━━━━━━━━

⏱️ Next ad available in {AD_COOLDOWN} seconds!

🚀 Keep watching to earn more!"""
        
        bot.send_message(message.chat.id, reward_text)
        
        time.sleep(AD_COOLDOWN)
        if user['daily_earnings'] < MAX_DAILY_INCOME:
            auto_ad_text = f"""🔔 NEW AD AVAILABLE!

💰 Ready to earn another ₹{AD_EARNING}?

Click "📺 WATCH ADS" to continue earning! 🚀"""
            bot.send_message(message.chat.id, auto_ad_text)
    
    threading.Thread(target=auto_start_timer, daemon=True).start()

@bot.message_handler(func=lambda message: message.text == "🆘 SUPPORT")
def help_support(message):
    help_text = f"""╔══════════════════════╗
    🆘 HELP & SUPPORT
╚══════════════════════╝

Need assistance? We're here! 💪

━━━━━━━━━━━━━━━━━━━━━━
📋 COMMON QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━

❓ How do I earn?
📺 Watch ads (₹{AD_EARNING} per ad)
🎁 Refer friends (₹{REFERRAL_BONUS_DISPLAY} bonus)
💰 Daily limit: ₹{MAX_DAILY_INCOME}

❓ When can I withdraw?
💵 Minimum: ₹{MIN_WITHDRAWAL}
🚨 Emergency? Contact developer

❓ How do referrals work?
🔗 Share your unique link
💎 Earn bonus per referral
♾️ No limit on referrals!

━━━━━━━━━━━━━━━━━━━━━━
📞 NEED HELP?
━━━━━━━━━━━━━━━━━━━━━━

Developer: {DEVELOPER_CONTACT}
Response: Quick & Real-time
Available: 24/7

💬 Click below for urgent support:"""
    
    markup = types.InlineKeyboardMarkup()
    btn_contact = types.InlineKeyboardButton("📞 Contact Developer", url=f"https://t.me/{DEVELOPER_CONTACT.replace('@', '')}")
    markup.add(btn_contact)
    
    bot.send_message(message.chat.id, help_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.from_user.id)
    user = get_user(user_id)
    
    if call.data == "update_profile":
        bot.send_message(call.message.chat.id, 
                        "✏️ To update your profile, send:\n\n"
                        "Name: Your Name\n"
                        "Email: your.email@example.com")
        bot.answer_callback_query(call.id)
    
    elif call.data.startswith("withdraw_"):
        method = call.data.replace("withdraw_", "").upper()
        bot.send_message(call.message.chat.id, 
                        f"💸 Withdrawal via {method}\n\n"
                        f"Please provide your {method} details:")
        bot.answer_callback_query(call.id, "Processing withdrawal request...")
    
    elif call.data.startswith("copy_link_"):
        code = call.data.replace("copy_link_", "")
        bot_username = bot.get_me().username
        link = f"https://t.me/{bot_username}?start={code}"
        bot.answer_callback_query(call.id, f"Link: {link}", show_alert=True)
    
    elif call.data == "ad_claimed":
        bot.answer_callback_query(call.id, "✅ Reward already claimed!")

@bot.message_handler(func=lambda message: "Name:" in message.text and "Email:" in message.text)
def update_profile_handler(message):
    user_id = str(message.from_user.id)
    user = get_user(user_id)
    
    try:
        lines = message.text.split('\n')
        name = lines[0].split('Name:')[1].strip()
        email = lines[1].split('Email:')[1].strip()
        
        user['name'] = name
        user['email'] = email
        save_user(user_id, user)
        
        bot.send_message(message.chat.id, "✅ Profile updated successfully!", reply_markup=main_menu_keyboard())
    except:
        bot.send_message(message.chat.id, "❌ Invalid format. Please try again.", reply_markup=main_menu_keyboard())

print("╔══════════════════════════════╗")
print("   🤖 EARNMASTER BOT STARTED   ")
print("╚══════════════════════════════╝")
print("")
print("✅ Bot is online and ready!")
print("💰 Users can now earn money!")
print("📺 Watch Ads feature active")
print("🎁 Referral system enabled")
print("")
print("Press Ctrl+C to stop the bot")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

# Run bot with polling
bot.infinity_polling()
