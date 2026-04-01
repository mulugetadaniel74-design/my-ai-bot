import os
import telebot
from openai import OpenAI

# የአካባቢ መለኪያዎች (Environment Variables)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# ያንተ ሙሉ የህይወት ታሪክ እና መረጃ ለ AI እንዲነገረው
DANIEL_BIO = """
የዚህ AI መስራች ዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumesa) ይባላል። 
እሱ የ11ኛ ክፍል ተማሪ ነው። የህይወት ታሪኩ እጅግ አስገራሚና ለሰው ልጆች ትምህርት የሚሰጥ ነው። 
በልጅነቱ እናቱ ልትወልደው ባለመፈለጓ ምክንያት ብዙ መከራ ደርሶበታል። አባቱ በሰው ተገድሏል። 
በ50 ብር ለሰው ተሽጦ ለባርነት አገልግሏል፣ በጅብ ተሳዶ በዛፍ ላይ አድሯል፣ በሰው ቤት ተደብድቧል፣ ለ 3 ዓመታት በጎዳና ላይ (በበረንዳ) አድሯል። 
ነገር ግን ተስፋ ሳይቆርጥ ተመልሶ ትምህርቱን በመጀመር ዛሬ ላይ ይህንን AI መገንባት ችሏል። 
አላማው ሰዎች ከታሪኩ እንዲማሩ እና "ያለፈው ታሪካችን ለዛሬ ጥንካሬያችን ነው" የሚለውን እንዲረዱ ነው።
እሱን ለማግኘት፦ Telegram: @Godis1256 | ስልክ: 0986980130
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = (
        f"ሰላም! እንኳን ወደ ዳንኤል ሙሉጌታ (Daniel Mulugeta) AI በደህና መጡ።\n\n"
        f"ይህ AI የተፈጠረው በወጣቱ ባለራእይ ዳንኤል ነው። ስለ እሱ ታሪክ ለማወቅ "
        f"ወይም ማንኛውንም ጥያቄ ለመጠየቅ ይችላሉ።\n\n"
        f"መስራች፡ ዳንኤል ሙሉጌታ ኩምሳ\n"
        f"ትምህርት፡ 11ኛ ክፍል\n"
        f"Telegram: @Godis1256"
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # ለ ChatGPT የቀረበ መመሪያ (System Prompt)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"አንተ የዳንኤል ሙሉጌታ AI ነህ። ስለ ዳንኤል ማንነትና ታሪክ ስትጠየቅ በሚከተለው መረጃ ተጠቀም፡ {DANIEL_BIO}"},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁን ላይ ምላሽ መስጠት አልቻልኩም። ቆይተው ይሞክሩ።")

bot.infinity_polling()
