
        
import os
import telebot
import yt_dlp

# Koyeb serverida token mana shu qatordan olinadi
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Menga Instagram Reels, TikTok, YouTube Shorts yoki Snapchat havolasini yuboring. Telefoningiz o'chig'ida ham yuklab beraman! 🚀")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    
    if any(p in url for p in ["instagram.com", "tiktok.com", "youtube.com", "youtu.be", "snapchat.com"]):
        status_msg = bot.reply_to(message, "Video yuklanmoqda... ⏳")
        video_filename = "downloaded_video.mp4"
        
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
                    bot.send_video(message.chat.id, video, caption="Video muvaffaqiyatli yuklandi! ✨")
                os.remove(video_filename)
            else:
                bot.reply_to(message, "Xatolik: Fayl topilmadi.")
                
        except Exception as e:
            bot.edit_message_text("Xatolik yuz berdi. Havola xato yoki video yopiq profilda. ❌", message.chat.id, status_msg.message_id)
    else:
        bot.reply_to(message, "Iltimos, faqat Instagram, TikTok, YouTube yoki Snapchat havolasini yuboring! ⚠️")

print("Bot serverda uzluksiz ishga tushdi...")
bot.infinity_polling()
           
