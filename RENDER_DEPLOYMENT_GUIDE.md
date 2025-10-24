# 🚀 Render Deployment Guide - EarnMaster Bot

## Complete Step-by-Step Instructions for 24/7 Hosting

---

## 📋 Prerequisites

Before deploying, make sure you have:

1. ✅ A GitHub account
2. ✅ A Render account (free) - Sign up at https://render.com
3. ✅ Your Telegram Bot Token
4. ✅ Firebase credentials file (if using Firebase)

---

## 🔧 Step 1: Prepare Your Repository

### 1.1 Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - EarnMaster Bot for Render deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANT:** Make sure `firebase-credentials.json` is in `.gitignore` and NOT pushed to GitHub!

---

## 🌐 Step 2: Deploy on Render

### 2.1 Create New Web Service

1. Go to https://render.com/dashboard
2. Click **"New +"** button
3. Select **"Web Service"**
4. Connect your GitHub repository
5. Select the repository you just pushed

### 2.2 Configure Web Service

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `earnmaster-bot` (or any name you prefer) |
| **Region** | `Oregon (US West)` or closest to you |
| **Branch** | `main` |
| **Root Directory** | `tapearntap_bot` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot.py` |
| **Instance Type** | `Free` |

### 2.3 Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `BOT_TOKEN` | Your bot token from BotFather | **Required** |
| `PYTHON_VERSION` | `3.11.0` | Optional |

**To add environment variables:**
1. Scroll to "Environment Variables" section
2. Click "Add Environment Variable"
3. Enter Key and Value
4. Click "Save"

### 2.4 Deploy!

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Watch the logs for any errors

---

## 🔥 Step 3: Handle Firebase (Optional but Recommended)

If you're using Firebase for data storage:

### Option A: Upload via Render Dashboard (Recommended)

1. After deployment, go to your service dashboard
2. Click **"Shell"** tab on the left
3. Use file upload feature to upload `firebase-credentials.json`
4. Place it in the correct directory

### Option B: Use Environment Variable

Convert your Firebase credentials to a single-line JSON string and add as environment variable:

```bash
# Minify your firebase-credentials.json
cat firebase-credentials.json | jq -c '.' > firebase-creds-minified.json
```

Then add environment variable:
- Key: `FIREBASE_CREDENTIALS`
- Value: (paste the minified JSON)

Update your `bot.py` to read from environment:

```python
import os
import json

# Try to load from environment first
firebase_creds = os.environ.get('FIREBASE_CREDENTIALS')
if firebase_creds:
    cred = credentials.Certificate(json.loads(firebase_creds))
else:
    cred = credentials.Certificate(FIREBASE_CREDS_PATH)
```

---

## ✅ Step 4: Verify Deployment

### 4.1 Check Logs

In Render dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. You should see:
   ```
   ✅ Web server started on port 8080
   🤖 Starting Telegram bot...
   ✅ Bot is online and ready!
   ```

### 4.2 Test Your Bot

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Bot should respond immediately

### 4.3 Check Health Endpoint

Visit your Render URL + `/health`:
```
https://your-service-name.onrender.com/health
```

Should return: `{"status": "healthy", "bot": "online"}`

---

## 🎯 Step 5: Keep Bot Running 24/7

### Important Notes:

**Free Tier Limitations:**
- Render free tier services **spin down after 15 minutes of inactivity**
- When inactive, the bot will stop responding
- It automatically wakes up when the health endpoint is accessed

**Solutions:**

### Option 1: Upgrade to Paid Plan ($7/month)
- Guaranteed 24/7 uptime
- No spin-down
- Better performance

### Option 2: Use External Monitoring (Free)
Use a service like UptimeRobot to ping your bot every 14 minutes:

1. Go to https://uptimerobot.com
2. Create free account
3. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://your-service-name.onrender.com/health`
   - Interval: 5 minutes
4. Save

**Note:** Even with UptimeRobot, there may be brief downtime during spin-up.

### Option 3: Combine Multiple Free Services
Deploy on multiple platforms and use one as backup:
- Render (Primary)
- Railway (Backup)
- Fly.io (Backup)

---

## 🔧 Troubleshooting

### Bot Not Starting?

**Check 1: Verify BOT_TOKEN**
- Go to Render dashboard > Environment Variables
- Make sure BOT_TOKEN is set correctly
- No extra spaces or quotes

**Check 2: Check Logs**
```bash
# In Render dashboard, go to Logs tab
# Look for error messages
```

**Check 3: Firebase Issues**
```
⚠️ Firebase initialization failed
```
Solution: Upload firebase-credentials.json to the service

### Bot Stops Responding?

**Cause 1: Free tier spin-down**
Solution: Use UptimeRobot or upgrade to paid plan

**Cause 2: Out of memory**
Solution: Optimize code or upgrade plan

### Polling Issues?

If you see timeout errors:
```python
# In bot.py, adjust polling parameters
bot.infinity_polling(timeout=60, long_polling_timeout=60)
```

---

## 🎨 Optional Enhancements

### Add Custom Domain

1. In Render dashboard, go to your service
2. Click "Settings"
3. Scroll to "Custom Domain"
4. Add your domain
5. Update DNS records as shown

### Enable Auto-Deploy

Already enabled by default! When you push to GitHub, Render automatically redeploys.

### Set Up Notifications

1. Go to Render account settings
2. Enable email notifications for:
   - Deploy failures
   - Service down alerts

---

## 📊 Monitoring Your Bot

### Check User Count
Your bot automatically tracks total users in the welcome message.

### View Logs
```bash
# In Render dashboard > Logs
# Filter by:
- "Error" for issues
- "✅" for successful operations
- "Firebase" for database operations
```

### Database Status
If using Firebase:
1. Go to Firebase Console
2. Check Firestore database
3. Monitor user collection

---

## 💰 Cost Breakdown

### Free Tier (Current Setup)
- ✅ $0/month
- ⚠️ Spins down after 15 min inactivity
- ✅ 750 hours/month free
- ✅ Good for testing/low traffic

### Starter Tier ($7/month)
- ✅ True 24/7 uptime
- ✅ No spin-down
- ✅ Better performance
- ✅ Recommended for production

---

## 🚨 Important Reminders

1. **Never commit sensitive files:**
   - ❌ firebase-credentials.json
   - ❌ serviceAccountKey.json
   - ❌ .env files with tokens

2. **Use environment variables for:**
   - ✅ BOT_TOKEN
   - ✅ API keys
   - ✅ Database credentials

3. **Monitor your bot:**
   - Check logs regularly
   - Set up UptimeRobot
   - Monitor Firebase usage

4. **Backup your data:**
   - Export Firebase data regularly
   - Keep local copies of user data
   - Document your bot configuration

---

## 📞 Need Help?

### Resources:
- 📚 Render Docs: https://render.com/docs
- 💬 Render Community: https://community.render.com
- 🐛 GitHub Issues: Create an issue in your repo
- 📧 Developer: @noxlooters_0073

---

## ✨ Success Checklist

Before going live, verify:

- [ ] Bot responds to /start command
- [ ] Firebase connected (if using)
- [ ] Watch Ads feature works
- [ ] Referral system works
- [ ] Profile displays correctly
- [ ] Withdrawal requests are saved
- [ ] Web server shows "Online & Running"
- [ ] Health endpoint returns 200 OK
- [ ] UptimeRobot monitor is active (optional)
- [ ] No sensitive data in GitHub repo

---

## 🎉 You're Done!

Your EarnMaster Bot is now running 24/7 on Render!

**Next Steps:**
1. Share your bot link
2. Monitor performance
3. Add more features
4. Scale as you grow

**Bot URL:** https://t.me/YOUR_BOT_USERNAME

---

**Deployed with ❤️ on Render**
