# 🦞 OpenClaw - 음성 기반 AI 어시스턴트 및 자동화 플랫폼 (v5.0 Turbo Nano)

OpenClaw는 다중 AI API와 MCP (Model Context Protocol) 서버를 통합한 음성 기반 자동화 플랫폼입니다. v5.0에서는 **Zero-Latency Voice Pipeline**과 **Nano-Mode**를 도입하여 압도적인 반응 속도와 보안을 제공합니다.

---

## 🎯 추구하는 목적 (Vision)

OpenClaw는 다음 목표를 추구합니다:

1. **자연스러운 음성 상호작용** - 텍스트가 아닌 음성으로 자연스럽게 대화하는 AI 어시스턴트
2. **다중 AI API 통합** - OpenAI, Groq, Gemini, DeepSeek, Cerebras, SambaNova 등 다양한 LLM 활용
3. **자동화된 작업 처리** - 음성 명령으로 시스템 제어, 작업 자동화, 정보 수집
4. **유연한 확장성** - MCP 서버를 통한 모듈형 기능 추가
5. **데이터 지속성** - PostgreSQL 데이터베이스를 통한 기록 및 상태 관리

---

## ⚙️ 작동 원리 (Architecture)

OpenClaw는 다음 아키텍처로 동작합니다:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  사용자     │────▶│  Telegram   │────▶│ VIVACE Master│────▶│   LLM API   │
│  (음성)     │    │   Bot       │    │ API (Turbo) │    │ (Nano/Ultra)│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Fast Path   │    │  MCP        │    │ LanceDB/PG  │
│ (Nano Mode) │    │  Servers    │    │  Database   │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 데이터 흐름 (v5.0 Turbo)

1. **음성 입력** → 사용자가 Telegram 봇에 음성 메시지 전송
2. **이벤트 감지** → `voice_watcher.py`가 파일을 감지하여 Master API에 즉각 전송
3. **Turbo Pipeline** → Master API 내부에서 **In-memory STT (Whisper)** 실행
4. **Nano-Mode Routing** → 단순 명령은 최적화된 경로로 즉시 응답 생성 (Nano Path)
5. **Ultra Processing** → 복잡한 작업은 MCP 서버 및 다중 에이전트 협업으로 처리
6. **통합 응답** → 음성(TTS)과 텍스트가 결합된 최종 결과를 Telegram으로 전송

---

## ✨ 주요 기능

### 🎙️ Turbo Voice Pipeline (v5.0)
- **Zero-Latency**: 파일 I/O를 최소화하고 API 레벨에서 상주형 STT 프로세스 활용
- **Whisper Turbo**: OpenAI/Groq Whisper를 병렬로 사용하여 최속의 전사 제공
- **Direct Telegram Feed**: 생성된 미디어 파일을 봇이 직접 스트리밍 전송

### 🧠 Nano-Mode & Master Hub
- **Nano-Mode**: 초경량 응답 경로를 통해 일상적인 명령에 0.5초 이내 반응
- **GPU Monitoring**: 실시간 VRAM 점유율 및 하드웨어 상태 체크 (Nvidia-SMI 연동)
- **Unified Master API**: 모든 창의적 도구(VIVACE, Video)와 시스템 지능을 하나의 허브로 통합

### 🤖 다중 AI API 지원
- **OpenAI**: GPT-4o, GPT-4o-mini, Whisper, TTS
- **Groq**: Llama 3, Whisper (고속 응답)
- **Gemini**: Google Gemini 1.5 Flash/Pro
- **DeepSeek**: DeepSeek-V3
- **Cerebras**: 고성능 추론
- **SambaNova**: 다양한 모델 지원

### 🌐 MCP 서버 통합

#### Antigravity Nexus (`mcp_servers/antigravity_nexus.py`)
- **delegate_to_antigravity**: 고수준 설계 및 창의적 작업 위임
- **system_cmd**: 시스템 명령 실행
- **system_vscode**: VSCode 제어
- **antigravity_opencode**: OpenCode IDE 활성화
- **speak_to_telegram**: TTS 음성을 Telegram으로 전송
- **vivace_generate_music**: AI 음악 생성 (VIVACE API)
- **vivace_generate_video**: AI 비디오 생성 (Wan2.1)

#### Reasoning Logger (`mcp_servers/reasoning_logger_mcp.py`)
- **log_reasoning_step**: 제1원칙 사고 과정 기록

### 📊 데이터베이스 관리
- **PostgreSQL**: 에이전트 기록, 상태 저장
- **Google Drive 백업**: 데이터 지속성 보장
- **Rust 구현**: `workspace/openclaw_rust_db/`에서 안정적인 DB 연동

### 🔍 API 상태 모니터링
- **check_keys.py**: API 키 가용성 확인
- **compact_health_check.py**: 간단한 상태 확인
- **exhaustive_check.py**: 전체 상태 확인
- **full_health_check.py**: 대체 상태 확인
- **verify_*.py**: 개별 API 검증 스크립트

---

## 🚀 설치 및 실행

### 1. 필수 요구사항

- Python 3.12+
- PostgreSQL (localhost:5432)
- Windows OS
- Telegram Bot (BotFather에서 생성)

### 2. 환경 설정

**가상 환경 생성:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**의존성 설치:**
```bash
pip install openai groq edge-tts requests python-dotenv mcp
```

**Rust 빌드:**
```bash
cd workspace/openclaw_rust_db
cargo build
```

### 3. 환경 변수 설정 (.env)

`.env` 파일에 다음 키 설정:

```env
# API Keys
DEEPSEEK_API_KEY=sk-xxx
CEREBRAS_API_KEY=xxx
TELEGRAM_BOT_TOKEN=xxx
TELEGRAM_CHAT_ID=xxx
GROQ_API_KEY=xxx
GEMINI_API_KEY=xxx
OPENAI_API_KEY=sk-xxx
SAMBANOVA_API_KEY=xxx

# Database
DATABASE_URL=postgres://postgres:2903@localhost:5432/openclaw_db
```

### 4. 실행 방법

**음성 감시 시작:**
```bash
cd workspace
python voice_watcher.py
```

**또는 배치 파일 실행:**
```bash
run_watcher.bat
```

**MCP 서버 실행:**
```bash
cd mcp_servers
python antigravity_nexus.py
python reasoning_logger_mcp.py
```

**API 상태 확인:**
```bash
python check_keys.py
python compact_health_check.py
```

---

## 📁 프로젝트 구조

```
OpenClaw/
├── .env                          # 환경 변수 (API 키, 토큰)
├── .venv/                        # Python 가상 환경
├── mcp_servers/                  # MCP 서버 구현
│   ├── antigravity_nexus.py       # 메인 MCP 서버 (시스템 제어, VIVACE)
│   └── reasoning_logger_mcp.py    # 제1원칙 사고 로거
├── workspace/                    # 메인 작업 공간
│   ├── openclaw_rust_db/         # Rust 데이터베이스 프로젝트
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── AGENTS.md                 # 에이전트 개발 가이드
│   ├── voice_watcher.py          # 오디오 파일 감시
│   ├── voice_pipeline.py         # STT + 라우팅 파이프라인
│   ├── voice_router.py           # 음성 명령 라우터
│   ├── stt_whisper.py          # Whisper STT 클라이언트
│   ├── tts_reply.py             # TTS 생성 (OpenAI + Edge)
│   └── verify_*.py             # API 검증 스크립트
├── check_keys.py                # API 키 확인
├── *_health_check.py           # API 상태 확인
└── README.md                   # 이 파일
```

---

## 🔧 개발 가이드

자세한 개발 가이드는 `workspace/AGENTS.md`를 참조하세요.

**주요 포인트:**
- UTF-8 인코딩 필수 (한글 지원)
- Windows 경로는 raw 문자열 사용: `r"D:\path\to\file"`
- 에러 메시지에 이모지 접두사 사용 (❌ 에러, ⚠️ 경고, ✅ 성공)
- 타입 에러 절대 억제 금지

---

## 🤝 기여 방법

기여를 환영합니다! 다음 단계를 따라주세요:

1. 포크 (Fork) 이 저장소
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 푸시 (`git push origin feature/AmazingFeature`)
5. 풀 리퀘스트 (Pull Request) 개설

---

## 📄 라이선스

이 프로젝트는 [라이선스 이름] 라이선스 하에 라이선스되었습니다.

---

## 👥 연락처

프로젝트 관리자: [이름/연락처]

---

## 🙏 감사의 말씀

이 프로젝트는 다음 오픈소스 프로젝트의 도움을 받았습니다:
- [OpenAI](https://openai.com/) - GPT, Whisper, TTS API
- [Groq](https://groq.com/) - 고속 LLM 추론
- [Google](https://ai.google.dev/) - Gemini API
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP 서버 프레임워크
- [Whisper](https://github.com/openai/whisper) - 음성 텍스트 변환
- [Edge-TTS](https://github.com/rany2/edge-tts) - Microsoft Edge TTS

---

**OpenClaw: 음성으로 더 자연스러운 AI와의 상호작용을 위해** 🦞
