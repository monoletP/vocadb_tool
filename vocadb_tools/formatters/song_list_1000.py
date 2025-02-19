from typing import Dict, List
from datetime import datetime
from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dtdate_short
from vocadb_tools.utils.mappings import get_korean_vocalist

class SongListFormatter1000:
    def __init__(self, song_ids: List[int]):
        """
        곡 id 리스트를 받아 포맷팅하는 클래스입니다. 유튜브 1000만 재생수 달성 목록을 위한 클래스입니다.
        
        Args:
            song_ids (List[int]): VocaDB의 곡 ID 리스트.
        """
        self.api = VocaDBAPI()
        self.song_ids = song_ids

    def _get_publish_date(self, pvs: List[Dict]) -> (datetime | datetime):
        """
        PV 링크들에서 최초 투고일과, 유튜브 투고일을 가져옵니다.
        """

        earliest_date = datetime.max
        yt_date = datetime.max

        for pv in pvs:
            if pv.get('pvType') != 'Original' or pv.get('disabled'):
                continue

            service = pv['service']

            # YouTube Topic 채널 제외
            if service == 'Youtube' and pv['author'].endswith(('Topic', '주제')):
                continue

            pub_date = datetime.fromisoformat(
                pv.get('publishDate', '2100-01-01T00:00:00')
            )
            if pub_date < earliest_date:
                earliest_date = pub_date
                
            if service == 'Youtube' and pub_date < yt_date:
                yt_date = pub_date

        return earliest_date, yt_date

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
                name_row = f"||  || {name}"
            else:
                name_row = f"||<-2> {name}"

            # 가수 목록 처리 (중복 제거하며 순서 유지), 프료듀서 처리
            vocals_list = []
            producer_list = []
            for artist in song_data['artists']:
                if artist['categories'] == 'Vocalist' and not artist['isSupport']:
                    vocal_korean = get_korean_vocalist(artist['name'])
                    if vocal_korean not in vocals_list:
                        vocals_list.append(vocal_korean)
                elif 'Producer' in [cat.strip() for cat in artist['categories'].split(',')] and not artist['isSupport']:
                    producer_list.append(artist['name'])
                    
            if vocals_list == []:  # 가수가 없는 경우
                continue

            # 린렌 예외 처리
            if ('카가미네 린·렌|카가미네 린' in vocals_list and 
                '카가미네 린·렌|카가미네 렌' in vocals_list):
                idx = min(vocals_list.index('카가미네 린·렌|카가미네 린'),
                            vocals_list.index('카가미네 린·렌|카가미네 렌'))
                vocals_list = [v for v in vocals_list if v not in ('카가미네 린·렌|카가미네 린', '카가미네 린·렌|카가미네 렌')]
                vocals_list.insert(idx, '카가미네 린·렌')
            
            vocals_str = ', '.join(f"[[{v}]]" for v in vocals_list)
            producer_str = ', '.join(f"[[{p}]]" for p in producer_list)

            # 투고일, 투고일(유튜브) 처리
            pub_date, yt_date = self._get_publish_date(
                song_data['pvs']
            )
            if pub_date != datetime.max and yt_date != datetime.max:
                formatted_pub_date = format_dtdate_short(pub_date)
                formatted_yt_date = format_dtdate_short(yt_date)
                if formatted_pub_date == formatted_yt_date:
                    formatted_date_row = f"<-2> {formatted_pub_date}"
                else:
                    formatted_date_row = f" {formatted_pub_date} || {formatted_yt_date}"

                # 최종 출력 행 구성
                output_row = (
                    f"{name_row} ||{formatted_date_row} || {producer_str} || {vocals_str} ||"
                )
                output_list.append((pub_date, output_row))

        # 공개일을 기준으로 정렬
        output_list.sort(key=lambda x: x[0])

        return '\n'.join(row for _, row in output_list)