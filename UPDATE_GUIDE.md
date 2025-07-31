# EverythingEverywhere 업데이트 가이드

## 🔄 기존 설치에서 v1.1.0으로 업데이트

### 단계별 업데이트 방법

#### 1. Chrome 확장 프로그램 페이지 열기
```
chrome://extensions/
```

#### 2. EverythingEverywhere 찾기
- 설치된 확장 프로그램 목록에서 "EverythingEverywhere" 찾기

#### 3. 새로고침 (권장)
- 확장 프로그램 카드 우하단의 **새로고침 🔄 버튼** 클릭
- 또는 **"다시 로드"** 링크 클릭

#### 4. Chrome 재시작
- Chrome을 **완전히 종료** 후 다시 시작
- 이 단계는 매우 중요합니다!

#### 5. 업데이트 확인
- 확장 프로그램 아이콘 클릭
- 새로운 "설정" 버튼이 보이는지 확인
- 버전이 1.1.0인지 확인

## 🆕 새로운 기능 테스트

### 설정 기능 사용해보기
1. 확장 프로그램 아이콘 클릭
2. **"설정"** 버튼 클릭
3. Everything 경로 설정 화면 확인
4. 추천 경로들이 표시되는지 확인

### Everything 상태 확인
- "✅ Everything 연결됨" 또는
- "⚠️ Everything을 찾을 수 없습니다" 메시지 확인
- 현재 사용 중인 경로가 표시되는지 확인

## 🔧 문제 해결

### 업데이트가 적용되지 않는 경우
1. **완전 재설치**:
   - 기존 확장 프로그램 "제거"
   - 새로 "압축해제된 확장 프로그램 로드"

2. **캐시 정리**:
   - Chrome 개발자 도구 (F12) → Application → Storage → Clear storage

3. **권한 확인**:
   - 새로운 "storage" 권한이 추가되었는지 확인

### 설정이 작동하지 않는 경우
1. Native Host 재설치:
   ```bash
   cd installer
   uninstall.bat
   install.bat
   ```

2. 로그 확인:
   ```bash
   native-host/native_host.log
   ```

## 📋 업데이트 체크리스트

- [ ] Chrome 확장 프로그램에서 새로고침 완료
- [ ] Chrome 완전 재시작 완료
- [ ] 새로운 설정 버튼 확인
- [ ] Everything 상태 정상 표시
- [ ] 우클릭 검색 기능 정상 작동
- [ ] 설정에서 경로 테스트 기능 작동

## 💡 새 기능 활용 팁

### Everything이 자동 탐지되지 않는 경우
1. 설정 → Everything 경로 직접 입력
2. 추천 경로 중 하나 클릭
3. "테스트" 버튼으로 유효성 확인
4. "저장" 버튼으로 설정 완료

### 포터블 버전 사용자
- 포터블 Everything 경로를 직접 설정
- 예: `D:\PortableApps\Everything\Everything.exe`

### 사용자 정의 설치 위치
- 비표준 경로에 설치된 Everything도 설정 가능
- 예: `C:\MyTools\Everything\Everything.exe`