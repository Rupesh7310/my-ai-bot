import telebot
import requests
import os

# Keys server se aayengi (Safe mode)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
MODEL_NAME = "models/gemma-4-26b-a4b-it"

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    print(f"📩 Message aaya: {message.text}")
    bot.send_chat_action(message.chat.id, 'typing') 
    
    try:
        # YAHAN HUMNE AI KO NAYA ATTITUDE DE DIYA HAI 😎
        prompt_text = (
            "You are a cool, casual, and friendly Telegram bot. "
            "Act like a close friend. Give very short, quick, and casual replies in Hinglish or English. "
            "NEVER write long paragraphs. Keep your reply to 1 or 2 lines maximum. "
            "Do NOT output your internal thinking, reasoning, or options. "
            "Only output the final, direct reply to the user.\n\n"
            f"User says: {message.text}"
        )
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={GEMINI_KEY}"
        data = {"contents": [{"parts": [{"text": prompt_text}]}]}
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            jawab = response.json()['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(message, jawab.strip())
        else:
            bot.reply_to(message, f"Google Error: {response.text}")
            
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()
