# 🚀 Multi Browser & Program Launcher

한 번의 클릭으로 여러 브라우저에서 원하는 사이트들을 자동으로 열고, 로컬 프로그램도 함께 실행하는 런처

## ✨ 주요 기능

- ✅ **무제한 URL**: 각 브라우저마다 1개~100개 이상 URL 설정 가능
- ✅ **로컬 프로그램 실행**: 원하는 .exe 파일도 함께 실행 가능
- ✅ **INI 파일 관리**: config.ini만 수정하면 됨 (exe 재컴파일 불필요)
- ✅ **다중 브라우저 지원**: Edge, Chrome, Brave, Firefox, Opera 등
- ✅ **자동 탭 열기**: 같은 브라우저의 여러 URL은 탭으로 열림
- ✅ **간편한 설정**: 메모장으로 config.ini 편집하면 끝!

## 📋 빠른 시작 (3단계)

### 1️⃣ URL 설정

`config.ini` 파일을 열어 원하는 URL 입력:

```ini
# 같은 브라우저를 여러 창으로 분리 가능!
[Edge-News]
url1 = https://www.naver.com
url2 = https://www.daum.net

[Chrome-Work]
url1 = https://www.google.com
url2 = https://mail.google.com
url3 = https://drive.google.com

[Chrome-Dev]
url1 = https://www.github.com
url2 = https://www.stackoverflow.com

[Brave]
url1 = https://www.youtube.com

[Programs]
program1 = C:\Windows\System32\calc.exe
program2 = C:\Program Files\Notepad++\notepad++.exe
```

### 2️⃣ EXE 생성

`build_exe.bat` 더블클릭 → 자동으로 빌드됨!

### 3️⃣ 실행

1. `dist\BrowserLauncher.exe` + `config.ini`를 같은 폴더에 복사
2. `BrowserLauncher.exe` 더블클릭!

## 📁 파일 구조

```
📦 프로젝트 폴더
├── browser_launcher.py    ← 메인 프로그램
├── config.ini            ← URL 설정 파일 ⭐
├── config_example.ini    ← 설정 예제 (참고용)
├── build_exe.bat         ← EXE 빌드 스크립트
├── requirements.txt      ← Python 패키지
├── 사용설명서.md         ← 상세 가이드
└── README.md            ← 이 파일

📦 빌드 후
dist/
├── BrowserLauncher.exe  ← 실행 파일 ⭐
└── config.ini           ← 이 파일도 같이 복사!
```

## 💡 사용 예시

### 업무용 세팅
```ini
[Edge]
url1 = https://mail.company.com
url2 = https://calendar.company.com

[Chrome]
url1 = https://jira.company.com
url2 = https://confluence.company.com
url3 = https://github.com/company
url4 = https://slack.com

[Programs]
program1 = C:\Program Files\Microsoft VS Code\Code.exe
program2 = C:\Program Files (x86)\Slack\slack.exe
program3 = C:\Program Files\Git\git-bash.exe
```

### 개인용 세팅
```ini
[Chrome]
url1 = https://www.youtube.com
url2 = https://www.netflix.com
url3 = https://www.reddit.com
url4 = https://mail.google.com
url5 = https://calendar.google.com
url6 = https://drive.google.com
url7 = https://keep.google.com
url8 = https://photos.google.com

[Programs]
program1 = C:\Program Files\Spotify\Spotify.exe
program2 = C:\Windows\System32\calc.exe
```

## 🔧 고급 기능

### 브라우저 추가/제거

**사용하지 않는 브라우저:**
- config.ini에서 해당 섹션 삭제 또는 주석 처리

**새 브라우저 추가:**
```ini
[Firefox]
url1 = https://www.mozilla.org
url2 = https://developer.mozilla.org
```

### 여러 설정 프로필 만들기

```
config_work.ini    ← 업무용
config_personal.ini ← 개인용
config_study.ini   ← 학습용
```

사용할 때: config.ini를 원하는 프로필로 교체

## 📖 상세 문서

전체 설명은 `사용설명서.md` 참고

## 🐛 문제 해결

### config.ini를 찾을 수 없습니다
→ config.ini 파일을 exe와 같은 폴더에 배치하세요

### 브라우저가 실행되지 않습니다
→ 해당 브라우저가 설치되어 있는지 확인하세요

### Brave 브라우저가 안 열립니다
→ `browser_launcher.py`에서 `'brave'`를 `'brave-browser'`로 변경 후 재빌드

## 📝 라이센스

자유롭게 사용하세요!

---

**버전:** 1.0
**최종 수정:** 2026-02-14
