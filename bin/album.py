#!/usr/bin/env python3
from vocadb_tools.formatters.album import AlbumFormatter
from vocadb_tools.api.vocadb import VocaDBAPI
import argparse
import pyperclip

def main():
    parser = argparse.ArgumentParser(description='Generate album table from VocaDB data.')
    parser.add_argument('album_id', type=int, help='The ID of the album to fetch data for.')
    parser.add_argument('--mode', type=str, default='full', 
                       choices=['full', 'only_link', 'utaite'], 
                       help='Mode to run the script in. "full" generates the full album table, "only_link" extracts only the links, "utaite" accesses utaitedb.net.')
    args = parser.parse_args()
    
    api = VocaDBAPI() if args.mode != 'utaite' else VocaDBAPI('utaitedb')
    album_data = api.get_album_details(args.album_id)
    formatter = AlbumFormatter(album_data)
    formatted = formatter.format_album()

    pyperclip.copy(formatted)
    print(formatted)

if __name__ == '__main__':
    main()