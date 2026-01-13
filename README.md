# vocadb_tool 사용설명서

이 패키지는 VocaDB를 사용해서 나무위키의 음성 합성 엔진 관련 내용을 생성합니다. 모든 명령어는 vocadb_tool 폴더 위치에서 실행합니다.

[사이트](https://vocadb-tool-1024514772433.asia-northeast1.run.app)

## 환경 설정

### YouTube API 키 설정 (선택 사항)

정확한 투고 시각(UTC+9 기준 날짜)을 가져오려면 YouTube Data API v3 키가 필요합니다:

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. 프로젝트 생성 또는 선택
3. "API 및 서비스" > "라이브러리"에서 "YouTube Data API v3" 활성화
4. "사용자 인증 정보" > "API 키 만들기"
5. 환경 변수 설정:
   ```bash
   # Windows (PowerShell)
   $env:YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
   
   # Linux/Mac
   export YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
   ```

**참고:** API 키 없이도 사용 가능하지만, VocaDB의 날짜 정보(자정 기준)를 사용합니다.

## 사용법

### 앨범 정보 가져오기

다음 명령어를 사용하여 앨범 정보를 가져옵니다. 결과는 클립보드에 복사됩니다.

    python -m bin.album <album_id> --mode <mode>

<album_id>는 앨범 창의 주소에서 /S/ 뒤의 숫자입니다. 예를 들어 앨범 [No title+](https://vocadb.net/Al/9553)의 표를 생성한다면 다음과 같이 입력합니다.

    python -m bin.album 9553

mode는 full, only_link, utaite 세 가지가 있습니다. 기본값은 full입니다.

- full은 모든 앨범 정보를 담은 표를 생성합니다. 프로듀서 문서의 디스코그래피 항목을 작성할 때 사용합니다.
- only_link는 앨범의 스트리밍 링크 주소만을 가져옵니다.
- utaite는 full과 마찬가지로 모든 앨범 정보를담은 표를 생성하는데, vocadb가 아닌 utaitedb에서 가져옵니다.

### 특정 곡의 음반 목록 가져오기

다음 명령어를 사용하여 입력한 song_id에 해당하는 곡이 수록된 모든 앨범들을 가져옵니다. 곡 문서의 음반 목록에 사용됩니다. 결과는 클립보드에 복사됩니다.

    python -m bin.album_list <song_id>

<song_id>는 곡 창의 주소에서 /S/ 뒤의 숫자입니다. 예를 들어 곡 [ヴァンパイア](https://vocadb.net/S/321205)의 음반 목록 문단을 생성한다면 다음과 같이 입력합니다.

    python -m bin.album_list 321205

### 프로듀서의 투고곡 목록 표 생성하기

#### 입력: 아티스트 id

다음 명령어를 사용해 입력한 artist_id에 해당하는 프로듀서 문서의 곡 목록 표를 생성할 수 있습니다. 결과는 클립보드에 복사됩니다. (chromedriver.exe를 최상단 폴더에 위치시켜야 함)

    python -m bin.song_list <artist_id> --song_type Unspecified --max_count <max_count>

<artist_id>는 프로듀서 창의 주소에서 /Ar/ 뒤의 숫자입니다. 예를 들어 프로듀서 [マサラダ](https://vocadb.net/Ar/121038)의 곡 목록 표를 생성한다면 다음과 같이 입력합니다.

    python -m bin.song_list 121038

<song_type>은 vocadb의 Song type을 선택합니다. 기본값은 Original입니다.

<max_count>는 최신으로부터 몇 곡을 가져올 것인지를 정합니다. 예를 들어 아래와 같이 입력하면 울트라 트레일러와 (무)책임집합체만 가져옵니다.(25.02.16 기준 최신 2곡)

    python -m bin.song_list 121038 --max_count 2

#### 입력: 곡 id들

다음 명령어를 사용해 artist_id가 아닌 곡 id들을 직접 입력해 곡 목록 표를 생성할 수 있습니다. 결과는 클립보드에 복사됩니다.

    python -m bin.song_list songs <song_id 1> <song_id 2> ...

예를 들어 아래와 같이 입력하면 (무)책임집합체와 mochimochi를 가져옵니다.

    python -m bin.song_list songs 667339 626191

#### 입력: html 코드

다음 명령어를 사용해 클립보드에 복사된 html 코드로부터 곡 id들을 추출해 곡 목록 표를 생성할 수 있습니다. 결과는 클립보드에 복사됩니다. [참고](https://gall.dcinside.com/mgallery/board/view?id=mikuhatsune&no=230899)

    python -m bin.song_list html
