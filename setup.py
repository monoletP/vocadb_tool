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
        "googletrans>=3.1.0"
    ],
    entry_points={
        "console_scripts": [
            "vocadb-album=vocadb_tools.bin.vocadb_album:main",
            "vocadb-albumlist=vocadb_tools.bin.vocadb_albumlist:main",
            "vocadb-songlist=vocadb_tools.bin.vocadb_songlist:main"
        ]
    }
)