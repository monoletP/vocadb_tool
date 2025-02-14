from datetime import datetime
from typing import Dict, List

def format_dictdate_korean(date_dict: Dict) -> str:
    """
    딕셔너리로 저장된 날짜를 한국어 형식으로 변환합니다.
    """
    return f"{date_dict['year']}년 {date_dict['month']}월 {date_dict['day']}일"

def format_dtdate_korean(date_obj: datetime) -> str:
    """
    datetime로 저장된 날짜를 한국어 형식으로 변환합니다.
    """
    return f"{date_obj.year}년 {date_obj.month}월 {date_obj.day}일"

def format_media_links(weblinks: List[Dict]) -> str:
    """
    미디어 링크들을 위키 문법으로 변환합니다.
    """
    icons = {
        'amazon': "[[파일:아마존닷컴 아이콘.svg|width=24]]",
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

        if link.get('category', '') != 'Commercial':
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
        elif service in ['itunes', 'itunes (jp)']:
            order_index = ordering['apple']
            url = url.replace('itunes', 'music')
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