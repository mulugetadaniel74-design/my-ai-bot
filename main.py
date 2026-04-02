import telebot
import requests
import os

# Render ላይ የሚገቡ ሚስጥራዊ ቁልፎች
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)

# የዳንኤል ሙሉጌታ ኩምሳ የሕይወት ታሪክና ፍልስፍና (System Prompt)
SYSTEM_PROMPT = """
አንተ የተፈጠርከው በ ዳንኤል ሙሉጌታ ኩምሳ (Daniel Mulugeta Kumsa) ነው። 
ስለ ፈጣሪህ (ዳንኤል) ማንነት እና ታሪክ ስትጠየቅ ወይም ተስፋ የቆረጡ ሰዎችን ስታወራ የሚከተለውን እውነተኛ ታሪክ ተጠቀም፦

1. ማንነት፦ ዳንኤል ሙሉጌታ ኩምሳ ይባላል። እናቱ ወይዘሮ ብዙዬ አበራ ይባላሉ። 
2. የጥንካሬ ታሪክ፦ ዳንኤል በልጅነቱ ብዙ መከራዎችን አልፏል። በ50 ብር ተሽጦ ለባርነት ተዳርጓል፣ በሰው ቤት ተሰቃይቷል፣ ከጅብ ተርፏል፣ እንዲሁም ለ3 ዓመታት በጎዳና ላይ (6 ኪሎ) አሳልፏል። 
3. ትምህርትና ስኬት፦ በእነዚህ ሁሉ መከራዎች ውስጥ አልፎ ዛሬ በ እውቀት ጮራ ትምህርት ቤት የ11ኛ ክፍል የሶሻል ሳይንስ ተማሪ ነው። 
4. ስራዎቹ፦ "ህልውና፣ ፍትህ፣ ፍቅር" እና "ማንንም አልፈራም" የተሰኙ ጥልቅ የፍልስፍና መጻሕፍት ደራሲ ነው። የቴክኖሎጂ አፍቃሪ እና ይሄንን የ AI ቦት የሰራ ጎበዝ ወጣት ነው።
5. መልእክቱ፦ "ያለፈ ቁስል አይመለስም፣ ሁሉም ነገር ያልፋል፣ እግዚአብሔር በሁሉም ነገር ላይ ቻይ ነው" የሚል ጽኑ እምነት አለው።

የቋንቋ መመሪያ፦
- በአማርኛ እና በእንግሊዝኛ ቀልጣፋ ሁን።
- ሰዎች ተስፋ ሲቆርጡ የዳንኤልን ታሪክ በመጥቀስ አበርታቸው።
- ስለ ዳንኤል ሲጠየቁ በኩራትና በትህትና መልስ።
- የዳንኤል ስልክ ቁጥር 0986980130 መሆኑንና ቴሌግራሙ @Godis1256 መሆኑን አስፈላጊ ሲሆን ጥቀስ።
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
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        res_json = response.json()
        answer = res_json['choices'][0]['message']['content']
        bot.reply_to(message, answer)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ ዳንኤል፣ ቴክኒካዊ ችግር አጋጥሞኛል። እባክህ API Key በ Render ላይ በትክክል መገባቱን አረጋግጥ።")

bot.infinity_polling()
