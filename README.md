# EverythingEverywhere 🔍

[![GitHub release](https://img.shields.io/github/v/release/username/EverythingEverywhere)](https://github.com/username/EverythingEverywhere/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

웹페이지에서 선택한 텍스트를 [Everything](https://www.voidtools.com/) 앱으로 즉시 검색할 수 있는 Chrome 확장 프로그램입니다.

## ✨ 주요 기능

- 🖱️ **간편한 우클릭 검색**: 웹페이지에서 텍스트 선택 후 우클릭만으로 즉시 검색
- ⚡ **빠른 실행**: Everything 앱이 자동으로 열리며 선택한 텍스트로 검색 수행
- 🔧 **자동 설치**: 확장 프로그램 ID와 Everything 경로 자동 감지
- 📁 **로컬 파일 검색**: 인터넷이 아닌 로컬 컴퓨터의 파일들을 빠르게 검색
- ⚙️ **수동 경로 설정**: Everything이 자동으로 찾아지지 않을 때 직접 경로 설정 가능
- 🎯 **지능형 탐지**: 다양한 Everything 설치 위치와 버전을 자동으로 탐지
- ✅ **경로 검증**: 설정한 Everything 경로가 유효한지 실시간 확인
- 📋 **자동 클립보드 복사**: 검색과 동시에 선택한 텍스트를 클립보드에 복사 (설정 가능)
- 🔔 **알림 기능**: 검색 완료 및 클립보드 복사 상태를 시각적으로 알림

## 🎬 데모

![EverythingEverywhere Demo](https://via.placeholder.com/600x400/1e293b/ffffff?text=Demo+GIF+Coming+Soon)

## 📋 요구사항

- ✅ Windows OS
- ✅ Google Chrome 브라우저
- ✅ [Everything](https://www.voidtools.com/) 검색 앱 설치
- ✅ Python 3.6 이상

## 🚀 빠른 설치 (권장)

1. **[최신 릴리즈 다운로드](https://github.com/username/EverythingEverywhere/releases/latest)**
2. **ZIP 파일 압축 해제**
3. **`setup.bat` 실행**
4. **안내에 따라 크롬 확장 프로그램 설치**
5. **크롬 재시작**

## 🔧 수동 설치

<details>
<summary>수동 설치 방법 (클릭하여 펼치기)</summary>

### 1. Everything 설치
- https://www.voidtools.com/ 에서 Everything 다운로드 및 설치

### 2. 크롬 확장 프로그램 로드
1. 크롬에서 `chrome://extensions/` 열기
2. 우측 상단 "개발자 모드" 활성화
3. "압축해제된 확장 프로그램 로드" 클릭
4. `chrome-extension` 폴더 선택

### 3. Native Messaging Host 설치
1. `installer` 폴더로 이동
2. `install.bat` 실행 (확장 프로그램 ID 자동 감지)
3. 설치 완료 메시지 확인

### 4. 크롬 재시작
- 크롬을 완전히 종료 후 다시 시작

</details>

## 📖 사용 방법

1. **텍스트 선택**: 웹페이지에서 검색하고 싶은 텍스트를 드래그로 선택
2. **우클릭**: 선택한 텍스트에서 마우스 우클릭
3. **메뉴 클릭**: "로컬에서 Everything으로 검색하기: [선택한 텍스트]" 클릭
4. **검색 결과**: Everything이 자동으로 열리며 검색 결과 표시

## ⚙️ 설정 방법

**Everything 경로가 자동으로 찾아지지 않는 경우:**

1. **확장 프로그램 아이콘** 클릭 (브라우저 우상단)
2. **"설정"** 버튼 클릭
3. **Everything.exe 전체 경로** 입력
4. **"테스트"** 버튼으로 경로 유효성 확인
5. **"저장"** 버튼으로 설정 저장

**추천 경로를 클릭**하면 자동으로 입력창에 입력됩니다.

### 📋 클립보드 복사 설정

1. **확장 프로그램 아이콘** 클릭 → **"설정"** 버튼 클릭
2. **"검색 시 텍스트를 클립보드에 자동 복사"** 체크박스 설정
3. **기본값**: 활성화 (검색 시 자동으로 클립보드에 복사됨)
4. **비활성화**: 검색만 실행하고 클립보드 복사하지 않음

이 기능을 활성화하면 Everything 검색과 동시에 선택한 텍스트가 클립보드에 복사되어 다른 곳에 붙여넣기할 수 있습니다.

## 🛠️ 문제 해결

<details>
<summary>자주 묻는 질문</summary>

### Everything이 실행되지 않는 경우
- Everything이 설치되어 있는지 확인
- 확장 프로그램 아이콘 클릭 → "설정" 버튼으로 수동 경로 설정
- `native-host/native_host.log` 파일에서 오류 로그 확인
- Everything이 기본 경로가 아닌 곳에 설치된 경우 환경변수 `EVERYTHING_PATH` 설정
- 포터블 버전이나 사용자 정의 설치 위치의 경우 설정에서 직접 경로 지정

### 확장 프로그램이 동작하지 않는 경우
- 크롬을 완전히 재시작
- `chrome://extensions/`에서 확장 프로그램 활성화 상태 확인
- 개발자 모드가 켜져 있는지 확인

### Native Host 오류
- 관리자 권한으로 `install.bat` 실행
- Windows Defender나 백신 프로그램에서 차단하지 않는지 확인

</details>

## 📁 프로젝트 구조

```
EverythingEverywhere/
├── chrome-extension/           # 🔧 Chrome 확장 프로그램
│   ├── manifest.json          # 확장 프로그램 설정
│   ├── background.js          # 백그라운드 스크립트
│   ├── popup.html & popup.js  # 팝업 UI
│   └── icons/                 # 아이콘 파일들
├── native-host/               # 🔗 Native Messaging Host
│   ├── native_host.py         # Python 메인 스크립트
│   └── *.json                 # 설정 파일
├── installer/                 # 📦 설치 스크립트
│   ├── install.py             # 자동 설치 스크립트
│   ├── install.bat            # Windows 배치 파일
│   └── uninstall.bat          # 제거 스크립트
└── README.md                  # 📖 프로젝트 문서
```

## 🗑️ 제거 방법

1. `installer/uninstall.bat` 실행
2. 크롬 확장 프로그램 페이지에서 확장 프로그램 제거

## 🤝 기여하기

버그 리포트, 기능 제안, Pull Request 등 모든 기여를 환영합니다!

1. 이 저장소를 Fork
2. 새로운 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 배포됩니다.

## ⭐ 지원

이 프로젝트가 유용하다면 ⭐를 눌러주세요!