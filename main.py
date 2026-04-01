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
    # Render በየጊዜው Port 10000 ላይ ጥያቄ ይልካል፣ እሱን እንዲመልስ ማድረግ
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

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
Always be philosophical and helpful.
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.text}"
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        # API Key ስህተት ካለ እዚህ ጋር ይናገራል
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ አሁን መመለስ አልቻልኩም። እባክህ Render ላይ GEMINI_API_KEY በትክክል መጻፉን አረጋግጥ።")

# 3. Flask እና ቦቱን በአንድ ላይ ማስጀመር
if __name__ == "__main__":
    # Flaskን በሌላ መስመር (Thread) ማስጀመር
    t = Thread(target=run)
    t.start()
    # ቦቱን ማስጀመር
    print("Bot is starting...")
    bot.infinity_polling()
        
