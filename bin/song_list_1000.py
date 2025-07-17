#!/usr/bin/env python3
import pyperclip
from vocadb_tools.formatters.song_list_1000 import SongListFormatter1000
from vocadb_tools.scraper.vocadb_scraper import get_song_ids_from_html

def main():
    html_code = pyperclip.paste()
    song_ids = get_song_ids_from_html(html_code)
    formatter = SongListFormatter1000(song_ids)
    
    formatted_table = formatter.format_song_list()
    pyperclip.copy(formatted_table)
    print(formatted_table)

if __name__ == '__main__':
    main()
