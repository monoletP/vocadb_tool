import requests
from bs4 import BeautifulSoup
import re
import time
from typing import List
from vocadb_tools.utils.exceptions import VocaDBAPIError
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class VocaDBScraper:
    BASE_URLS = {
        'vocadb': "https://vocadb.net",
        'utaitedb': "https://utaitedb.net"
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
        
    def get_song_ids_from_html(self, html: str) -> List[int]:
        """
        td 태그의 style이 "width: 80px;"인 내부의 a 태그에서 곡 ID 리스트를 추출합니다.
        """
        soup = BeautifulSoup(html, 'html.parser')
        song_ids: List[int] = []
        for td_tag in soup.find_all('td', style="width: 80px;"):
            a_tag = td_tag.find('a', href=True)
            if a_tag:
                match = re.match(r'/S/(\d+)', a_tag['href'])
                if match:
                    song_ids.append(int(match.group(1)))
        return song_ids
        
    def get_song_list(self, artist_id: int, song_type: str = "Original", max_count: int = 1000) -> List[int]:
        """
        가수의 곡 목록에서 곡 ID 리스트를 가져옵니다.
        Selenium을 사용해 JavaScript 렌더링이 필요한 페이지의 HTML을 가져옵니다.
        max_count 개 이상의 곡 ID를 수집하면 반복을 종료합니다.
        """
        
        url = f"{self.base_url}/Search"
        params = {
            "searchType": "Song",
            "artistId[0]": f"{artist_id}",
            "artistParticipationStatus": "OnlyMainAlbums",
            "childTags": "false",
            "childVoicebanks": "false",
            "draftsOnly": "false",
            "filter": "",
            "maxLength": "0",
            "minLength": "0",
            "onlyRatedSongs": "false",
            "onlyWithPVs": "true",
            "page": "1",
            "pageSize": "40",
            "songType": song_type,
            "sort": "PublishDate",
            "unifyEntryTypesAndTags": "false",
            "viewMode": "Details"
        }
        
        all_song_ids: List[int] = []
        
        # Selenium 드라이버 설정 (Chrome)
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        
        try:
            page = 1
            while True:
                params["page"] = str(page)
                query_string = urllib.parse.urlencode(params)
                full_url = f"{url}?{query_string}"
                driver.get(full_url)
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "td[style='width: 80px;']"))
                    )
                except TimeoutException:
                    break

                time.sleep(1)
                html = driver.page_source
                
                song_ids: List[int] = self.get_song_ids_from_html(html)
                if not song_ids:
                    break
                all_song_ids.extend(song_ids)
                if len(all_song_ids) >= max_count:
                    break
                page += 1
            
            return all_song_ids[:max_count]
        except Exception as e:
            raise VocaDBAPIError(f"곡 목록을 가져오는데 실패했습니다: {e}") from e
        finally:
            driver.quit()
