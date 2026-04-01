import os
import telebot
import google.generativeai as genai

# የእርስዎ ቁልፎች
BOT_TOKEN = "8643065828:AAGaXS158SdOZJoLsJxrOpCs1iEsmup6XKM"
GEMINI_KEY = "AIzaSyBMv6RUQJQSYbpRxKdAXW9DzmhEJ1DdnNk"

# Gemini ማዘጋጃ
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም ዳንኤል! የGemini AI ቦትህ አሁን ዝግጁ ነው።")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ ስህተት ተፈጥሯል። ድጋሚ ይሞክሩ።")

if __name__ == "__main__":
    bot.infinity_polling()
    
