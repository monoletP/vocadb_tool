from typing import Dict, List
from datetime import datetime
from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dtdate_korean, parse_artist_vocals

class SongListFormatter:
    def __init__(self, song_ids: List[int]):
        """
        곡 id 리스트를 받아 포맷팅하는 클래스입니다.
        
        Args:
            song_ids (List[int]): VocaDB의 곡 ID 리스트.
        """
        self.api = VocaDBAPI()
        self.song_ids = song_ids

    def _format_media_icons(self, pvs: List[Dict]) -> (str, datetime):
        """
        PV 링크를 위키 아이콘으로 변환합니다.
        아이콘은 NicoNicoDouga, Youtube, Bilibili, SoundCloud, Piapro 순으로 합쳐집니다.
        """
        icons = {
            'NicoNicoDouga': '[[파일:니코니코 동화 아이콘.svg|width=24]]',
            'Youtube': '[[파일:유튜브 아이콘.svg|width=27]]',
            'Bilibili': '[[파일:빌리빌리 아이콘.svg|height=24]]',
            'SoundCloud': '[[파일:사운드클라우드 아이콘.svg|width=24]]',
            'Piapro': '[[파일:피아프로 아이콘.svg|width=24]]'
        }
        media_links_dict = {service: [] for service in icons}
        earliest_date = datetime.max

        for pv in pvs:
            if pv.get('pvType') != 'Original' or pv.get('disabled'):
                continue

            service = pv['service']
            url = pv['url']

            # YouTube Topic 채널 제외
            if service == 'Youtube' and pv['author'].endswith(('Topic', '주제')):
                continue

            if service in icons:
                media_links_dict[service].append(f"[[{url}|{icons[service]}]]")

            pub_date = datetime.fromisoformat(
                pv.get('publishDate', '2100-01-01T00:00:00')
            )
            if pub_date < earliest_date:
                earliest_date = pub_date

        # 원하는 순서대로 아이콘을 결합
        order = ['NicoNicoDouga', 'Youtube', 'Bilibili', 'SoundCloud', 'Piapro']
        media_links = ''.join(''.join(media_links_dict[service]) for service in order)

        return media_links, earliest_date

    def format_song_list(self) -> str:
        """
        곡 목록을 위키 문법으로 포맷팅합니다.
        """
        output_list = []

        for song_id in self.song_ids:
            song_data = self.api.get_song_details(song_id)

            name = song_data['defaultName']

            # 제목 행 구성
            if is_japanese(name):
                name_row = f"||  || {name} ||"
            else:
                name_row = f"||<-2> {name} ||"
           
            vocals_format = parse_artist_vocals(song_data['artists'])

            # 미디어 링크와 공개일 처리
            media_links, pub_date = self._format_media_icons(
                song_data['pvs']
            )
            if pub_date != datetime.max:
                formatted_date = format_dtdate_korean(pub_date)

                # 최종 출력 행 구성
                output_row = (
                    f"{name_row} {vocals_format} || {media_links} || "
                    f"{formatted_date} || ||"
                )
                output_list.append((pub_date, output_row))

        # 공개일을 기준으로 정렬
        output_list.sort(key=lambda x: x[0])

        return '\n'.join(row for _, row in output_list)