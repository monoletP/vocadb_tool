from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.utils.language import is_japanese
from vocadb_tools.utils.formatting import format_dictdate_korean, format_media_links
from vocadb_tools.utils.mappings import get_korean_vocalist


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
            f"||<tablewidth=600px><tablealign=center><tablebgcolor=#ffffff,#2d2f34><tablebordercolor=#282a3e><-{5 if self.is_compilation else 4}> {{{{{{-2 Album}}}}}}[br]'''{{{{{{+2 {album_name}}}}}}}'''{ko_name} ||",
            f"||<bgcolor=#fff,#1f2023><nopad><-{5 if self.is_compilation else 4}> [[파일:빈 정사각형 이미지.svg|width=100%]] ||",
            f"||<-2><width=15%><bgcolor=#DCDCDC,#2d2f34> '''발매일''' ||<-{3 if self.is_compilation else 2}><width=85%> {release_date} ||"
        ]

        if cat_num:
            output.append(
                f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''상품 번호''' ||<-{3 if self.is_compilation else 2}> {cat_num} ||")
        if pv_links:
            output.append(
                f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''트레일러''' ||<-{3 if self.is_compilation else 2}> {pv_links} ||")
        if media_links:
            output.append(
                f"||<-2><bgcolor=#DCDCDC,#2d2f34> '''링크''' ||<-{3 if self.is_compilation else 2}> {media_links} ||")

        return '\n'.join(output)

    def _format_track_list(self) -> str:
        """
        트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
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
                f"||<-{5 if self.is_compilation else 4}><rowbgcolor=#DCDCDC,#2d2f34> {{{{{{-1 '''Disc 1{' - ' if disc_name else ''}{disc_name}'''}}}}}} ||")
        cur_disc = 1

        for song in self.album_data['songs']:
            if has_multiple_discs and song['discNumber'] != cur_disc:
                cur_disc = song['discNumber']
                disc_name = self.album_data['discs'][str(
                    cur_disc)].get('name', '')
                tracks.append(
                    f"||<-{5 if self.is_compilation else 4}><rowbgcolor=#DCDCDC,#2d2f34> {{{{{{-1 '''Disc {cur_disc}{' - ' if disc_name else ''}{disc_name}'''}}}}}} ||")

            track_num = song['trackNumber']
            name = song['name']
            translation = " {{{-3 {{{#gray ()}}}}}}" if is_japanese(name) else ""

            if 'song' in song:
                vocals_list = []
                for v in song['song']['artistString'].split(" feat. ")[-1].strip().split(', '):
                    vocal = get_korean_vocalist(v)
                    if vocal not in vocals_list:
                        vocals_list.append(vocal)

                # feat. various의 경우 곡 문서에 직접 접속해 가수 정보를 가져옴
                if 'various' in vocals_list:
                    song_id = song['song']['id']
                    song_data = self.api.get_song_details(song_id)

                    vocals_list = []
                    for vocal in song_data['artists']:
                        if (vocal['categories'] == 'Vocalist' and
                                not vocal['isSupport']):
                            vocalist_korean = get_korean_vocalist(
                                vocal['name'])
                            if vocalist_korean not in vocals_list:
                                vocals_list.append(vocalist_korean)

                # 린렌 예외 처리
                if ('카가미네 린·렌|카가미네 린' in vocals_list and
                        '카가미네 린·렌|카가미네 렌' in vocals_list):
                    idx = min(vocals_list.index('카가미네 린·렌|카가미네 린'),
                              vocals_list.index('카가미네 린·렌|카가미네 렌'))
                    vocals_list = [v for v in vocals_list if v not in (
                        '카가미네 린·렌|카가미네 린', '카가미네 린·렌|카가미네 렌')]
                    vocals_list.insert(idx, '카가미네 린·렌')

                vocals_str = ', '.join(f"[[{v}]]" for v in vocals_list)
            else:
                vocals_str = ""

            if self.is_compilation:
                tracks.append(
                    f"|| '''{track_num:02d}''' ||<-2>{name}{translation} || {vocals_str} || {song['song']['artistString'].split(' feat. ')[0]} ||")
            else:
                tracks.append(
                    f"|| '''{track_num:02d}''' ||<-2>{name}{translation} || {vocals_str} ||")

        return '\n'.join(tracks)

    def format_album(self) -> str:
        """
        앨범 정보와 트랙 리스트를 위키 문법으로 포맷팅합니다.
        """
        album_info = self._format_album_info()
        track_list = self._format_track_list()

        return f"{album_info}\n{track_list}"
