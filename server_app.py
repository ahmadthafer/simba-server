from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pyrogram import Client
import uvicorn
import os

app = FastAPI()

API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

# استخدام اسم جلسة جديد لتجنب التعليق
client = Client("railway_srv", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/stream/{file_id}.mp4")
async def stream_video(file_id: str):
    try:
        async def generate():
            # استخدام حجم قطعة (Chunk) ثابت ومستقر
            async for chunk in client.stream_media(file_id, block_size=1024 * 256):
                if not chunk:
                    break
                yield chunk

        return StreamingResponse(
            generate(),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Type": "video/mp4",
                "Cache-Control": "no-cache",
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Stream failed")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error") # تقليل السجلات لمنع الـ Rate Limit
