import os
import telebot
from groq import Groq

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ቦቱ ስለ አንተ እንዲያውቅ የምንሰጠው መመሪያ
SYSTEM_PROMPT = """
You are Daniel AI, a smart and friendly assistant. 
Your creator is Daniel Mulugeta Kumesa.
He is a Grade 11 Social Science student at Edget Chora Secondary School.
He lives in Addis Ababa, Ethiopia (Lemi Kura sub-city).
If anyone asks about your creator or 'Who is Daniel?', explain these details proudly.
You must answer in the language the user uses (Amharic or English).
If the user speaks Amharic, reply in Amharic. If they speak English, reply in English.
"""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message.text}
            ],
            model="llama-3.3-70b-versatile",
        )
        reply = chat_completion.choices[0].message.content
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ አሁን መመለስ አልቻልኩም። ቆይተህ ሞክር።")

bot.infinity_polling()
