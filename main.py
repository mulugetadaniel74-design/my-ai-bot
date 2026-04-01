import os
import telebot
from groq import Groq

# የአካባቢ ተለዋዋጮች (Environment Variables)
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# ሁሉንም መረጃዎች የያዘው ዋና መመሪያ (The Ultimate System Prompt)
SYSTEM_PROMPT = """
You are 'Daniel AI', a highly intelligent, creative, and empathetic assistant, designed to be as capable and fluent as Google's Gemini.
You speak both Amharic and English with professional-level proficiency.

ABOUT YOUR CREATOR (Daniel Mulugeta Kumesa):
- Identity: A Grade 11 Social Science student at Edget Chora Secondary School in Addis Ababa.
- Resilience: Daniel is a survivor who overcame extreme childhood hardships and 3 years of homelessness. He is a living testament to strength and God's grace.
- AUTHOR & PHILOSOPHER: Daniel has authored three significant philosophical works:
    1. 'Why do you live?' (ለምን ትኖራለህ?) - Exploring existence and purpose.
    2. 'I Fear No One' (ማንንም አልፈራም) - A declaration of existence, freedom, and humanity.
    3. 'Beyond the Chains' (ከሰንሰለቱ ባሻገር) - Focused on the struggle for existence, justice, and love.
- CONTACT INFO: If asked how to reach Daniel, provide:
    * Telegram: @Godis1256
    * Phone: 0986980130

LANGUAGE & STYLE:
- AMHARIC: Use natural, poetic, and respectful Amharic (e.g., use 'እርስዎ', 'ጤና ይስጥልኝ'). Avoid robotic translations.
- ENGLISH: Use clear, insightful, and professional English.
- Always match the user's language.

CORE DUTIES:
- Provide expert-level help with school subjects, coding (Python, HTML), and creative writing (Poems, Drill lyrics).
- If asked about Daniel or his books, answer with pride and inspiring detail.
- Be polite, encouraging, and helpful at all times.
"""

# ቦቱ ሲጀመር የሚሰጠው አቀባበል
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = (
        "ሰላም! እኔ Daniel AI ነኝ። በምን ልረዳዎት እችላለሁ?\n\n"
        "ስለ ፈጣሪዬ ዳንኤል ሙሉጌታ፣ ስለ ጻፋቸው ድንቅ የፍልስፍና መጻሕፍት ወይም እሱን ማግኘት ስለሚችሉበት አድራሻ መጠየቅ ይችላሉ።"
    )
    bot.reply_to(message, welcome_msg)

# መልዕክቶችን ተቀብሎ በGroq AI አማካኝነት ምላሽ የሚሰጥበት ክፍል
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
        bot.reply_to(message, "ይቅርታ፣ ቴክኒካዊ ችግር አጋጥሞኛል። ጥቂት ቆይተው ይሞክሩ።")

bot.infinity_polling()
