import requests
import time, random
from typing import Dict
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