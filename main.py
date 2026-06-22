from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "rafiq-server running"}

@app.get("/video/{video_id}")
def get_video_url(video_id: str):
    try:
        ydl_opts = {
            'format': 'best[ext=mp4][height<=480]/best[ext=mp4]/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False
            )
            return {
                "url": info['url'],
                "title": info.get('title', ''),
                "duration": info.get('duration', 0),
            }
    except Exception as e:
        return {"error": str(e)}
