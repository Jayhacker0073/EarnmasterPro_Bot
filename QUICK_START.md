# ⚡ Quick Start - Deploy to Render in 5 Minutes

## 🚀 Super Fast Deployment Guide

---

## Step 1: Push to GitHub (2 minutes)

```bash
git init
git add .
git commit -m "Deploy EarnMaster Bot"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Step 2: Deploy on Render (2 minutes)

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Fill in:
   - **Name:** `earnmaster-bot`
   - **Root Directory:** `tapearntap_bot`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

---

## Step 3: Add Bot Token (1 minute)

1. Click **"Advanced"**
2. Add Environment Variable:
   - **Key:** `BOT_TOKEN`
   - **Value:** `YOUR_BOT_TOKEN_FROM_BOTFATHER`
3. Click **"Create Web Service"**

---

## Step 4: Wait & Test

⏳ Wait 3-5 minutes for deployment

✅ Open Telegram and test your bot with `/start`

---

## 🎯 That's It!

Your bot is now live 24/7!

For detailed instructions, see: `RENDER_DEPLOYMENT_GUIDE.md`

---

## ⚠️ Important Notes

**Free Tier:** Bot spins down after 15 min of inactivity

**Solution:** Use UptimeRobot.com to ping your bot every 5 minutes (free)

**URL to ping:** `https://your-service-name.onrender.com/health`

---

## 🔥 Firebase Setup (Optional)

If using Firebase, after deployment:

1. Go to Render dashboard → Your service
2. Click **"Shell"** tab
3. Upload `firebase-credentials.json` to the root directory

---

## ✅ Verify Everything Works

Test these commands in Telegram:
- `/start` - Welcome message
- `👤 PROFILE` - View profile
- `📺 WATCH ADS` - Load an ad
- `🎁 REFERRAL` - Get referral link
- `🆘 SUPPORT` - Support info

---

## 📞 Issues?

Check logs in Render dashboard → Logs tab

Common fixes:
- **Bot not responding:** Check BOT_TOKEN is correct
- **Firebase error:** Upload firebase-credentials.json
- **Import errors:** Check requirements.txt

---

**Happy Deploying! 🚀**
