#!/usr/bin/env python3
"""
Admin Panel Backend - Flask Server
Provides API endpoints for admin panel
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import telebot
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Bot Token
BOT_TOKEN = "8425583035:AAFgItKbdTj_rpxQ4FUVID6gfMo2A79Duls"
bot = telebot.TeleBot(BOT_TOKEN)

# Get the directory of this file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(CURRENT_DIR, 'firebase-credentials.json')
USERS_JSON_PATH = os.path.join(CURRENT_DIR, 'users_data.json')
WITHDRAWALS_JSON_PATH = os.path.join(CURRENT_DIR, 'withdrawals.json')

# Initialize Firebase
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(FIREBASE_CREDS_PATH)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    USE_FIREBASE = True
    print("✅ Firebase initialized for admin panel")
    print(f"📁 Credentials loaded from: {FIREBASE_CREDS_PATH}")
except Exception as e:
    print(f"⚠️ Firebase not available: {e}")
    print(f"📁 Looking for credentials at: {FIREBASE_CREDS_PATH}")
    USE_FIREBASE = False
    db = None

# Admin credentials
ADMIN_USERNAME = "Jay"
ADMIN_PASSWORD = "Jayhacker_123455"

@app.route('/')
def index():
    """Serve login page"""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """Serve dashboard page"""
    return render_template('dashboard.html')

@app.route('/users')
def users():
    """Serve users page"""
    return render_template('users.html')

@app.route('/withdrawals')
def withdrawals():
    """Serve withdrawals page"""
    return render_template('withdrawals.html')

@app.route('/broadcast')
def broadcast():
    """Serve broadcast page"""
    return render_template('broadcast.html')

@app.route('/api/login', methods=['POST'])
def login():
    """Admin login"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        if USE_FIREBASE:
            # Get all users
            users_ref = db.collection('users')
            users = list(users_ref.stream())
            
            total_users = len(users)
            total_earnings = sum(doc.to_dict().get('total_earnings', 0) for doc in users)
            total_clicks = sum(doc.to_dict().get('total_clicks', 0) for doc in users)
            
            # Get pending withdrawals
            withdrawals_ref = db.collection('withdrawals').where('status', '==', 'pending')
            pending_withdrawals = len(list(withdrawals_ref.stream()))
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_users': total_users,
                    'total_earnings': round(total_earnings, 2),
                    'total_clicks': total_clicks,
                    'pending_withdrawals': pending_withdrawals
                }
            })
        else:
            # JSON fallback
            import json
            users = {}
            if os.path.exists(USERS_JSON_PATH):
                with open(USERS_JSON_PATH, 'r') as f:
                    users = json.load(f)
            
            total_users = len(users)
            total_earnings = sum(u.get('total_earnings', 0) for u in users.values())
            total_clicks = sum(u.get('total_clicks', 0) for u in users.values())
            
            withdrawals = {}
            if os.path.exists(WITHDRAWALS_JSON_PATH):
                with open(WITHDRAWALS_JSON_PATH, 'r') as f:
                    withdrawals = json.load(f)
            
            pending_withdrawals = sum(1 for w in withdrawals.values() if w.get('status') == 'pending')
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_users': total_users,
                    'total_earnings': round(total_earnings, 2),
                    'total_clicks': total_clicks,
                    'pending_withdrawals': pending_withdrawals
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        if USE_FIREBASE:
            users_ref = db.collection('users')
            docs = users_ref.stream()
            
            users_list = []
            for doc in docs:
                user_data = doc.to_dict()
                user_data['id'] = doc.id
                users_list.append(user_data)
            
            return jsonify({'success': True, 'users': users_list})
        else:
            # JSON fallback
            import json
            users = {}
            if os.path.exists(USERS_JSON_PATH):
                with open(USERS_JSON_PATH, 'r') as f:
                    users = json.load(f)
            
            users_list = []
            for user_id, user_data in users.items():
                user_data['id'] = user_id
                users_list.append(user_data)
            
            return jsonify({'success': True, 'users': users_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/withdrawals', methods=['GET'])
def get_withdrawals():
    """Get all withdrawal requests"""
    try:
        if USE_FIREBASE:
            withdrawals_ref = db.collection('withdrawals')
            docs = withdrawals_ref.stream()
            
            withdrawals_list = []
            for doc in docs:
                withdrawal_data = doc.to_dict()
                withdrawal_data['id'] = doc.id
                withdrawals_list.append(withdrawal_data)
            
            # Sort by requested_at (newest first)
            withdrawals_list.sort(key=lambda x: x.get('requested_at', ''), reverse=True)
            
            return jsonify({'success': True, 'withdrawals': withdrawals_list})
        else:
            # JSON fallback
            import json
            withdrawals = {}
            if os.path.exists(WITHDRAWALS_JSON_PATH):
                with open(WITHDRAWALS_JSON_PATH, 'r') as f:
                    withdrawals = json.load(f)
            
            withdrawals_list = []
            for withdrawal_id, withdrawal_data in withdrawals.items():
                withdrawal_data['id'] = withdrawal_id
                withdrawals_list.append(withdrawal_data)
            
            # Sort by requested_at (newest first)
            withdrawals_list.sort(key=lambda x: x.get('requested_at', ''), reverse=True)
            
            return jsonify({'success': True, 'withdrawals': withdrawals_list})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/withdrawal/update', methods=['POST'])
def update_withdrawal():
    """Update withdrawal status"""
    try:
        data = request.json
        withdrawal_id = data.get('withdrawal_id')
        status = data.get('status')  # 'approved' or 'rejected'
        
        if USE_FIREBASE:
            withdrawal_ref = db.collection('withdrawals').document(withdrawal_id)
            withdrawal_doc = withdrawal_ref.get()
            
            if not withdrawal_doc.exists:
                return jsonify({'success': False, 'message': 'Withdrawal not found'}), 404
            
            withdrawal_data = withdrawal_doc.to_dict()
            user_id = withdrawal_data['user_id']
            amount = withdrawal_data['amount']
            
            # Update withdrawal status
            withdrawal_ref.update({
                'status': status,
                'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Notify user
            if status == 'approved':
                message = f"✅ Withdrawal Approved!\n\n💰 Amount: ₹{amount}\n\nYour payment has been processed successfully!"
            else:
                message = f"❌ Withdrawal Rejected\n\n💰 Amount: ₹{amount}\n\nPlease contact support for more information."
            
            try:
                bot.send_message(user_id, message)
            except:
                pass
            
            return jsonify({'success': True, 'message': f'Withdrawal {status}'})
        else:
            # JSON fallback
            import json
            withdrawals = {}
            if os.path.exists(WITHDRAWALS_JSON_PATH):
                with open(WITHDRAWALS_JSON_PATH, 'r') as f:
                    withdrawals = json.load(f)
            
            if withdrawal_id not in withdrawals:
                return jsonify({'success': False, 'message': 'Withdrawal not found'}), 404
            
            withdrawal_data = withdrawals[withdrawal_id]
            user_id = withdrawal_data['user_id']
            amount = withdrawal_data['amount']
            
            # Update withdrawal status
            withdrawals[withdrawal_id]['status'] = status
            withdrawals[withdrawal_id]['processed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(WITHDRAWALS_JSON_PATH, 'w') as f:
                json.dump(withdrawals, f, indent=4)
            
            # Notify user
            if status == 'approved':
                message = f"✅ Withdrawal Approved!\n\n💰 Amount: ₹{amount}\n\nYour payment has been processed successfully!"
            else:
                message = f"❌ Withdrawal Rejected\n\n💰 Amount: ₹{amount}\n\nPlease contact support for more information."
            
            try:
                bot.send_message(user_id, message)
            except:
                pass
            
            return jsonify({'success': True, 'message': f'Withdrawal {status}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/broadcast', methods=['POST'])
def broadcast_message():
    """Send broadcast message to all users"""
    try:
        data = request.json
        message = data.get('message')
        
        if not message:
            return jsonify({'success': False, 'message': 'Message is required'}), 400
        
        # Get all users
        if USE_FIREBASE:
            users_ref = db.collection('users')
            docs = users_ref.stream()
            user_ids = [doc.id for doc in docs]
        else:
            import json
            users = {}
            if os.path.exists('users_data.json'):
                with open('users_data.json', 'r') as f:
                    users = json.load(f)
            user_ids = list(users.keys())
        
        # Send message to all users
        success_count = 0
        failed_count = 0
        
        for user_id in user_ids:
            try:
                bot.send_message(user_id, message)
                success_count += 1
            except:
                failed_count += 1
        
        # Save broadcast record
        if USE_FIREBASE:
            broadcast_ref = db.collection('broadcasts').document()
            broadcast_ref.set({
                'message': message,
                'sent_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_users': len(user_ids),
                'success_count': success_count,
                'failed_count': failed_count
            })
        
        return jsonify({
            'success': True,
            'message': 'Broadcast sent',
            'stats': {
                'total': len(user_ids),
                'success': success_count,
                'failed': failed_count
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("╔══════════════════════════════╗")
    print("   🔥 ADMIN PANEL STARTED 🔥   ")
    print("╚══════════════════════════════╝")
    print("")
    print("✅ Server running on: http://localhost:5000")
    print("🔐 Default credentials:")
    print(f"   Username: {ADMIN_USERNAME}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print("")
    print("⚠️  CHANGE DEFAULT PASSWORD IN admin_panel.py!")
    print("")
    app.run(debug=True, host='0.0.0.0', port=5000)
