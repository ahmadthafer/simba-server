from pyrogram import Client, filters
import os

# ضع معلوماتك هنا أو استخدم متغيرات البيئة
API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"
# استبدل هذا برابط تطبيقك في Railway بعد الرفع
RAILWAY_URL = "https://your-app-name.up.railway.app" 

app = Client("simba_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.video | filters.document)
async def get_link(client, message):
    file_id = message.video.file_id if message.video else message.document.file_id
    direct_link = f"{RAILWAY_URL}/stream/{file_id}.mp4"
    await message.reply_text(f"✅ رابط البث المباشر:\n\n`{direct_link}`")

if __name__ == "__main__":
    app.run()
