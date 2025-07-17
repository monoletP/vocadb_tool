#!/usr/bin/env python3
import sys
import argparse
import pyperclip
from vocadb_tools.formatters.song_list import SongListFormatter
from vocadb_tools.api.vocadb import VocaDBAPI
from vocadb_tools.scraper.vocadb_scraper import get_song_ids_from_html

def main():
    parser = argparse.ArgumentParser(description="Generate song list table from VocaDB")
    subparsers = parser.add_subparsers(dest="mode", help="Mode to run the script in")

    # artist 모드 인자 설정
    artist_parser = subparsers.add_parser("artist", help="Receive artist id and fetch song list")
    artist_parser.add_argument("artist_id", type=int, help="The ID of the artist to fetch data for")
    artist_parser.add_argument("--song_type", type=str, default="Original",
                               choices=["Unspecified", "Original", "Cover", "Remix", "Instrumental", "Mashup", "MusicPV", "DramaPV", "Other"],
                               help="The type of songs to fetch")
    artist_parser.add_argument("--max_count", type=int, default=1000, help="The maximum number of songs to fetch")

    # songs 모드 인자 설정
    songs_parser = subparsers.add_parser("songs", help="Receive a list of song IDs to format")
    songs_parser.add_argument("songs", type=int, nargs="+", help="The list of song IDs to format")
    
    # html 모드 인자 설정
    html_parser = subparsers.add_parser("html", help="Receive HTML code and fetch song IDs")

    args = parser.parse_args()

    if args.mode == "artist":
        # artist 모드의 경우 artist_id 인자가 반드시 필요합니다.
        if not hasattr(args, "artist_id"):
            parser.error("artist 모드에서는 artist_id 인자가 필수입니다.")
        api = VocaDBAPI()
        song_ids = api.get_song_list(args.artist_id, song_type=args.song_type, max_count=args.max_count)
        formatter = SongListFormatter(song_ids)
    elif args.mode == "songs":
        formatter = SongListFormatter(args.songs)
    elif args.mode == "html":
        html_code = pyperclip.paste()
        song_ids = get_song_ids_from_html(html_code)
        formatter = SongListFormatter(song_ids)
    else:
        parser.error("mode 인자는 artist, songs, html 중 하나여야 합니다.")
        sys.exit()
    
    formatted_table = formatter.format_song_list()
    pyperclip.copy(formatted_table)
    print(formatted_table)

if __name__ == '__main__':
    # sys.argv의 두 번째 인자가 int인 경우 기본 subcommand를 추가합니다.
    if len(sys.argv) < 2 or sys.argv[1].isdigit():
        sys.argv.insert(1, 'artist')
    main()
