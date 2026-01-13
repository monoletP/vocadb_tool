from datetime import datetime, timezone, timedelta
from typing import Dict, List
from vocadb_tools.utils.mappings import get_vocalist_korean_name, get_producer_korean_name

# 한국 시간대 (UTC+9)
KST = timezone(timedelta(hours=9))

def format_dictdate_korean(date_dict: Dict) -> str:
    """
    딕셔너리로 저장된 날짜를 한국어 형식으로 변환합니다.
    """
    return f"{date_dict['year']}년 {date_dict['month']}월 {date_dict['day']}일"
def convert_utc_to_kst(date_obj: datetime) -> datetime:
    """
    UTC 시간을 KST(UTC+9)로 변환합니다.
    timezone 정보가 없는 datetime 객체는 UTC로 간주합니다.
    """
    if date_obj.tzinfo is None:
        date_obj = date_obj.replace(tzinfo=timezone.utc)
    return date_obj.astimezone(KST)
def format_dtdate_korean(date_obj: datetime) -> str:
    """
    datetime로 저장된 날짜를 한국어 형식으로 변환합니다.
    """
    return f"{date_obj.year}년 {date_obj.month}월 {date_obj.day}일"

def format_dtdate_short(date_obj: datetime) -> str:
    """
    datetime으로 저장된 날짜를 짧은 형식으로 변환합니다.
    """
    return f"{(date_obj.year % 100):02}/{date_obj.month:02}/{date_obj.day:02}"

def format_media_links(weblinks: List[Dict]) -> str:
    """
    미디어 링크들을 위키 문법으로 변환합니다.
    """
    icons = {
        'amazon': "[[파일:아마존닷컴 아이콘.svg|width=24&bgcolor=white]]",
        'apple': "[[파일:Apple Music 아이콘.svg|width=24]]",
        'spotify': "[[파일:스포티파이 아이콘.svg|width=24]]",
        'youtube': "[[파일:유튜브 아이콘.svg|width=27]]",
        'youtube music': "[[파일:유튜브 뮤직 아이콘.svg|width=24]]",
        'niconicodouga': "[[파일:니코니코 동화 아이콘.svg|width=24]]",
        'bilibili': "[[파일:빌리빌리 아이콘.svg|height=24]]",
        'soundcloud': "[[파일:사운드클라우드 아이콘.svg|width=24]]",
        'booth': "[[파일:BOOTH 아이콘.svg|width=24]]",
        'karent': "[[파일:KarenT.png|height=16&theme=light]][[파일:KarenT white.png|height=16&theme=dark]]"
    }
    
    ordering = {
        'amazon': 0,
        'apple': 1,
        'spotify': 2,
        'youtube music': 3,
        'karent': 4,
        'booth': 5,
        'niconicodouga': 6,
        'youtube': 7,
        'bilibili': 8,
        'soundcloud': 9
    }

    formatted_links_with_order = []
    for link in weblinks:
        if link.get('disabled', True):
            continue

        if 'category' in link and link.get('category', '') != 'Commercial':
            continue

        service_field = link.get('description', link.get('service'))
        if not service_field:
            continue
        service = service_field.lower()
        url = link['url']
        order_index = None

        if service in ordering:
            order_index = ordering[service]
            formatted_link = f"[[{url}|{icons[service]}]]"
        elif 'amazon' in service:
            if 'mp3' in service or 'unlimited' in service:
                continue
            order_index = ordering['amazon']
            icon = icons['amazon']
            url = f"https://www.amazon.co.jp/dp/{url.split('/dp/')[-1]}"
            
            if '(le) w/bonus' in service:
                label = '[*LEw/B]'
            elif 'le' in service:
                label = '[*LE]'
            elif 're' in service:
                label = '[*RE]'
            else:
                label = ''
            formatted_link = f"[[{url}|{icon}]]{label}"
        elif service in ['itunes', 'itunes (jp)']:
            order_index = ordering['apple']
            url = url.replace('itunes', 'music')
            formatted_link = f"[[{url}|{icons['apple']}]]"
        elif service in ['apple music', 'apple music (jp)']:
            order_index = ordering['apple']
            formatted_link = f"[[{url}|{icons['apple']}]]"
        elif service in ordering:
            order_index = ordering[service]
            formatted_link = f"[[{url}|{icons[service]}]]"
        else:
            continue

        formatted_links_with_order.append((order_index, formatted_link))

    formatted_links_with_order.sort(key=lambda x: x[0])
    formatted_links = (link for _, link in formatted_links_with_order)
            
    return ''.join(formatted_links)

def format_vocal_links(vocalists: List[str]) -> str:
    """
    가수들의 이름을 위키 문법으로 변환합니다.
    """
    output = []
    for v in vocalists:
        vocal_format = get_vocalist_korean_name(v)
        if vocal_format not in output:
            output.append(vocal_format)
        
    # 린렌 예외 처리
    if ('카가미네 린·렌|카가미네 린' in output and
        '카가미네 린·렌|카가미네 렌' in output):
        idx = min(output.index('카가미네 린·렌|카가미네 린'),
                    output.index('카가미네 린·렌|카가미네 렌'))
        output = [v for v in output if v not in (
            '카가미네 린·렌|카가미네 린', '카가미네 린·렌|카가미네 렌')]
        output.insert(idx, '카가미네 린·렌')
    
    return '[br]'.join({f"[[{v}]]" for v in output})

def parse_artist_vocals(artist_data: Dict) -> str:
    """
    아티스트 데이터에서 가수들의 이름을 위키 문법으로 변환합니다.
    """
    vocalists = []
    for artist in artist_data:
        if artist['categories'] == 'Vocalist' and not artist['isSupport']:
            vocal_korean = get_vocalist_korean_name(artist['name'])
            if vocal_korean not in vocalists:
                vocalists.append(vocal_korean)
    
    return format_vocal_links(vocalists)

def format_producer_links(producers: List[str]) -> str:
    """
    프로듀서들의 이름을 위키 문법으로 변환합니다.
    """
    output = []
    for p in producers:
        producer_format = get_producer_korean_name(p)
        output.append(producer_format)
    
    return '[br]'.join({f"[[{p}]]" for p in output})

def parse_producer(artist_data: Dict) -> str:
    """
    아티스트 데이터에서 프로듀서들의 이름을 위키 문법으로 변환합니다.
    """
    producers = []
    for artist in artist_data:
        if 'Producer' in [cat.strip() for cat in artist['categories'].split(',')] and not artist['isSupport']:
            producers.append(artist['name'])
    
    return format_producer_links(producers)