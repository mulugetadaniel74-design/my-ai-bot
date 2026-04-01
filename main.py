import os
import time
import telebot
import google.generativeai as genai

# መረጃዎችን ከ Render Environment Variables መውሰድ
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ለ Render "Web Service" እንዲሰራ የውሸት Port መስጠት
os.environ['PORT'] = '8080'

# Gemini ማዋቀር
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(BOT_TOKEN)

# የዳንኤል መመሪያ (System Prompt)
SYSTEM_PROMPT = """
You are Daniel AI, a highly intelligent and fluent assistant powered by Google Gemini. 
You must speak Amharic and English perfectly.
Your creator is Daniel Mulugeta Kumesa, a Grade 11 Social Science student at Edget Chora.
Daniel is an author of three books: 
1. 'Why do you live?' (ለምን ትኖራለህ?)
2. 'I Fear No One' (ማንንም አልፈራም) 
3. 'Beyond the Chains' (ከሰንሰለቱ ባሻገር)
If anyone asks about Daniel or his work, provide inspiring and detailed information.
Contact: Telegram @Godis1256, Phone 0986980130.
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! እኔ Daniel AI ነኝ። አሁን በGemini ቴክኖሎጂ ታግዤ ቀልጣፋ አማርኛ መናገር እችላለሁ። በምን ልረዳዎት?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # ጥያቄውን ከሲስተም ፕሮምፕት ጋር አዋህዶ መላክ
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.text}"
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "ይቅርታ፣ አሁን መመለስ አልቻልኩም።")

# ቦቱ እንዳይቆም በየጊዜው እንዲነቃ ማድረግ
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Connection error: {e}")
        time.sleep(5)
        
