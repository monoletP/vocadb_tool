from typing import Dict, List
from datetime import datetime
from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dtdate_korean
from vocadb_tools.utils.mappings import get_korean_vocalist

class SongListFormatter:
    def __init__(self, song_ids: List[int]):
        """
        곡 id 리스트를 받아 포맷팅하는 클래스입니다.
        
        Args:
            song_ids (List[int]): VocaDB의 곡 ID 리스트.
        """
        self.api = VocaDBAPI()
        self.song_ids = song_ids

    def _format_media_icons(self, pvs: List[Dict]) -> str:
        """
        PV 링크를 위키 아이콘으로 변환합니다.
        """
        icons = {
            'NicoNicoDouga': '[[파일:니코니코 동화 아이콘.svg|width=24]]',
            'Youtube': '[[파일:유튜브 아이콘.svg|width=27]]',
            'Bilibili': '[[파일:빌리빌리 아이콘.svg|height=24]]',
            'SoundCloud': '[[파일:사운드클라우드 아이콘.svg|width=24]]',
            'Piapro': '[[파일:피아프로 아이콘.svg|width=24]]'
        }
        media_links = []
        earliest_date = datetime.max

        for pv in pvs:
            if not pv.get('pvType') == 'Original' or pv.get('disabled'):
                continue
            service = pv['service']
            url = pv['url']

            # YouTube Topic 채널 제외
            if service == 'Youtube' and pv['author'].endswith(('Topic', '주제')):
                continue

            if service in icons:
                media_links.append(f"[[{url}|{icons[service]}]]")

            # 가장 이른 공개일 찾기
            pub_date = datetime.fromisoformat(
                pv['publishDate'].replace('Z', '+00:00')
            )
            if pub_date < earliest_date:
                earliest_date = pub_date

        return ''.join(media_links), earliest_date

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

            # 가수 목록 처리 (중복 제거하며 순서 유지)
            vocals_list = []
            for vocal in song_data['artists']:
                if vocal['categories'] == 'Vocalist' and not vocal['isSupport']:
                    vocal_korean = get_korean_vocalist(vocal['name'])
                    if vocal_korean not in vocals_list:
                        vocals_list.append(vocal_korean)

            # 린렌 예외 처리
            if ('카가미네 린·렌|카가미네 린' in vocals_list and 
                '카가미네 린·렌|카가미네 렌' in vocals_list):
                idx = min(vocals_list.index('카가미네 린·렌|카가미네 린'),
                            vocals_list.index('카가미네 린·렌|카가미네 렌'))
                vocals_list = [v for v in vocals_list if v not in ('카가미네 린·렌|카가미네 린', '카가미네 린·렌|카가미네 렌')]
                vocals_list.insert(idx, '카가미네 린·렌')
            
            vocals_str = ', '.join(f"[[{v}]]" for v in vocals_list)

            # 미디어 링크와 공개일 처리
            media_links, pub_date = self._format_media_icons(
                song_data['pvs']
            )
            if pub_date != datetime.max:
                formatted_date = format_dtdate_korean(pub_date)

                # 최종 출력 행 구성
                output_row = (
                    f"{name_row} {vocals_str} || {media_links} || "
                    f"{formatted_date} || ||"
                )
                output_list.append((pub_date, output_row))

        # 공개일을 기준으로 정렬
        output_list.sort(key=lambda x: x[0])

        return '\n'.join(row for _, row in output_list)