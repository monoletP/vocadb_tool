import json
from typing import Dict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
VOCALIST_MAPPING_FILE = DATA_DIR / "vocalist_mapping.json"
PRODUCER_MAPPING_FILE = DATA_DIR / "producer_mapping.json"

with open(VOCALIST_MAPPING_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)
    VOCALIST_MAPPING: Dict[str, str] = data["VOCALIST_MAPPING"]

with open(PRODUCER_MAPPING_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)
    PRODUCER_MAPPING: Dict[str, str] = data["PRODUCER_MAPPING"]

def get_vocalist_korean_name(name: str) -> str:
    """보컬리스트의 한국어 이름을 반환"""
    if name not in VOCALIST_MAPPING:
        name_splitted = name.split()
        for vocalist_word in name_splitted:
            if vocalist_word in VOCALIST_MAPPING:
                name = vocalist_word
                break
    return VOCALIST_MAPPING.get(name, name)

def get_producer_korean_name(name: str) -> str:
    """프로듀서의 한국어 이름을 반환"""
    return PRODUCER_MAPPING.get(name, name)