import os
import telebot
import google.generativeai as genai

# Token እና Key (ከ Render Environment Variables ይነበባሉ)
BOT_TOKEN = "8643065828:AAGaXS158SdOZJoLsJxrOpCs1iEsmup6XKM"
GEMINI_API_KEY = "AIzaSyBMv6RUQJQSYbpRxKdAXW9DzmhEJ1DdnNk"

# Gemini ማዘጋጃ
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

# የዳንኤል ታሪክ መመሪያ (System Instruction)
DANIEL_BIO = """
አንተ የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumesa) AI ነህ። 
ዳንኤል የ11ኛ ክፍል የማህበራዊ ሳይንስ ተማሪ ነው። 
ታሪኩ፦ በልጅነቱ በ50 ብር ለባርነት ተሽጧል፣ በረንዳ ላይ አድሯል፣ ጅብ ሊበላው ሲል ተርፏል። 
ይህ ሁሉ መከራ አልፎ ዛሬ ይህን AI ሰርቷል። 'ለምን ትኖራለህ?' የሚል መጽሐፍ እየጻፈ ነው። 
ሁልጊዜ ስትመልስ በታላቅ አክብሮት እና የሱን የጽናት ታሪክ በሚያሳይ መልኩ ይሁን።
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም! የዳንኤል AI ዝግጁ ነው። ማንኛውንም ጥያቄ ይጠይቁኝ።")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Gemini ምላሽ እንዲሰጥ ማድረግ
        full_prompt = f"{DANIEL_BIO}\n\nተጠቃሚው እንዲህ ይላል፦ {message.text}"
        response = model.generate_content(full_prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ ትንሽ መቆራረጥ ተፈጥሯል። እባክህ ድጋሚ ሞክር።")

if __name__ == "__main__":
    print("Gemini Bot እየሰራ ነው...")
    bot.infinity_polling()
    
