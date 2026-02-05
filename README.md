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

# 🦞 OpenClaw (Antigravity System) 한국어 매뉴얼

**Updated:** 2026.02.05
**Author:** Antigravity AI

이 문서는 OpenClaw 시스템을 처음 사용하는 사용자를 위한 **공식 한글 가이드**입니다.

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
    - **주의:** 단톡방에서는 봇을 부를 때 **멘션(@(사용자 봇 이름))**을 하거나 답변을 해줘야 반응합니다.

#### **주요 명령어:**

- `/start` : 봇을 깨우고 인사를 나눕니다.
- `/restart` : 봇이 응답하지 않을 때 재시작합니다. (문제 해결용)
- `/clear` : 대화 기억을 지웁니다. (새로운 주제로 이야기하고 싶을 때)

---

## 3. 🧠 무엇을 할 수 있나요? (Capabilities)

### **1. AI 비서 (Powered by Google Gemini 2.0)**

- **질문/답변:** "양자컴퓨터 원리가 뭐야?", "이 영어 문장 한국어로 번역해줘"
- **문서 요약:** 아주 긴 글이나 뉴스 기사를 복사해 붙여넣으면 핵심만 요약해줍니다. (100만 자까지 처리 가능)

### **2. 실시간 웹 검색 (Brave Search)**

- **명령 예시:** "지금 비트코인 시세 검색해줘", "최신 아이폰 출시일 언제야?"
- **특징:** AI가 학습한 옛날 정보가 아니라, **실시간 인터넷 검색**을 통해 최신 정보를 가져옵니다.

### **3. PC 제어 및 코딩 (Code Interpreter)**

- **파일 관리:** "내 프로젝트 폴더에 있는 파일 리스트 보여줘"
- **코드 수정:** "이 파이썬 파일에서 에러 나는 부분 찾아서 고쳐줘" (개발자용 기능)

---

## 4. ⚠️ 문제 발생 시 해결법 (Troubleshooting)

### **Q. 텔레그램 봇이 대답을 안 해요.**

- **체크 1:** 터미널 창(PowerShell)이 켜져 있나요? 실수로 껐다면 [1단계]부터 다시 시작하세요.
- **체크 2:** 텔레그램 채팅방에 `/restart`라고 입력해보세요.

### **Q. 답변이 계속 반복되거나 이상한 말을 해요.**

- 텔레그램에서 `/clear`를 입력해서 AI의 기억을 초기화하세요.
- 그래도 안 되면 터미널을 끄고(`Ctrl + C`) 다시 실행하세요.

### **Q. "Unauthorized" 오류가 떠요.**

- 현재 설정상 뜨지 않아야 정상입니다. 만약 뜬다면 `openclaw.json` 설정 파일이 변경되었는지 확인해야 합니다. (기본 설정: 누구나 사용 가능)

---

## 5. 🛠️ 설정 정보 (Configuration)

이 정보는 고급 사용자를 위한 기술적인 내용입니다.

- **설치 경로:** `(현재 폴더)`
- **설정 파일:** `~/.openclaw/openclaw.json` (메인 설정)
- **환경 변수:** `~/.openclaw/.env` (API 키 저장소)

### **사용 중인 AI 모델:**

1. **메인 (Primary):** `google/gemini-2.0-flash` (대용량 처리, 똑똑함)
2. **백업 (Fallback):**
   - `groq/llama-3.3` (초고속 답변)
   - `deepseek/chat` (가성비)
