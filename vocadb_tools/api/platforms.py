"""
플랫폼별 API/스크래핑을 통해 정확한 투고 날짜를 가져옵니다.
"""
import re
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional
from bs4 import BeautifulSoup

# 한국 시간대 (UTC+9)
KST = timezone(timedelta(hours=9))

def extract_video_id_from_url(url: str, service: str) -> Optional[str]:
    """URL에서 비디오 ID를 추출합니다."""
    if service == 'Youtube':
        # https://www.youtube.com/watch?v=VIDEO_ID
        # https://youtu.be/VIDEO_ID
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
    
    elif service == 'NicoNicoDouga':
        # https://www.nicovideo.jp/watch/smXXXXXXXX
        match = re.search(r'nicovideo\.jp/watch/([a-z0-9]+)', url)
        if match:
            return match.group(1)
    
    elif service == 'Bilibili':
        # https://www.bilibili.com/video/BV1xx411c7XD
        # https://www.bilibili.com/video/av12345678
        match = re.search(r'bilibili\.com/video/((?:BV|av)[a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
    
    return None

def get_youtube_publish_date(video_id: str, api_key: str) -> Optional[datetime]:
    """
    YouTube Data API v3를 사용하여 동영상의 정확한 투고 시각을 가져옵니다.
    반환값은 UTC+9(KST)로 변환된 datetime 객체입니다.
    """
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            'part': 'snippet',
            'id': video_id,
            'key': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            published_at = data['items'][0]['snippet']['publishedAt']
            # ISO 8601 형식 파싱 (예: 2024-01-01T12:34:56Z)
            dt = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            # UTC+9로 변환
            return dt.astimezone(KST)
    except Exception as e:
        print(f"YouTube API 오류 (video_id: {video_id}): {e}")
    
    return None

def get_niconico_publish_date(video_id: str) -> Optional[datetime]:
    """
    니코니코동화 페이지를 스크래핑하여 정확한 투고 시각을 가져옵니다.
    반환값은 UTC+9(KST)로 변환된 datetime 객체입니다.
    니코니코는 이미 JST(UTC+9)로 표시되므로 timezone만 추가합니다.
    """
    try:
        url = f"https://www.nicovideo.jp/watch/{video_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # meta 태그에서 uploadDate 추출
        meta_upload = soup.find('meta', {'property': 'video:release_date'})
        if meta_upload and meta_upload.get('content'):
            upload_date_str = meta_upload['content']
            # ISO 8601 형식 파싱
            dt = datetime.fromisoformat(upload_date_str.replace('Z', '+00:00'))
            # 이미 JST인 경우도 있으므로 KST로 변환
            return dt.astimezone(KST)
        
        # 대체: JSON-LD 데이터 파싱
        json_ld = soup.find('script', {'type': 'application/ld+json'})
        if json_ld:
            import json
            data = json.loads(json_ld.string)
            if 'uploadDate' in data:
                dt = datetime.fromisoformat(data['uploadDate'].replace('Z', '+00:00'))
                return dt.astimezone(KST)
    
    except Exception as e:
        print(f"니코니코 스크래핑 오류 (video_id: {video_id}): {e}")
    
    return None

def get_bilibili_publish_date(video_id: str) -> Optional[datetime]:
    """
    Bilibili API로 동영상 투고 시각을 가져옵니다.
    video_id는 BV 또는 av 번호입니다.
    Bilibili는 UTC+8(중국 시간)이지만 pubdate는 UTC 타임스탬프이므로 UTC+9로 변환합니다.
    """
    try:
        # BV 번호인 경우
        if video_id.startswith('BV'):
            url = f"https://api.bilibili.com/x/web-interface/view?bvid={video_id}"
        # av 번호인 경우 (av 접두사 제거)
        else:
            aid = video_id.replace('av', '')
            url = f"https://api.bilibili.com/x/web-interface/view?aid={aid}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('code') == 0 and 'data' in data:
            # pubdate는 Unix 타임스탬프 (UTC)
            timestamp = data['data']['pubdate']
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            # UTC+9로 변환
            return dt.astimezone(KST)
    
    except Exception as e:
        print(f"Bilibili API 오류 (video_id: {video_id}): {e}")
    
    return None

def get_platform_publish_date(url: str, service: str, youtube_api_key: Optional[str] = None) -> Optional[datetime]:
    """
    플랫폼별로 정확한 투고 시각을 가져옵니다.
    반환값은 UTC+9(KST) datetime 객체입니다.
    """
    video_id = extract_video_id_from_url(url, service)
    if not video_id:
        return None
    
    if service == 'Youtube' and youtube_api_key:
        return get_youtube_publish_date(video_id, youtube_api_key)
    elif service == 'NicoNicoDouga':
        return get_niconico_publish_date(video_id)
    elif service == 'Bilibili':
        return get_bilibili_publish_date(video_id)
    
    return None
