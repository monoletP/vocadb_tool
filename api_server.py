from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.formatters.album_list import AlbumListFormatter
from vocadb_tools.formatters.album import AlbumFormatter
from vocadb_tools.formatters.song_list import SongListFormatter
from vocadb_tools.scraper.vocadb_scraper import get_song_ids_from_html
import logging

app = FastAPI(title="VocaDB Tool API", version="1.0.0")
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 메인 페이지
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 각 기능별 페이지들
@app.get("/album", response_class=HTMLResponse)
async def album_page(request: Request):
    return templates.TemplateResponse("album.html", {"request": request})

@app.get("/album-list", response_class=HTMLResponse)
async def album_list_page(request: Request):
    return templates.TemplateResponse("album_list.html", {"request": request})

@app.get("/song-list-artist", response_class=HTMLResponse)
async def song_list_artist_page(request: Request):
    return templates.TemplateResponse("song_list_artist.html", {"request": request})

@app.get("/song-list-songs", response_class=HTMLResponse)
async def song_list_songs_page(request: Request):
    return templates.TemplateResponse("song_list_songs.html", {"request": request})

@app.get("/song-list-html", response_class=HTMLResponse)
async def song_list_html_page(request: Request):
    return templates.TemplateResponse("song_list_html.html", {"request": request})

# 폼 처리 엔드포인트들
@app.post("/album", response_class=HTMLResponse)
async def album_form(request: Request, album_id: int = Form(...), site: str = Form("vocadb"), mode: str = Form("full")):
    try:
        formatter = AlbumFormatter(album_id=album_id, site=site)
        
        if mode == 'only_link':
            formatted = formatter.format_album_links()
        else:
            formatted = formatter.format_album()
        
        return templates.TemplateResponse("album.html", {
            "request": request,
            "result": formatted,
            "message": "앨범 정보를 성공적으로 가져왔습니다.",
            "album_id": album_id,
            "mode": mode
        })
    except Exception as e:
        return templates.TemplateResponse("album.html", {
            "request": request,
            "error": str(e),
            "album_id": album_id,
            "mode": mode
        })

@app.post("/album-list", response_class=HTMLResponse)
async def album_list_form(request: Request, song_id: int = Form(...), site: str = Form("vocadb")):
    try:
        formatter = AlbumListFormatter(song_id=song_id, site=site)
        formatted = formatter.format_album_entries()
        
        return templates.TemplateResponse("album_list.html", {
            "request": request,
            "result": formatted,
            "message": "음반 목록을 성공적으로 가져왔습니다.",
            "song_id": song_id
        })
    except Exception as e:
        return templates.TemplateResponse("album_list.html", {
            "request": request,
            "error": str(e),
            "song_id": song_id
        })

@app.post("/song-list-artist", response_class=HTMLResponse)
async def song_list_artist_form(
    request: Request, 
    site: str = Form("vocadb"),
    artist_id: int = Form(...), 
    song_type: str = Form("Original"),
    max_count: Optional[int] = Form(None)
):
    try:
        api = VocaDBAPI(site=site)
        song_ids = api.get_song_list(
            artist_id,
            song_type=song_type,
            max_count=max_count if max_count is not None else 1000
        )
        formatter = SongListFormatter(song_ids, site=site)
        formatted = formatter.format_song_list()
        
        return templates.TemplateResponse("song_list_artist.html", {
            "request": request,
            "result": formatted,
            "message": "곡 목록을 성공적으로 가져왔습니다.",
            "artist_id": artist_id,
            "song_type": song_type,
            "max_count": max_count
        })
    except Exception as e:
        return templates.TemplateResponse("song_list_artist.html", {
            "request": request,
            "error": str(e),
            "artist_id": artist_id,
            "song_type": song_type,
            "max_count": max_count
        })

@app.post("/song-list-songs", response_class=HTMLResponse)
async def song_list_songs_form(request: Request, song_ids: str = Form(...), site: str = Form("vocadb")):
    try:
        # 쉼표로 구분된 곡 ID들을 파싱
        song_id_list = [int(id.strip()) for id in song_ids.split(',') if id.strip()]
        formatter = SongListFormatter(song_id_list, site=site)
        formatted = formatter.format_song_list()
        
        return templates.TemplateResponse("song_list_songs.html", {
            "request": request,
            "result": formatted,
            "message": f"{len(song_id_list)}개의 곡 목록을 성공적으로 가져왔습니다.",
            "song_ids": song_ids
        })
    except Exception as e:
        return templates.TemplateResponse("song_list_songs.html", {
            "request": request,
            "error": str(e),
            "song_ids": song_ids
        })

@app.post("/song-list-html", response_class=HTMLResponse)
async def song_list_html_form(request: Request, html_content: str = Form(...), site: str = Form("vocadb")):
    try:
        song_ids = get_song_ids_from_html(html_content)
        formatter = SongListFormatter(song_ids, site=site)
        formatted = formatter.format_song_list()
        
        return templates.TemplateResponse("song_list_html.html", {
            "request": request,
            "result": formatted,
            "message": f"HTML에서 {len(song_ids)}개의 곡을 추출했습니다.",
            "html_content": html_content
        })
    except Exception as e:
        return templates.TemplateResponse("song_list_html.html", {
            "request": request,
            "error": str(e),
            "html_content": html_content
        })

if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)