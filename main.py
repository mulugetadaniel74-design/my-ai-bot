import os
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. ለ Render ድረ-ገጽ መስሎ እንዲታይ Flask ማዘጋጀት
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    # Render በየጊዜው Port 10000 ላይ ጥያቄ ይልካል
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# 2. ቦቱን ማዘጋጀት
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = "You are Daniel AI, powered by Gemini. Creator: Daniel Mulugeta Kumesa."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {message.text}")
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ የ Gemini ቁልፍ (API Key) ላይ ስህተት አለ።")

# 3. Flask እና ቦቱን በአንድ ላይ ማስጀመር
if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()

