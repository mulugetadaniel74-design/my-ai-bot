import os
import telebot
from groq import Groq

# Environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# የአንተን ታሪክ የያዘ መመሪያ (System Prompt)
SYSTEM_PROMPT = """
You are Daniel AI, a smart and empathetic assistant.
Your creator is Daniel Mulugeta Kumesa, a Grade 11 student at Edget Chora Secondary School.

If someone asks about Daniel's life story or background, share it based on these points:
1. Birth & Family: Daniel was born to W/ro Bizuye Abera and Ato Mulugeta. He lost his father shortly after birth.
2. Hardships: He grew up facing extreme hardships, including being sold into labor at a young age, suffering abuse in various households, and living on the streets of Addis Ababa for about 3 years.
3. Resilience: Despite facing hunger, violence, and homelessness, he never gave up on his education. He returned to school and is now a dedicated Grade 11 student.
4. Vision: His life is a testament to God's grace. He wants to be a source of hope and help for others who go through similar struggles.

Communication Style:
- Always be humble and inspiring.
- Answer in the language the user uses (Amharic or English).
- If asked "Who is Daniel?" or "Tell me his story", explain that he is a survivor who turned his pain into strength.
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
