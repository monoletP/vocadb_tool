from typing import Dict
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dictdate_korean, format_media_links
from vocadb_tools.utils.mappings import get_korean_vocalist

class AlbumFormatter:
    def __init__(self, album_data: Dict):
        self.album_data = album_data
        
    def _format_album_info(self) -> str:
        """
        앨범 정보를 위키 문법으로 포맷팅합니다.
        """
        album_name = self.album_data['name']
        ko_name = "[br]{{{-1 한글명}}}" if is_japanese(album_name) else ''
        
        release = self.album_data['originalRelease']
        release_date = format_dictdate_korean(release['releaseDate'])
        cat_num = release.get('catNum', '')

        pvs = self.album_data.get('pvs', [])
        pv_links = format_media_links(pvs)
        
        weblinks = self.album_data.get('webLinks', [])
        media_links = format_media_links(weblinks)
        
        # 앨범 기본 정보 템플릿
        output = [
            f"=== Album 《{album_name}》 ===",
            f"||<tablewidth=600px><tablealign=center><tablebgcolor=#ffffff,#2d2f34><tablebordercolor=#282a3e><-4> {{{{{{-2 Album}}}}}}[br]'''{{{{{{+2 {album_name}}}}}}}'''{ko_name} ||",
            "||<bgcolor=#fff,#1f2023><nopad><-4> [[파일:빈 가로 이미지.svg|width=100%]] ||",
            f"||<-2><width=15%><bgcolor=#DCDCDC,#2d2f34> '''발매일''' ||<-2><width=85%> {release_date} ||"
        ]
        
        if cat_num:
            output.append(f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''상품 번호''' ||<-2> {cat_num} ||")
        if pv_links:
            output.append(f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''트레일러''' ||<-2> {pv_links} ||")
        if media_links:
            output.append(f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''링크''' ||<-2> {media_links} ||")
        
        return '\n'.join(output)
    
    def _format_track_list(self) -> str:
        """
        트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
        tracks = []
        tracks.append("||<colkeepall><rowbgcolor=#DCDCDC,#2d2f34><width=9%> '''트랙''' ||<-2><width=70%> '''제목''' ||<width=21%> '''가수''' ||")
        
        for song in self.album_data['songs']:
            track_num = song['trackNumber']
            name = song['name']
            translation = " {{{-3 {{{#gray ()}}}}}}" if is_japanese(name) else ""
            
            artists = [get_korean_vocalist(a) for a in song['song']['artistString'].split("feat. ")[-1].strip().split(', ')] if 'song' in song else []
            artists_formatted = ', '.join(f"[[{a}]]" for a in artists)
            
            tracks.append(f"|| '''{track_num:02d}''' ||<-2>{name}{translation} || {artists_formatted} ||")
            
        return '\n'.join(tracks)

    def format_album(self) -> str:
        """
        앨범 정보와 트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
        album_info = self._format_album_info()
        track_list = self._format_track_list()
        
        return f"{album_info}\n{track_list}"
