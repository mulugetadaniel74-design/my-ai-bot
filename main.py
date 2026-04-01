import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# ለRender ሰርቨር ዝግጅት
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# ቁልፎችን ከRender Environment Variables እናነባለን
BOT_TOKEN = os.getenv("BOT_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! የ AI ቦትህ በስኬት ተጭኗል። ምን ልርዳህ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # ቦቱን በጀርባ እንዲሰራ ማድረግ
    threading.Thread(target=run_bot).start()
    # Render በሚሰጠን Port ላይ Flaskን ማስጀመር
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
