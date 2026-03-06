import os
import telebot
from yt_dlp import YoutubeDL

API_TOKEN = '8539330758:AAEGZTrXHDGj-ZtdBf53KlPIwcCIaTww928'
bot = telebot.TeleBot(API_TOKEN)

# Fitur balas /start agar tidak diam saja
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Halo! Kirimkan saja link TikTok ke sini, nanti saya download-kan videonya buat kamu.")

# Fitur download video
@bot.message_handler(func=lambda message: True)
def download_send(message):
    url = message.text
    if "http" in url:
        pesan_tunggu = bot.reply_to(message, "⏳ Sedang memproses video, tunggu sebentar ya...")
        try:
            # Trik ganti link YouTube Shorts
            link_final = url.replace("/shorts/", "/watch?v=") if "/shorts/" in url else url
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'video_%(id)s.mp4',
                'quiet': True,
                'no_warnings': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link_final, download=True)
                filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="✅ Ini videonya!")
            
            os.remove(filename)
            bot.delete_message(message.chat.id, pesan_tunggu.message_id)
            
        except Exception as e:
            bot.edit_message_text(f"❌ Gagal download! YouTube mungkin memblokir IP ini. Coba pakai Hotspot HP!", message.chat.id, pesan_tunggu.message_id)
            print(f"Error: {e}")

print("🚀 BOT SUDAH AKTIF!")
bot.polling()
