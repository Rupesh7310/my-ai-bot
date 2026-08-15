import telebot
import requests
import os
import threading
import http.server
import socketserver

# Yeh nakli server Render ko khush rakhne ke liye hai taaki wo error na de
def keep_alive():
    PORT = int(os.environ.get('PORT', 8080))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Fake server running on port {PORT}")
        httpd.serve_forever()

# Server ko background mein chalu kar diya
threading.Thread(target=keep_alive, daemon=True).start()

# --- Yahan se humara Asli Bot ka code shuru hota hai ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
MODEL_NAME = "models/gemma-4-26b-a4b-it"

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    print(f"📩 Message aaya: {message.text}")
    bot.send_chat_action(message.chat.id, 'typing') 
    
    try:
        # AI ko strict kiya gaya hai taaki bhashan na de
        prompt_text = (
            "Act as a cool, casual Indian friend speaking in Hinglish. "
            "CRITICAL INSTRUCTION: You must output ONLY your final spoken reply. "
            "NO internal thoughts, NO rules, NO options, NO bullet points, NO explanations. "
            "Just say your short 1-2 line reply directly.\n\n"
            f"User: {message.text}\n"
            "Friend: "
        )
        
        url = f"https://generativelanguage.googleapis.com/v1beta/{MODEL_NAME}:generateContent?key={GEMINI_KEY}"
        data = {"contents": [{"parts": [{"text": prompt_text}]}]}
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            jawab = response.json()['candidates'][0]['content']['parts'][0]['text']
            jawab = jawab.replace("Friend:", "").replace("Option 1:", "").strip()
            bot.reply_to(message, jawab)
        else:
            bot.reply_to(message, f"Google Error: {response.text}")
            
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.infinity_polling()
