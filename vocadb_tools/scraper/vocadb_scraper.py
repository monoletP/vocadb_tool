import re
from typing import List
from bs4 import BeautifulSoup

def get_song_ids_from_html(html: str) -> List[int]:
    """
    td 태그의 style이 "width: 80px;" 또는 "width: 75px;"인 내부의 a 태그에서 곡 ID 리스트를 추출합니다.
    """
    soup = BeautifulSoup(html, 'html.parser')
    song_ids: List[int] = []
    for td_tag in soup.find_all('td', style={"width: 80px;", "width: 75px;"}):
        a_tag = td_tag.find('a', href=True)
        if a_tag:
            match = re.match(r'/S/(\d+)', a_tag['href'])
            if match:
                song_ids.append(int(match.group(1)))
    return song_ids