from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dictdate_korean, format_media_links
from vocadb_tools.api.vocadb import VocaDBAPI

class AlbumListFormatter:
    def __init__(self, song_id: int):
        self.api = VocaDBAPI()
        self.song_id = song_id
        self.song_data = self.api.get_song_details(song_id)
        
    def format_album_entries(self) -> str:
        """
        곡이 수록된 앨범 목록을 위키 문법으로 포맷팅합니다.
        """
        output_list = []
        
        for album in self.song_data['albums']:
            # 앨범 세부 정보 가져오기
            album_data = self.api.get_album_details(album['id'])
            
            # 트랙 번호 찾기
            track_num = ''
            is_multi_disc = (album_data.get('songs', [])[-1].get('discNumber', 1) != 1)
            for track in album_data.get('songs', []):
                if track.get('song', {}).get('id') == self.song_id:
                    disc_num = track.get('discNumber', -1)
                    track_disc = f'Disc {disc_num}, ' if is_multi_disc else ''
                    track_num = track_disc + str(track.get('trackNumber'))
                    break
            
            # 앨범명과 번역 처리
            album_name = album['name']
            translation_row = (
                "|| '''원제''' ||"
                f"{f' {album_name} ||' if is_japanese(album_name) else ''}"
            )
            
            # 발매일 처리
            release_date = format_dictdate_korean(album['releaseDate'])
            
            # 미디어 링크 처리
            media_links = format_media_links(album_data.get('webLinks', []))
            
            # 앨범 엔트리 구성
            entry = [
                "||<|5><#fff,#010101><tablebgcolor=#fff,#1c1d1f><nopad> "
                "[[파일:빈 정사각형 이미지.svg|height=177]] "
                "||<colbgcolor=#d3d3d3,#383b40> '''번역명''' "
                f"||{' ' if is_japanese(album_name) else f'<|2> {album_name}'} ||",
                translation_row,
                f"|| '''트랙''' || {track_num} ||",
                f"|| '''발매일''' || {release_date} ||",
                f"|| '''링크''' || {media_links} ||"
            ]
            
            output_list.append('\n'.join(entry))
        
        return '\n\n'.join(output_list)