import os
import telebot
import yt_dlp
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Menga Instagram Reels, TikTok yoki YouTube Shorts havolasini yuboring. 24/7 rejimda yuklab beraman! 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    
    if "instagram.com" in url or "tiktok.com" in url or "youtube.com" in url or "youtu.be" in url:
        status_msg = bot.reply_to(message, "Video yuklanmoqda... ⏳")
        
        video_filename = "/tmp/downloaded_video.mp4"
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_filename,
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            if os.path.exists(video_filename):
                os.remove(video_filename)
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            bot.delete_message(message.chat.id, status_msg.message_id)
            
            if os.path.exists(video_filename):
                with open(video_filename, 'rb') as video:
                    bot.send_video(message.chat.id, video, caption="Video yuklandi! ✨")
                os.remove(video_filename)
            else:
                bot.reply_to(message, "Xatolik: Fayl topilmadi.")
                
        except Exception as e:
            bot.edit_message_text("Xatolik yuz berdi. Havola xato yoki video yopiq profilda. ❌", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Iltimos, faqat Instagram, TikTok yoki YouTube havolasini yuboring! ⚠️")

@server.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    url = os.environ.get('RENDER_EXTERNAL_URL')
    bot.set_webhook(url=url + '/' + BOT_TOKEN)
    return "Bot Serverda Faol!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
  
