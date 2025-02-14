import re

def is_japanese(text: str) -> bool:
    """
    텍스트가 일본어를 포함하고 있는지 확인합니다.
    """
    # 히라가나, 가타가나, 한자 중 하나라도 포함되어 있는지 확인
    has_hiragana = bool(re.search(r'[\u3040-\u309F]', text))  # 히라가나
    has_katakana = bool(re.search(r'[\u30A0-\u30FF]', text))  # 가타가나
    has_kanji = bool(re.search(r'[\u4E00-\u9FAF]', text))     # 한자

    # 히라가나, 가타가나, 한자 중 하나라도 포함되면 True 반환
    return has_hiragana or has_katakana or has_kanji