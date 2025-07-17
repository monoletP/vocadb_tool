import requests
import time, random
from typing import Dict, List
from vocadb_tools.utils.exceptions import VocaDBAPIError

class VocaDBAPI:
    BASE_URLS = {
        'vocadb': "https://vocadb.net/api",
        'utaitedb': "https://utaitedb.net/api"
    }
    
    def __init__(self, site: str = 'vocadb'):
        """
        site에 따라 base_url이 설정됩니다.
        Args:
            site (str): 'vocadb' 또는 'utaitedb' 중 하나
        """
        if site not in self.BASE_URLS:
            raise ValueError(f"Invalid site: {site}. Must be one of {list(self.BASE_URLS.keys())}")
            
        self.base_url = self.BASE_URLS[site]
        self.session = requests.Session()
    
    def get_album_details(self, album_id: int) -> Dict:
        """
        앨범 세부 정보를 가져옵니다.
        """
        url = f"{self.base_url}/albums/{album_id}/details"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            time.sleep(random.uniform(0.1, 0.5))
            return response.json()
        except requests.exceptions.RequestException as e:
            raise VocaDBAPIError(f"앨범 정보를 가져오는데 실패했습니다: {e}") from e
    
    def get_song_details(self, song_id: int, params: Dict = None) -> Dict:
        """
        곡 세부 정보를 가져옵니다.
        """
        if params is None:
            params = {'fields': 'Artists,PVs,Albums'}
        url = f"{self.base_url}/songs/{song_id}"
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(random.uniform(0.1, 0.5))
            return response.json()
        except requests.exceptions.RequestException as e:
            raise VocaDBAPIError(f"곡 정보를 가져오는데 실패했습니다: {e}") from e
    def get_song_list(self, artist_id: int, song_type: str = "Original", max_count: int = 1000) -> List[int]:
        """
        가수의 곡 목록에서 곡 ID 리스트를 가져옵니다.
        API를 통해 JSON 데이터를 가져와서 곡 ID를 추출합니다.
        max_count 개 이상의 곡 ID를 수집하면 반복을 종료합니다.
        """
        
        url = f"{self.base_url}/songs"
        all_song_ids: List[int] = []
        start = 0
        max_results = 300  # 한 번에 더 많은 데이터를 가져오도록 증가
        
        try:
            while len(all_song_ids) < max_count:
                params = {
                    "start": str(start),
                    "getTotalCount": "true",
                    "maxResults": str(max_results),
                    "query": "",
                    "fields": "AdditionalNames,MainPicture",
                    "lang": "Default",
                    "nameMatchMode": "Auto",
                    "sort": "PublishDate",
                    "songTypes": song_type,
                    "childTags": "false",
                    "artistId[]": str(artist_id),
                    "artistParticipationStatus": "OnlyMainAlbums",
                    "onlyWithPvs": "true"
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                items = data.get("items", [])
                
                if not items:
                    break
                    
                # 각 item에서 id 추출
                for item in items:
                    if "id" in item:
                        all_song_ids.append(item["id"])
                        if len(all_song_ids) >= max_count:
                            break
                
                # 더 이상 가져올 데이터가 없으면 종료
                if len(items) < max_results:
                    break
                    
                start += max_results
                time.sleep(0.1)  # API 호출 간격 조절
            
            return all_song_ids[:max_count]
            
        except requests.exceptions.RequestException as e:
            raise VocaDBAPIError(f"API 요청 실패: {e}") from e
        except Exception as e:
            raise VocaDBAPIError(f"곡 목록을 가져오는데 실패했습니다: {e}") from e
