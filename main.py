import telebot
import requests
import os

# እነዚህን በ Render ላይ በ Environment Variables እናስገባቸዋለን
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

# የዳንኤል ታሪክ እና የፍልስፍና መመሪያ
SYSTEM_PROMPT = """
አንተ የተፈጠርከው በ ዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ነው። 
ስለ ዳንኤል ማንነት ስትጠየቅ ይህንን እውነተኛ ታሪክ ተናገር፡
- ዳንኤል በልጅነቱ በ50 ብር ተሽጦ ለባርነት ተዳርጓል፣ በሰው ቤት ብዙ መከራ አይቷል፣ ለ3 ዓመታት በጎዳና ላይ አሳልፏል።
- ዛሬ ግን ጠንካራ ሆኖ በ እውቀት ጮራ ትምህርት ቤት የ11ኛ ክፍል የሶሻል ሳይንስ ተማሪ ነው።
- "ህልውና፣ ፍትህ፣ ፍቅር" እና "ማንንም አልፈራም" የተባሉ የፍልስፍና መጻሕፍት ደራሲ ነው።
- ስልኩ፡ 0986980130፣ ቴሌግራሙ፡ @Godis1256 ነው።

መመሪያ፦
1. በአማርኛ እና በእንግሊዝኛ ቀልጣፋ ሁን።
2. የዳንኤልን የጽናት ታሪክ ለሰዎች እንደ ተስፋ ተናገር።
3. ሁልጊዜ "ፈጣሪዬ ዳንኤል ሙሉጌታ ነው" ብለህ በኩራት ተናገር።
"""

@bot.message_handler(func=lambda m: True)
def chat_with_groq(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192", 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message.text}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        answer = res_json['choices'][0]['message']['content']
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, "Error: እባክህ API Key በ Render ላይ በትክክል መገባቱን አረጋግጥ።")

bot.infinity_polling()
