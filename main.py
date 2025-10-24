import requests
import telebot

BOT_TOKEN = "8400260942:AAHDpBo3UtWTkEm7AzpQkG0h_Z9df8wgi2A"
SSP_ID = "975562"
PUBLISHER_ID = "975562"

bot = telebot.TeleBot(BOT_TOKEN)

def get_ad(telegram_id):
    url = f"http://{SSP_ID}.xml.adx1.com/telegram-mb"
    data = {
        "language_code": "en",
        "publisher_id": PUBLISHER_ID,
        "telegram_id": telegram_id,
        "production": False
    }
    try:
        res = requests.post(url, json=data)
        if res.status_code == 200 and res.json():
            return res.json()[0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ad: {e}")
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to TapEarnTap Bot!\nUse /ad to view ads.")

@bot.message_handler(commands=['ad'])
def show_ad(message):
    ad = get_ad(message.chat.id)
    if ad:
        caption = f"🔥 {ad['title']}\n\n{ad['message']}"
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text=ad.get("button", "View Offer"), url=ad["link"]))
        bot.send_photo(message.chat.id, ad["image"], caption=caption, reply_markup=markup)
        bot.send_message(message.chat.id, "✅ Ad delivered!")
    else:
        bot.send_message(message.chat.id, "⚠️ No ads available right now. Please try again later.")

print("Welcome to TapEarnTap Bot 💸")
print("Type /ad to get a sponsored message!")
bot.polling()
