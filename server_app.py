from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from pyrogram import Client
import uvicorn
import os

app = FastAPI()

# معلوماتك المؤكدة
API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

# نستخدم جلسة البوت هنا
client = Client("stream_srv", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/stream/{file_id}.mp4")
async def stream_video(file_id: str):
    async def generate():
        # تعديل: طلبنا من تليجرام إرسال البيانات بقطع صغيرة جداً (64 كيلوبايت) لتبدأ الصورة فوراً
        async for chunk in client.stream_media(file_id, block_size=64 * 1024):
            yield chunk

    return StreamingResponse(
        generate(),
        media_type="video/mp4",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Type": "video/mp4",
            "Connection": "keep-alive",
        }
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
