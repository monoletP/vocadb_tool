from typing import Dict

# 보컬리스트 매핑 딕셔너리 업데이트
VOCALIST_MAPPING: Dict[str, str] = {
    '初音ミク': '하츠네 미쿠',
    '鏡音リン': '카가미네 린·렌|카가미네 린',
    '鏡音レン': '카가미네 린·렌|카가미네 렌',
    '巡音ルカ': '메구리네 루카',
    'MEIKO': 'MEIKO',
    'KAITO': 'KAITO',
    '重音テト': '카사네 테토',
    '重音テトSV': '카사네 테토#카사네 테토 SV|카사네 테토 SV',
    'IA': 'IA -ARIA ON THE PLANETES-|IA',
    '結月ゆかり': '유즈키 유카리',
    '猫村いろは': '네코무라 이로하',
    '紲星あかり': '키즈나 아카리',
    'GUMI': 'GUMI from Megpoid|GUMI',
    'AI Megpoid': 'GUMI from Megpoid|GUMI',
    '音街ウナ': '오토마치 우나',
    'Synthesizer V AI 音街ウナ': '오토마치 우나#SynthV|오토마치 우나',
    '神威がくぽ': '가쿠포이드|카무이 가쿠포',
    '可不': '카후(음성 합성 라이브러리)|카후',
    '羽累': '하루(음성 합성 라이브러리)|하루',
    '星界': '세카이(음성 합성 라이브러리)|세카이',
    '裏命': '리메(음성 합성 라이브러리)|리메',
    '狐子': '코코(음성 합성 라이브러리)|코코',
    '歌愛ユキ': '카아이 유키',
    '鳴花ヒメ': '메이카 히메·미코토|메이카 히메',
    '鳴花ミコト': '메이카 히메·미코토|메이카 미코토',
    'v4 flower': 'flower(음성 합성 라이브러리)|v4 flower',
    'Ci flower': 'flower(음성 합성 라이브러리)|Ci flower',
    'v flower': 'flower(음성 합성 라이브러리)|v flower',
    'flower': 'flower(음성 합성 라이브러리)|flower',
    'ずんだもん': '즌다몬',
    '東北きりたん': '도호쿠 키리탄',
    '足立レイ': '아다치 레이',
    '小春六花': '코하루 릿카',
    '夏色花梨': '나츠키 카린',
    '花隈千冬': '하나쿠마 치후유',
    '知声': 'Chis-A'
    # 필요한 경우 다른 보컬리스트 추가
}

def get_korean_vocalist(name: str) -> str:
    """보컬리스트의 한국어 이름을 반환"""
            
    #가수가 매핑에 없으면 공백으로 잘라서 해당 단어가 매핑에 있는지 확인
    if name not in VOCALIST_MAPPING:
        name_splitted = name.split()
        for vocalist_word in name_splitted:
            if vocalist_word in VOCALIST_MAPPING:
                name = vocalist_word
                break
    
    # 한국어로 변환
    return VOCALIST_MAPPING.get(name, name)