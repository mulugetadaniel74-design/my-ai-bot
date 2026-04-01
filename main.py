import os
import telebot
import google.generativeai as genai

# ቁልፎችን ከ Environment ማምጣት
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini ማዘጋጀት
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        # ለተጠቃሚው ምላሽ መስጠት
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        # ስህተት ካለ በግልጽ እንዲነግረን
        bot.reply_to(message, f"ስህተት ተከስቷል: {str(e)}")

if __name__ == "__main__":
    print("ቦቱ እየተነሳ ነው...")
    bot.infinity_polling()

