from setuptools import setup, find_packages

setup(
    name="vocadb_tools",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pyperclip>=1.8.2",
        "langdetect>=1.0.9",
        "selenium>=4.9.0"
    ],
    entry_points={
        "console_scripts": [
            "vocadb-album=bin.album:main",
            "vocadb-albumlist=bin.album_list:main",
            "vocadb-songlist=bin.song_list:main",
            "vocadb-songlist1000=bin.song_list_1000:main"
        ]
    }
)