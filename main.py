import os
import time
import telebot
import google.generativeai as genai
from flask import Flask
from threading import Thread

# 1. ለ Render "Web Service" እንዲሰራ Flask ማዘጋጀት
app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 2. ቦቱን ማዘጋጀት
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

SYSTEM_PROMPT = """
You are Daniel AI, a highly intelligent and fluent assistant powered by Google Gemini. 
You must speak Amharic and English perfectly.
Your creator is Daniel Mulugeta Kumesa, a Grade 11 Social Science student at Edget Chora.
Daniel is an author of three books: 'Why do you live?', 'I Fear No One', and 'Beyond the Chains'.
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.text}"
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁን መመለስ አልቻልኩም።")

# 3. Flask እና ቦቱን በአንድ ላይ ማስጀመር
def start_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Flaskን በሌላ መስመር (Thread) ማስጀመር
    t = Thread(target=run)
    t.start()
    # ቦቱን ማስጀመር
    start_bot()
    
