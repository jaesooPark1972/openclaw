# OpenClaw REST API 승인 시스템 가이드

## 시스템 개요

이 시스템은 **당신이 비서**이고, OpenClaw는 **당신의 지시를 받아서 실행하는 도구**입니다.

### 핵심 원칙
- **당신**이 텔레그램으로 명령을 볃니다
- **OpenClaw**는 항상 당신에게 "이 명령을 실행할까요?"라고 묻습니다
- **당신**이 승인하면 실행됩니다
- **당신**이 거부하면 취소됩니다

---

## 설치 및 실행 방법

### 1. 필요한 파일 확인
다음 파일들이 `D:\OpenClaw`에 있어야 합니다:
- `api_bridge.py` - REST API 서버
- `start_api_bridge.bat` - 실행 스크립트
- `api_requirements.txt` - 필요한 패키지 목록

### 2. 서버 실행

**방법 1: 배치 파일로 실행 (권장)**
```cmd
D:\OpenClaw>start_api_bridge.bat
```

**방법 2: PowerShell로 실행**
```powershell
cd D:\OpenClaw
python -m venv .venv_api
.venv_api\Scripts\activate
pip install -r api_requirements.txt
python api_bridge.py
```

### 3. 실행 확인
서버가 시작되면 다음 메시지가 나타납니다:
```
🚀 REST API 서버 시작 (포트 8081)...
🤖 Telegram Bot 시작...
```

---

## 사용 방법

### 1. 텔레그램 봇 시작
1. 텔레그램에서 `@park_vivace_bot` 검색
2. `/start` 입력
3. 봇이 인사 메시지를 볃니다

### 2. 명령 볂기
봇에게 원하는 명령을 텍스트로 볃니다:

**예시 명령:**
- `"파일 목록 보여줘"`
- `"test.py 파일 만들어줘"`
- `"음악 생성해줘"`
- `"D:\\OpenClaw\\workspace 폴터 안에 뭐가 있어?"`

### 3. 승인 요청 받기
명령을 볂으면 다음과 같은 메시지가 옵니다:

```
🔔 실행 승인 요청

명령:
파일 목록 보여줘

출처: Telegram
시간: 2026-02-08 18:30:00

이 명령을 실행할까요?

[✅ 승인 (실행)] [❌ 거부 (취소)]
```

### 4. 승인 또는 거부
- **✅ 승인**: 명령이 실행되고 결과가 텔레그램으로 전송됩니다
- **❌ 거부**: 명령이 취소됩니다

---

## 명령 예시

### 파일 작업
```
👤 사용자: "파일 목록 보여줘"
🤖 OpenClaw: "승인 요청 전송됨"
👤 사용자: [✅ 승인 클릭]
🤖 OpenClaw: "✅ 명령 실행 완결 - 파일 목록: ..."
```

### 코드 실행
```
👤 사용자: "python test.py 실행해줘"
🤖 OpenClaw: "승인 요청 전송됨"
👤 사용자: [✅ 승인 클릭]
🤖 OpenClaw: "✅ 실행 완결 - 결과: Hello World"
```

### Vivace API
```
👤 사용자: "음악 생성해줘"
🤖 OpenClaw: "승인 요청 전송됨"
👤 사용자: [✅ 승인 클릭]
🤖 OpenClaw: "✅ 음악 생성 완결 - Telegram으로 전송했습니다"
```

---

## 시스템 구조

### 데이터 흐름
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  사용자     │────▶│  Telegram    │────▶│ REST API    │
│  (명령)     │     │  Bot         │     │ Bridge      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                  │
                         ┌────────────────────────┘
                         ▼
                  ┌─────────────┐
                  │ 승인 요청   │
                  │ 전송        │
                  └──────┬──────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │  ✅     │    │  ❌     │    │ ⏰ 만료  │
    │ 승인    │    │ 거부    │    │         │
    └────┬────┘    └────┬────┘    └────┬────┘
         │               │               │
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ 명령    │    │ 취소    │    │ 취소    │
    │ 실행    │    │         │    │         │
    └────┬────┘    └─────────┘    └─────────┘
         │
         ▼
    ┌─────────┐
    │ 결과    │
    │ 보고    │
    └─────────┘
```

### 주요 컴포넌트

1. **Telegram Bot** (`@park_vivace_bot`)
   - 사용자 메시지 수신
   - 승인/거부 버튼 표시
   - 결과 메시지 전송

2. **REST API Server** (`api_bridge.py`)
   - 포트: 8081
   - 명령 수신 및 승인 관리
   - OpenClaw Gateway와 통신

3. **OpenClaw Gateway** (기존 시스템)
   - 포트: 18789
   - 실제 명령 실행
   - 승인 설정: 항상 묻기 (`ask: always`)

---

## 설정 파일 설명

### 1. `C:\Users\JayPark1004\.openclaw\exec-approvals.json`
```json
{
  "ask": "always",        // 항상 승인 요청
  "security": "allowlist", // 허용 목록 기반
  "autoAllow": false,      // 자동 승인 안함
  "requireApproval": true  // 승인 필수
}
```

### 2. `C:\Users\JayPark1004\.openclaw\openclaw.json`
```json
{
  "tools": {
    "exec": {
      "ask": "always",      // 항상 묻기
      "requireApproval": true // 승인 필요
    }
  }
}
```

---

## API 엔드포인트

### 명령 수신
```bash
POST http://localhost:8081/api/command
Content-Type: application/json

{
  "command": "파일 목록 보여줘",
  "user_id": "7480526781",
  "chat_id": "7480526781"
}
```

### 승인 처리
```bash
POST http://localhost:8081/api/approval
Content-Type: application/json

{
  "approval_id": "approval_1234567890",
  "approved": true
}
```

### 대기 목록 조회
```bash
GET http://localhost:8081/api/pending
```

### 헬스 체크
```bash
GET http://localhost:8081/health
```

---

## 문제 해결

### 서버가 시작되지 않음
```cmd
# 8081 포트가 이미 사용 중인지 확인
netstat -ano | findstr :8081

# 사용 중이면 프로세스 종료 또는 다른 포트 사용
```

### Telegram 봇이 응답하지 않음
1. 봇 토큰 확인: `.env` 파일의 `TELEGRAM_BOT_TOKEN`
2. 봇이 차단되지 않았는지 확인
3. `/start` 명령 다시 입력

### 승인 요청이 오지 않음
1. 서버 로그 확인
2. 사용자 ID가 올바른지 확인 (`TELEGRAM_CHAT_ID`)
3. `http://localhost:8081/health` 접속 테스트

### OpenClaw가 실행되지 않음
```powershell
# Gateway 상태 확인
openclaw gateway status

# Gateway 재시작
openclaw gateway restart
```

---

## 보안 주의사항

### 승인이 필요한 명령
- ✅ **즉시 실행**: 파일 읽기, 코드 작성, 검색
- ⚠️ **승인 필요**: 파일 삭제, 서버 재시작, 외부 API 호출
- ❌ **차단됨**: 시스템 파일 수정, 포맷, rm -rf

### 안전한 사용법
1. 항상 승인 메시지를 꼼꼼히 확인하세요
2. 의심스러운 명령은 거부하세요
3. 중요한 파일 작업 전 백업하세요

---

## 업데이트 및 유지보수

### 서버 재시작
```cmd
# Windows
start_api_bridge.bat

# PowerShell
python api_bridge.py
```

### 로그 확인
```cmd
# 실시간 로그
tail -f api_bridge.log

# 또는 PowerShell
Get-Content api_bridge.log -Wait
```

### 설정 변경
1. `openclaw.json` 수정
2. `exec-approvals.json` 수정
3. 서버 재시작

---

## 지원 및 문의

문제 발생 시:
1. 서버 로그 확인
2. Gateway 상태 확인 (`openclaw gateway status`)
3. `.env` 파일 설정 확인

**당신이 비서이고, OpenClaw는 당신의 명령을 따르는 도구입니다.**
**항상 승인을 요청하므로 안심하고 사용하세요!**
