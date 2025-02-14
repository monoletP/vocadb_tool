# vocadb_tool 사용설명서

이 패키지는 VocaDB를 사용해서 나무위키의 음성 합성 엔진 관련 내용을 생성합니다. 모든 명령어는 vocadb_tool 폴더 위치에서 실행합니다.

## 사용법

### 앨범 정보 가져오기
다음 명령어를 사용하여 앨범 정보를 가져옵니다. 결과는 클립보드에 복사됩니다.

    python -m bin.album <album_id> --mode <mode>

<album_id>는 앨범 창의 주소에서 /S/ 뒤의 숫자입니다. 예를 들어 앨범 [No title+](https://vocadb.net/Al/9553)의 표를 생성한다면 다음과 같이 입력합니다.

    python -m bin.album 9553

mode는 full, only_link, utaite 세 가지가 있습니다. 기본값은 full입니다.
* full은 모든 앨범 정보를 담은 표를 생성합니다. 프로듀서 문서의 디스코그래피 항목을 작성할 때 사용합니다. 
* only_link는 앨범의 스트리밍 링크 주소만을 가져옵니다.
* utaite는 full과 마찬가지로 모든 앨범 정보를담은 표를 생성하는데, vocadb가 아닌 utaitedb에서 가져옵니다. 

TODO: Dics 줄 자동추가

### 특정 곡의 음반 목록 가져오기
다음 명령어를 사용하여 입력한 song_id에 해당하는 곡이 수록된 모든 앨범들을 가져옵니다. 곡 문서의 음반 목록에 사용됩니다. 결과는 클립보드에 복사됩니다. 

    python -m bin.album_list <song_id>

<song_id>는 곡 창의 주소에서 /S/ 뒤의 숫자입니다. 예를 들어 곡 [ヴァンパイア](https://vocadb.net/S/321205)의 음반 목록 문단을 생성한다면 다음과 같이 입력합니다.

    python -m bin.album_list 321205

### 프로듀서의 투고곡 목록 표 생성하기
다음 명령어를 사용해 프로듀서 문서의 곡 목록 표를 생성할 수 있습니다. 결과는 클립보드에 복사됩니다.

vocadb에 직접 접속해 프로듀서 문서에서 Recent songs / PVs을 클릭해 나오는 곡 목록에서 More filters를 클릭하고 Song type은 Original Song, Artist에서 Only main songs, 그리고 밑의 Only with PVs를 체크합니다. Showing 10 items of ???라 적힌 것을 클릭 후 한번에 보이는 곡 수를 40 또는 100으로 변경합니다.(표가 지나치게 길면 vocadb에 요청 도중 끊길 수 있습니다.)

그 다음 개발자 도구(f12)를 열어서 Ctrl+Shift+C로 표 요소를 선택합니다. 딱 봐도 앨범에만 수록되어 있는 곡은 tr요소를 선택 후 Delete element하는 것을 추천합니다. 마지막으로 tbody 요소를 선택 후 Copy - Copy element를 해서 표에 해당하는 html 코드를 클립보드에 복사합니다. 이것이 입력값으로 들어갑니다. 그리고 다음 명령어를 실행합니다. 

    python -m bin.song_list

설명이 이해가지 않는다면 다음 링크를 참고해주세요.(https://gall.dcinside.com/mgallery/board/view?id=mikuhatsune&no=230899)

TODO: html 코드를 직접 복사하지 않고 프로듀서 id만 입력하면 가져올 수 있게 수정
