from pyrogram import Client, filters
import os

# معلوماتك المؤكدة من الصور السابقة
API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

# رابط تطبيقك الحقيقي على Railway
RAILWAY_URL = "https://web-production-a21b7.up.railway.app" 

app = Client("simba_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.video | filters.document)
async def get_link(client, message):
    try:
        # استخراج المعرف الفريد للملف
        file_id = message.video.file_id if message.video else message.document.file_id
        
        # إنشاء الرابط المباشر باستخدام رابط Railway
        direct_link = f"{RAILWAY_URL}/stream/{file_id}.mp4"
        
        # الرد على المستخدم بالرابط
        await message.reply_text(
            f"✅ **يا بطل، رابط البث المباشر جاهز:**\n\n"
            f"`{direct_link}`\n\n"
            f"🚀 يمكنك الآن لصقه في VLC أو متصفحك."
        )
    except Exception as e:
        await message.reply_text(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    print("🚀 سيمبا بوت بدأ العمل على Railway...")
    app.run()
