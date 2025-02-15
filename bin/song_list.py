#!/usr/bin/env python3
import argparse
import pyperclip
from vocadb_tools.formatters.song_list import SongListFormatter

def main():
    parser = argparse.ArgumentParser(description="Generate song list for an artist from VocaDB")
    parser.add_argument("artist_id", type=int, help="Artist ID on VocaDB")
    parser.add_argument("max_count", type=int, nargs="?", default=1000,
                        help="Number of songs to fetch from the beginning (default: 1000)")
    args = parser.parse_args()

    formatter = SongListFormatter(args.artist_id, max_count=args.max_count)
    formatted_table = formatter.format_song_list()
    
    pyperclip.copy(formatted_table)
    print(formatted_table)
    
if __name__ == '__main__':
    main()
