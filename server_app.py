from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pyrogram import Client
import uvicorn
import os

app = FastAPI()

# معلوماتك الحقيقية
API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

# استخدام اسم جلسة جديد ونظيف
client = Client("simba_srv_v2", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/stream/{file_id}.mp4")
async def stream_video(file_id: str):
    async def generate():
        try:
            async for chunk in client.stream_media(file_id):
                if not chunk: break
                yield chunk
        except Exception as e:
            print(f"Streaming Error: {e}")

    return StreamingResponse(
        generate(),
        media_type="video/mp4",
        headers={"Accept-Ranges": "bytes"}
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # تقليل مستوى السجلات يمنع Railway من حظرك
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="error")
