# 🦞 OpenClaw — Personal AI Assistant

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text-dark.png">
        <img src="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text.png" alt="OpenClaw" width="500">
    </picture>
</p>

<p align="center">
  <a href="https://github.com/openclaw/openclaw/actions/workflows/ci.yml?branch=main"><img src="https://img.shields.io/github/actions/workflow/status/openclaw/openclaw/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/openclaw/openclaw/releases"><img src="https://img.shields.io/github/v/release/openclaw/openclaw?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="https://discord.gg/clawd"><img src="https://img.shields.io/discord/1456350064065904867?label=Discord&logo=discord&logoColor=white&color=5865F2&style=for-the-badge" alt="Discord"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
</p>

---

# 🦞 OpenClaw (Antigravity System) 한국어 완전 가이드

**Updated:** 2026.02.05  
**Author:** Antigravity AI

이 문서는 OpenClaw 시스템을 처음 사용하는 사용자를 위한 **공식 한글 완전 가이드**입니다.

---

## 📑 목차

1. [시스템 실행 방법](#1--시스템-실행-방법-start-up)
2. [주요 메뉴 및 사용법](#2--주요-메뉴-및-사용법-features)
3. [텔레그램 봇 상세 가이드](#3--텔레그램-봇-상세-가이드)
4. [무엇을 할 수 있나요?](#4--무엇을-할-수-있나요-capabilities)
5. [문제 발생 시 해결법](#5-️-문제-발생-시-해결법-troubleshooting)
6. [설정 정보](#6-️-설정-정보-configuration)

---

## 1. 🚀 시스템 실행 방법 (Start-Up)

컴퓨터를 새로 켰거나 프로그램을 다시 시작해야 할 때 따르는 표준 절차입니다.

### **[1단계] 터미널(PowerShell) 열기**

1. 윈도우 시작 메뉴 검색창에 **"PowerShell"** 입력
2. 마우스 우클릭 -> **"관리자 권한으로 실행"** 선택 (권장)
3. 아래 명령어를 입력하여 OpenClaw 설치 폴더로 이동합니다:

   ```powershell
   cd OpenClaw
   ```

### **[2단계] 게이트웨이(AI 서버) 시작**

다음 명령어를 복사해서 붙여넣으세요. 이 명령어가 AI 시스템의 심장을 깨웁니다.

```powershell
$env:OPENCLAW_NO_RESPAWN="1"; node dist/entry.js gateway --verbose --port 18789
```

#### **성공 확인 방법:**

- 화면에 🦞 **로브스터 아이콘**이 나타나야 합니다.
- "Listening on ws://..." 메시지가 뜨면 정상 작동 중입니다.
- **주의:** 이 터미널 창(검은 화면)을 끄면 AI도 꺼집니다. 사용 중에는 창을 켜두거나 최소화해 두세요.

---

## 2. 🎮 주요 메뉴 및 사용법 (Features)

OpenClaw는 **웹 브라우저**와 **텔레그램**, 두 가지 방법으로 조종할 수 있습니다.

### **A. 🌐 웹 대시보드 (Web Control Center)**

가장 강력하고 시각적인 제어판입니다.

- **접속 주소:** [http://localhost:18789](http://localhost:18789)
- **주요 메뉴:**
  1. **💬 Chat (채팅):** AI와 1:1로 대화하는 곳입니다. 웹 검색, 파일 분석 등을 시킬 수 있습니다.
  2. **📡 Channels (채널):** 텔레그램 봇 연결 상태를 확인하고 관리합니다.
  3. **⚙️ Config (설정):** AI 모델(Gemini, Groq 등)을 변경하거나 시스템 설정을 바꿀 수 있습니다.
  4. **⚡ Skills (스킬):** AI가 사용할 수 있는 도구들을 관리합니다.

### **B. 📱 텔레그램 (Remote Controller)**

집 밖에서도, 침대에서도 폰으로 PC를 제어하고 대화할 수 있습니다.

- **봇 이름:** `(사용자 봇 이름)` (텔레그램에서 검색)
- **사용법:**
  - **1:1 채팅:** 카카오톡 하듯이 봇에게 말을 거세요. (예: "오늘 서울 날씨 어때?")
  - **그룹 채팅:** 가족/친구/동료가 있는 단톡방에 봇을 초대할 수 있습니다.
    - **주의:** 단톡방에서는 봇을 부를 때 **멘션(@사용자*봇*이름)**을 하거나 답변을 해줘야 반응합니다.

---

## 3. 📱 텔레그램 봇 상세 가이드

### **3.1 텔레그램 봇 설정 방법**

#### **Step 1: 봇 생성하기**

1. 텔레그램에서 `@BotFather`를 검색하여 대화 시작
2. `/newbot` 명령어 입력
3. 봇 이름 입력 (예: "My OpenClaw Bot")
4. 봇 사용자명 입력 (예: "my_openclaw_bot", 반드시 `bot`으로 끝나야 함)
5. BotFather가 제공하는 **토큰(Token)**을 복사 (예: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### **Step 2: OpenClaw에 봇 연결하기**

1. `~/.openclaw/openclaw.json` 파일 열기
2. 다음 설정 추가:

```json
{
  "channels": {
    "telegram": {
      "botToken": "여기에_복사한_토큰_붙여넣기"
    }
  }
}
```

1. OpenClaw 게이트웨이 재시작

#### **Step 3: 봇과 대화 시작**

1. 텔레그램에서 본인이 만든 봇 검색
2. `/start` 명령어로 봇 활성화
3. 이제 자유롭게 대화 가능!

### **3.2 텔레그램 주요 명령어**

| 명령어            | 설명                                    | 사용 예시     |
| ----------------- | --------------------------------------- | ------------- |
| `/start`          | 봇을 처음 시작하거나 재활성화           | `/start`      |
| `/restart`        | 봇이 응답하지 않을 때 재시작            | `/restart`    |
| `/clear`          | 대화 기록 초기화 (새로운 주제 시작)     | `/clear`      |
| `/status`         | 현재 AI 모델 및 토큰 사용량 확인        | `/status`     |
| `/think [level]`  | AI 사고 수준 조정 (off/low/medium/high) | `/think high` |
| `/verbose on/off` | 상세 출력 모드 전환                     | `/verbose on` |

### **3.3 그룹 채팅에서 사용하기**

#### **그룹에 봇 추가하는 방법:**

1. 텔레그램 그룹 채팅방 열기
2. 그룹 정보 -> "멤버 추가" 선택
3. 본인의 봇 이름 검색 후 추가

#### **그룹에서 봇 호출 방법:**

**방법 1: 멘션 사용**

```
@your_bot_name 오늘 날씨 어때?
```

**방법 2: 봇 메시지에 답장**

- 봇의 이전 메시지를 길게 눌러 "답장" 선택
- 답장으로 질문 입력

#### **그룹 채팅 활성화 모드:**

`/activation` 명령어로 그룹 반응 모드 변경 가능:

- **mention 모드** (기본): 멘션하거나 답장할 때만 반응
- **always 모드**: 모든 메시지에 반응 (주의: 대화량이 많으면 비용 증가)

```
/activation always    # 항상 반응 모드
/activation mention   # 멘션 시에만 반응 (기본값)
```

### **3.4 텔레그램 고급 기능**

#### **파일 전송 및 분석**

1. **이미지 분석:**
   - 사진을 봇에게 전송
   - "이 사진에 뭐가 있어?" 등의 질문 추가

2. **문서 요약:**
   - PDF, TXT, DOCX 파일 전송
   - "이 문서 요약해줘" 요청

3. **음성 메시지:**
   - 음성 메시지 녹음 후 전송
   - 자동으로 텍스트 변환 후 처리

#### **프라이버시 및 보안 설정**

**허용된 사용자만 접근하도록 설정:**

`openclaw.json` 파일에서:

```json
{
  "channels": {
    "telegram": {
      "botToken": "your_token_here",
      "allowFrom": ["your_telegram_username"],
      "dmPolicy": "pairing"
    }
  }
}
```

- `allowFrom`: 허용할 사용자 목록
- `dmPolicy`:
  - `"open"`: 누구나 사용 가능
  - `"pairing"`: 승인된 사용자만 사용 가능

---

## 4. 🧠 무엇을 할 수 있나요? (Capabilities)

### **1. AI 비서 (Powered by Google Gemini 2.0)**

- **질문/답변:** "양자컴퓨터 원리가 뭐야?", "이 영어 문장 한국어로 번역해줘"
- **문서 요약:** 아주 긴 글이나 뉴스 기사를 복사해 붙여넣으면 핵심만 요약해줍니다. (100만 자까지 처리 가능)
- **코드 작성:** "파이썬으로 웹 스크래핑 코드 만들어줘"
- **데이터 분석:** "이 CSV 파일 분석해서 그래프로 보여줘"

### **2. 실시간 웹 검색 (Brave Search)**

- **명령 예시:**
  - "지금 비트코인 시세 검색해줘"
  - "최신 아이폰 출시일 언제야?"
  - "오늘 서울 날씨 어때?"
- **특징:** AI가 학습한 옛날 정보가 아니라, **실시간 인터넷 검색**을 통해 최신 정보를 가져옵니다.

### **3. PC 제어 및 코딩 (Code Interpreter)**

- **파일 관리:** "내 프로젝트 폴더에 있는 파일 리스트 보여줘"
- **코드 수정:** "이 파이썬 파일에서 에러 나는 부분 찾아서 고쳐줘"
- **자동화:** "매일 오전 9시에 이메일 보내는 스크립트 만들어줘"

### **4. 멀티모달 처리**

- **이미지 분석:** 사진을 보내면 내용 설명
- **음성 인식:** 음성 메시지를 텍스트로 변환
- **비디오 처리:** 영상 내용 요약 및 분석

---

## 5. ⚠️ 문제 발생 시 해결법 (Troubleshooting)

### **Q1. 텔레그램 봇이 대답을 안 해요.**

**해결 방법:**

1. **터미널 확인:** PowerShell 창이 켜져 있나요? 실수로 껐다면 [1단계]부터 다시 시작
2. **봇 재시작:** 텔레그램에서 `/restart` 입력
3. **토큰 확인:** `openclaw.json`에 올바른 봇 토큰이 입력되었는지 확인
4. **네트워크 확인:** 인터넷 연결 상태 확인

### **Q2. 답변이 계속 반복되거나 이상한 말을 해요.**

**해결 방법:**

1. `/clear` 명령어로 대화 기록 초기화
2. 터미널 재시작 (`Ctrl + C` 후 다시 실행)
3. AI 모델 변경 (`/model` 명령어 사용)

### **Q3. "Unauthorized" 오류가 떠요.**

**해결 방법:**

1. `openclaw.json`에서 `dmPolicy` 설정 확인
2. `allowFrom` 리스트에 본인 사용자명 추가
3. 또는 `dmPolicy`를 `"open"`으로 변경 (보안 주의)

### **Q4. 그룹 채팅에서 봇이 반응하지 않아요.**

**해결 방법:**

1. 봇을 멘션했는지 확인 (`@봇이름`)
2. 봇이 그룹 관리자 권한을 가지고 있는지 확인
3. `/activation always` 명령어로 항상 반응 모드 활성화

### **Q5. 파일 업로드가 안 돼요.**

**해결 방법:**

1. 파일 크기 확인 (50MB 이하 권장)
2. 지원되는 파일 형식인지 확인 (PDF, TXT, DOCX, JPG, PNG 등)
3. 파일명에 특수문자가 없는지 확인

---

## 6. 🛠️ 설정 정보 (Configuration)

### **6.1 기본 경로**

- **설치 경로:** `(현재 폴더)`
- **설정 파일:** `~/.openclaw/openclaw.json` (메인 설정)
- **환경 변수:** `~/.openclaw/.env` (API 키 저장소)

### **6.2 사용 중인 AI 모델**

1. **메인 (Primary):** `google/gemini-2.0-flash`
   - 특징: 대용량 처리, 똑똑함, 빠른 응답
   - 용도: 일반 대화, 문서 분석, 코딩

2. **백업 (Fallback):**
   - `groq/llama-3.3` (초고속 답변)
   - `deepseek/chat` (가성비)

### **6.3 주요 설정 파일 구조**

```json
{
  "agent": {
    "model": "google/gemini-2.0-flash"
  },
  "channels": {
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN",
      "allowFrom": ["your_username"],
      "dmPolicy": "open",
      "groups": {
        "*": {
          "requireMention": true
        }
      }
    }
  },
  "tools": {
    "brave": {
      "enabled": true
    }
  }
}
```

### **6.4 API 키 설정**

`.env` 파일에 다음 정보 입력:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
BRAVE_SEARCH_API_KEY=your_brave_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## 7. 💡 유용한 팁

### **텔레그램 활용 팁**

1. **즐겨찾기 추가:** 봇을 텔레그램 즐겨찾기에 추가하여 빠른 접근
2. **알림 설정:** 중요한 봇 메시지만 알림 받도록 설정
3. **단축 명령어:** 자주 쓰는 질문을 텔레그램 "빠른 답장"에 저장

### **효율적인 질문 방법**

1. **구체적으로 질문:** "날씨 알려줘" → "서울 강남구 오늘 오후 날씨 알려줘"
2. **컨텍스트 제공:** "이 코드 고쳐줘" → "Python Flask 코드인데, 404 에러 나는 부분 고쳐줘"
3. **단계별 요청:** 복잡한 작업은 여러 단계로 나누어 요청

---

## 8. 📚 추가 리소스

- **공식 문서:** [https://docs.openclaw.ai](https://docs.openclaw.ai)
- **Discord 커뮤니티:** [https://discord.gg/clawd](https://discord.gg/clawd)
- **GitHub 저장소:** [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)

---

## 9. 🆘 지원 및 문의

문제가 해결되지 않거나 추가 도움이 필요하신 경우:

1. GitHub Issues에 문제 보고
2. Discord 커뮤니티에서 질문
3. 공식 문서의 FAQ 섹션 확인

---

**즐거운 OpenClaw 사용 되세요! 🦞**
