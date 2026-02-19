from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pyrogram import Client
import uvicorn
import os

app = FastAPI()

# معلوماتك المؤكدة
API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

# استخدام اسم جلسة ثابت لـ Railway
client = Client("simba_streaming", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/stream/{file_id}.mp4")
async def stream_video(file_id: str):
    try:
        async def generate():
            # حذفنا block_size لأن مكتبتك لا تدعمها وتسبب خطأ TypeError
            async for chunk in client.stream_media(file_id):
                if not chunk:
                    break
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
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Stream failed")

if __name__ == "__main__":
    # استخدام بورت Railway التلقائي وتقليل السجلات
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
