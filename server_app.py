from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pyrogram import Client
import uvicorn
import os

app = FastAPI()

API_ID = 36663397
API_HASH = "6663349d5f967cfb3d242cedfd4fcdbc"
BOT_TOKEN = "8474643725:AAFH0hHLnbHgX0mzjV-dRoB5s6lAdp8rWJU"

client = Client("stream_srv", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_event("startup")
async def startup():
    await client.start()

@app.get("/stream/{file_id}.mp4")
async def stream_video(file_id: str):
    async def generate():
        async for chunk in client.stream_media(file_id):
            yield chunk
    return StreamingResponse(generate(), media_type="video/mp4")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
