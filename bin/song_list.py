#!/usr/bin/env python3
from vocadb_tools.formatters.song_list import SongListFormatter
import pyperclip

def main():
    # 클립보드에서 HTML 코드 가져오기
    html_code = pyperclip.paste()

    formatter = SongListFormatter(html_code)
    formatted_table = formatter.format_song_list()
    
    pyperclip.copy(formatted_table)
    print(formatted_table)
    
if __name__ == '__main__':
    main()
