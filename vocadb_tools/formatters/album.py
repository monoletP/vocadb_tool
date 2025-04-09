from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dictdate_korean, format_media_links, format_vocal_links, parse_artist_vocals, format_producer_links


class AlbumFormatter:
    def __init__(self, album_id: int, site: str = 'vocadb'):
        self.api = VocaDBAPI() if site != 'utaitedb' else VocaDBAPI('utaitedb')
        self.album_id = album_id
        self.album_data = self.api.get_album_details(album_id)
        self.is_compilation = self.album_data['discType'] == 'Compilation'

    def _format_album_info(self) -> str:
        """
        앨범 정보를 위키 문법으로 포맷팅합니다.
        """
        album_name = self.album_data.get('name', '알 수 없음')
        ko_name = "[br]{{{-1 한글명}}}" if is_japanese(album_name) else ''

        release = self.album_data.get('originalRelease', {})
        release_date = format_dictdate_korean(release.get('releaseDate', ''))
        cat_num = release.get('catNum', '')

        pvs = self.album_data.get('pvs', [])
        pv_links = format_media_links(pvs)

        weblinks = self.album_data.get('webLinks', [])
        media_links = format_media_links(weblinks)

        col_padding = 5 if self.is_compilation else 4
        title_padding = 3 if self.is_compilation else 2

        output = [
            f"=== Album 《{album_name}》 ===",
            f"||<tablewidth=600px><tablealign=center><tablebgcolor=#ffffff,#2d2f34><tablebordercolor=#282a3e><-{col_padding}> {{{{{{-2 Album}}}}}}[br]'''{{{{{{+2 {album_name}}}}}}}'''{ko_name} ||",
            f"||<bgcolor=#fff,#1f2023><nopad><-{col_padding}> [[파일:빈 정사각형 이미지.svg|width=100%]] ||",
            f"||<-2><width=15%><bgcolor=#DCDCDC,#2d2f34> '''발매일''' ||<-{title_padding}><width=85%> {release_date} ||"
        ]

        extra_fields = {
            "상품 번호": cat_num,
            "트레일러": pv_links,
            "링크": media_links,
        }
        for label, value in extra_fields.items():
            if value:
                output.append(f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''{label}''' ||<-{title_padding}> {value} ||")

        return '\n'.join(output)

    def _format_track_list(self) -> str:
        """
        트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
        col_padding = 5 if self.is_compilation else 4
        
        tracks = []
        if self.is_compilation:
            tracks.append(
                "||<colkeepall><rowbgcolor=#DCDCDC,#2d2f34><width=9%> '''트랙''' ||<-2><width=50%> '''제목''' ||<width=21%> '''가수''' ||<width=20%> '''아티스트''' ||")
        else:
            tracks.append(
                "||<colkeepall><rowbgcolor=#DCDCDC,#2d2f34><width=9%> '''트랙''' ||<-2><width=70%> '''제목''' ||<width=21%> '''가수''' ||")

        has_multiple_discs = len(self.album_data['discs']) > 1
        if has_multiple_discs:
            disc_name = self.album_data['discs']["1"].get('name', '')
            tracks.append(
                f"||<-{col_padding}><rowbgcolor=#DCDCDC,#2d2f34> {{{{{{-1 '''Disc 1{' - ' if disc_name else ''}{disc_name}'''}}}}}} ||")
        cur_disc = 1

        for song in self.album_data['songs']:
            if has_multiple_discs and song['discNumber'] != cur_disc:
                cur_disc = song['discNumber']
                disc_name = self.album_data['discs'][str(
                    cur_disc)].get('name', '')
                tracks.append(
                    f"||<-{col_padding}><rowbgcolor=#DCDCDC,#2d2f34> {{{{{{-1 '''Disc {cur_disc}{' - ' if disc_name else ''}{disc_name}'''}}}}}} ||")

            track_num = song['trackNumber']
            name = song['name']
            translation = " {{{-3 {{{#gray ()}}}}}}" if is_japanese(name) else ""

            if 'song' in song:
                vocal_string = song['song']['artistString'].split(" feat. ")[-1].strip()
                vocals_format = ''
                producer_string = song['song']['artistString'].split(" feat. ")[0].strip()
                producer_format = format_producer_links(producer_string.split(',')) if producer_string else ""
                
                if vocal_string == 'various':
                    song_id = song['song']['id']
                    song_data = self.api.get_song_details(song_id)
                    
                    vocals_format = parse_artist_vocals(song_data['artists'])
                    
                else: vocals_format = format_vocal_links(vocal_string.split(',')) if vocal_string else ""
            else:
                vocals_format = ""
                producer_format = ""

            if self.is_compilation:
                tracks.append(
                    f"|| '''{track_num:02d}''' ||<-2>{name}{translation} || {vocals_format} || {producer_format} ||")
            else:
                tracks.append(
                    f"|| '''{track_num:02d}''' ||<-2>{name}{translation} || {vocals_format} ||")

        return '\n'.join(tracks)

    def format_album(self) -> str:
        """
        앨범 정보와 트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
        album_info = self._format_album_info()
        track_list = self._format_track_list()

        return f"{album_info}\n{track_list}"
