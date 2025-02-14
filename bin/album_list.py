#!/usr/bin/env python3
from vocadb_tools.formatters.album_list import AlbumListFormatter
import argparse
import pyperclip

def main():
    parser = argparse.ArgumentParser(description='Generate album list for a song on VocaDB')
    parser.add_argument('song_id', type=int, help='Song ID on VocaDB')
    args = parser.parse_args()
    
    formatter = AlbumListFormatter(args.song_id)
    formatted_entries = formatter.format_album_entries()

    pyperclip.copy(formatted_entries)
    print(formatted_entries)

if __name__ == '__main__':
    main()