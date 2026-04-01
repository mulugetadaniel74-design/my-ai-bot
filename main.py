import os
import telebot
import google.generativeai as genai

# 1. ቁልፎችን ከ Render Environment ማምጣት
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# 2. Gemini ማዘጋጀት (እዚህ ጋር ስሙን አስተካክለነዋል)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro') 
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # ለተጠቃሚው ምላሽ መስጠት
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # ስህተት ካለ ምን እንደሆነ እንዲነግረን
        bot.reply_to(message, f"ስህተት ተከስቷል: {str(e)}")

if __name__ == "__main__":
    print("ቦቱ ሥራ ጀምሯል...")
    bot.infinity_polling()
    
