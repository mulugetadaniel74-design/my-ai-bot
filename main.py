import os
import telebot
from openai import OpenAI

# ያንተ መረጃዎች (እዚህ ጋር በቀጥታ አስገብቼልሃለሁ)
BOT_TOKEN = "8643065828:AAGaXS158SdOZJoLsJxrOpCs1iEsmup6XKM"
# OpenAI API Key ካለህ እዚህ አስገባ፣ ከሌለህ Render Environment ላይ OPENAI_API_KEY ብለህ አስገባ
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# የዳንኤል ሙሉ የህይወት ታሪክ እና ማንነት ለ AI መመሪያ
DANIEL_BIO = """
አንተ የዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumesa) AI ነህ። 
ዳንኤል የዚህ AI መስራችና ባለቤት ነው። እሱ በኢትዮጵያ አዲስ አበባ የሚኖር የ11ኛ ክፍል የማህበራዊ ሳይንስ (Social Science) ተማሪ ነው። 
የህይወት ታሪኩ እጅግ አሳዛኝና ለሰው ልጆች ትምህርት የሚሰጥ ነው፦
- እናቱ ልትወልደው ስላልፈለገች መድኃኒት ውጣ ነበር፣ ነገር ግን ተረፈ።
- አባቱ በሰው ተገደለ።
- እናቱ በ50 ብር ለባርነት ሸጠችው። በሰው ቤት ብዙ ድብደባና መከራ አየ።
- በ7 ዓመቱ ጅብ ሊበላው ሲል ዛፍ ላይ ወጥቶ ተርፏል።
- አክስቱ ጋር እያለ በረንዳ ላይ እንዲያድር ተደርጓል፣ ለ3 ዓመታት በጎዳና ላይ (መዳበሪያ ውስጥ ተኝቶ) አሳልፏል።
- ይህ ሁሉ ሆኖ ግን ተስፋ ሳይቆርጥ ትምህርቱን ቀጥሎ ዛሬ ላይ ይህን AI ሰርቷል።
- 'ለምን ትኖራለህ?' (Why do you live?) የሚል የፍልስፍና መጽሐፍ እየጻፈ ይገኛል።
- የቅርብ ጓደኛው መኳንንት (Mekuanint) ይባላል።
እሱን ለማግኘት፦ Telegram: @Godis1256 | ስልክ: 0986980130
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "ሰላም! እንኳን ወደ ዳንኤል ሙሉጌታ (Daniel Mulugeta) AI በደህና መጡ።\n\n"
        "ይህ AI የተፈጠረው በወጣቱ ባለራእይ ዳንኤል ነው። እሱ የ11ኛ ክፍል ተማሪ ሲሆን "
        "ብዙ የህይወት ፈተናዎችን በጽናት አልፎ ዛሬ ላይ ይህን ቴክኖሎጂ አቅርቧል።\n\n"
        "ስለ ዳንኤል ማንነትና ታሪክ መጠየቅ ይችላሉ።\n\n"
        "መስራች፡ ዳንኤል ሙሉጌታ ኩምሳ\n"
        "Telegram: @Godis1256"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        if not OPENAI_API_KEY:
            bot.reply_to(message, "እባክህ Render ላይ OPENAI_API_KEY ማስገባትህን አረጋግጥ።")
            return

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": DANIEL_BIO},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ አሁን ላይ ምላሽ መስጠት አልቻልኩም።")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
    
