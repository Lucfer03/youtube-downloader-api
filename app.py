from fastapi import FastAPI, Response
import yt_dlp
import io

app = FastAPI()

@app.get("/get-audio")
async def get_audio(url: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    
    # تحميل الصوت فـ ذاكرة مؤقتة (Buffer)
    buffer = io.BytesIO()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ملاحظة: yt-dlp كيتعامل مع الملفات، لذا غنحملوه فـ ملف مؤقت ثم نقراوه
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        
        with open(filename, 'rb') as f:
            data = f.read()
            
    return Response(content=data, media_type="audio/mpeg")
