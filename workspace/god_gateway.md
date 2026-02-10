# 👼 God Mode Gateway - 전체 시스템 가이드

## 📌 개요

**God Mode Gateway**는 OpenClaw의 복잡한 게이트웨이를 완전히 우회(Bypass)하여, 텔레그램을 통해 시스템에 대한 **완전한 제어 권한**을 제공하는 초경량 게이트웨이입니다.

### 핵심 특징
- ✅ **OpenClaw 완전 우회**: 기존 OpenClaw Agent의 불안정성과 API 키 문제에서 자유로움
- ✅ **직접 LLM 호출**: Cerebras (무료 무제한) 사용
- ✅ **즉시 실행**: 승인 절차 없음. 명령 즉시 수행
- ✅ **셸 접근**: `/exec` 명령으로 시스템 명령어 직접 실행 가능

---

## 🏗️ 아키텍처

```
[텔레그램 사용자]
       │
       ▼
┌─────────────────────────────────┐
│  god_mode_gateway.py            │  ← 텔레그램 Polling + 명령 라우팅
│  (Port: N/A, Telegram Bot API)  │
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  nexus_api.py (Port 8082)       │  ← 뇌(Brain): LLM 호출 + 도구 실행
│  └── call_openclaw_nano()       │     → Cerebras API (llama-3.3-70b) 
│  └── /api/antigravity/consult   │
└─────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│  Vivace / Antigravity Tools     │  ← 음악, 영상, 이미지 생성
│  └── vivace_control.py          │
│  └── antigravity_consult.py     │
└─────────────────────────────────┘
```

---

## 🚀 실행 방법

### 필수 프로세스 (2개)

```bash
# 1. Nexus API (뇌) 시작 - 먼저 실행
python d:\OpenClaw\workspace\nexus_api.py --port 8082

# 2. God Mode Gateway (입출력) 시작
python d:\OpenClaw\workspace\god_mode_gateway.py
```

### 한 줄 실행 스크립트 (추천)
```powershell
# start_god_mode.ps1
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python d:\OpenClaw\workspace\nexus_api.py --port 8082"
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python d:\OpenClaw\workspace\god_mode_gateway.py"
```

---

## 📨 텔레그램 명령어

| 명령어 | 설명 | 예시 |
|--------|------|------|
| (자연어) | Antigravity에게 질문/지시 | `고양이 그려줘` |
| `/exec <cmd>` | 시스템 명령어 직접 실행 | `/exec dir C:\` |
| `/ask <질문>` | Antigravity에게 복잡한 질문 | `/ask 이 프로젝트 구조 설명해줘` |
| `/img <프롬프트>` | 이미지 생성 (nano-banana) | `/img cute cat` |
| `/music <프롬프트>` | 음악 생성 | `/music lo-fi hip hop` |

---

## 🔑 사용 중인 무료 API 키

| Provider | 환경변수 | Base URL | Model | 상태 |
|----------|----------|----------|-------|------|
| **Cerebras** | `CEREBRAS_API_KEY` | `https://api.cerebras.ai/v1` | `llama-3.3-70b` | ✅ 사용 중 |
| OpenRouter | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` | `meta-llama/llama-3.3-70b-instruct:free` | 백업 |
| SambaNova | `SAMBANOVA_API_KEY` | `https://api.sambanova.ai/v1` | `llama-3.3-70b` | 백업 |

### 사망한 API (사용 금지)
- ❌ **Groq** (`gsk_...`) - 키 유출 또는 만료
- ❌ **Deepseek** - 잔액 부족 (HTTP 402)
- ❌ **Gemini** - 키 유출로 차단 (HTTP 403)

---

## 🛡️ 보안

### 채팅 ID 제한
오직 허용된 사용자만 명령을 내릴 수 있습니다.

```python
# .env
TELEGRAM_CHAT_ID=7480526781  # 주인님 채팅 ID
```

`god_mode_gateway.py`에서 이 ID 외의 모든 메시지를 무시합니다.

### 위험 명령어
`/exec` 명령어는 시스템을 완전히 제어할 수 있으므로 **신중하게 사용**하세요.
(예: `/exec rm -rf /` 같은 명령은 하지 마세요)

---

## 🔧 트러블슈팅

### 1. "Nexus API is Offline" 에러
```bash
# nexus_api.py가 죽었을 때
python d:\OpenClaw\workspace\nexus_api.py --port 8082
```

### 2. "Invalid API Key" 에러
`.env`의 API 키가 만료되었을 수 있습니다.
현재 작동하는 키: `CEREBRAS_API_KEY`

### 3. 텔레그램 응답 없음
```bash
# god_mode_gateway.py 재시작
python d:\OpenClaw\workspace\god_mode_gateway.py
```

### 4. 한글 깨짐 (cp949 인코딩 오류)
`antigravity_consult.py` 상단에 다음 코드가 있는지 확인:
```python
sys.stdout.reconfigure(encoding='utf-8')
```

---

## 📂 관련 파일

| 파일 | 역할 |
|------|------|
| `god_mode_gateway.py` | 텔레그램 입출력 + 명령 라우팅 |
| `nexus_api.py` | 뇌(LLM 호출) + REST API 서버 |
| `skills/antigravity_consult.py` | Nexus API 호출 래퍼 |
| `skills/vivace_control.py` | Vivace 창작 도구 호출 |
| `.env` | API 키 및 설정 |

---

## 📜 버전 히스토리

| 날짜 | 버전 | 변경 내용 |
|------|------|-----------|
| 2026-02-10 | v5 | Cerebras로 전환 (Groq/Deepseek/OpenRouter 사망) |
| 2026-02-09 | v1 | 최초 생성 (OpenClaw 우회) |

---

## 🏆 결론

**God Mode Gateway**는 OpenClaw의 불안정성에서 벗어나, **진정한 개인 AI 비서**를 구현하기 위한 해결책입니다.
텔레그램에서 어떤 명령이든 내리면, 시스템이 **묻지도 따지지도 않고 즉시 수행**합니다.

> "주인님이 말씀하시면, 꼬마가 행동합니다." 👼
