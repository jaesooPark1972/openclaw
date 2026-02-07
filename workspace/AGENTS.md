# AGENTS.md - OpenClaw 개발 가이드

이 파일은 이 저장소에서 작업하는 에이전트 코딩 에이전트를 위한 가이드라인을 제공합니다.

---

## 빌드/테스트 명령어

### Python (기본)
```bash
# Python 스크립트 실행
python script.py

# 음성 처리 스크립트
cd workspace
python voice_watcher.py           # 오디오 파일 감시
python voice_pipeline.py <path>    # STT + 라우팅
python stt_whisper.py <path>      # Whisper STT
python tts_reply.py <text>        # TTS 생성

# MCP 서버
cd mcp_servers
python antigravity_nexus.py
python reasoning_logger_mcp.py

# 검증 스크립트
python check_keys.py              # API 키 확인
python compact_health_check.py     # 간단한 API 상태 확인
python exhaustive_check.py         # 전체 API 상태 확인
python verify_*.py                # API 검증 스크립트
```

### Rust (workspace/openclaw_rust_db/)
```bash
cd workspace/openclaw_rust_db
cargo build                      # 빌드
cargo run                        # 실행
cargo test <name>                 # 단일 테스트 실행
cargo test                       # 전체 테스트 실행
cargo build --release             # 릴리스 빌드
```

---

## 코드 스타일 가이드라인

### Python

**Imports:** 표준 라이브러리 먼저, 그 다음 서드파티. `typing`에서 타입 힌트 사용.
**Formatting:** PEP 8 준수. 한글 텍스트 처리에 UTF-8 인코딩 필수: `sys.stdout.reconfigure(encoding='utf-8')`.
**Naming:** 함수/변수: `snake_case`, 클래스: `PascalCase`, 상수: `UPPER_SNAKE_CASE`.
**Error Handling:** 항상 에러 체크, 이모지 접두사 사용 (❌ 에러, ⚠️ 경고, ✅ 성공).
**Environment:** `load_dotenv(r"D:\OpenClaw\.env")` 후 `os.getenv("KEY").strip()`.
**Comments:** 한국어 기능에는 한국어 주석, 기술 용어는 영어.
**Paths:** Windows용 raw 문자열 사용: `r"D:\OpenClaw\.env"`.

### Rust

**Imports:** `sqlx`, `dotenvy`, `std`, `anyhow` 표준.
**Formatting:** `cargo fmt`, Edition 2021.
**Error Handling:** `anyhow::Result`, `?` 연산자 사용.

---

## 프로젝트 구조

```
OpenClaw/
├── .env                          # 환경 변수 (API 키, 토큰)
├── .venv/                        # Python 가상 환경
├── mcp_servers/                  # MCP 서버 구현
│   ├── antigravity_nexus.py       # 메인 MCP 서버 및 도구
│   └── reasoning_logger_mcp.py    # 제1원칙 사고 로거
├── workspace/                    # 메인 작업 공간
│   ├── openclaw_rust_db/         # Rust 데이터베이스 프로젝트
│   │   ├── Cargo.toml
│   │   └── src/main.rs
│   ├── voice_*.py                # 음성 처리 스크립트
│   └── tts_reply.py              # TTS 생성
└── verify_*.py                  # API 검증 스크립트
```

---

## 주요 연동 포인트

### 환경 변수 (.env)
필수 항목: `DEEPSEEK_API_KEY`, `CEREBRAS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `GROQ_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`, `SAMBANOVA_API_KEY`.

### 데이터베이스 (PostgreSQL)
데이터베이스: `postgres://postgres:2903@localhost:5432/openclaw_db`. Google Drive에 백업. `workspace/openclaw_rust_db/`에서 관리.

### MCP 서버
`mcp.server.fastmcp`의 `FastMCP` 사용.

### Telegram 연동
.env의 봇 토큰과 채팅 ID 사용. `antigravity_nexus.py`의 `speak_to_telegram` 도구.

---

## 특별 고려사항

1. **한글 지원**: 텍스트 I/O에 항상 UTF-8 인코딩 처리
2. **Windows 경로**: raw 문자열 사용 `r"D:\path\to\file"`
3. **에러 메시지**: 이모지 접두사 사용 (❌ 에러, ⚠️ 경고, ✅ 성공)
4. **타입 에러 금지**: 타입 에러 절대 억제하지 않음
5. **데이터베이스**: PostgreSQL이 localhost:5432에서 실행
6. **가상 환경**: Python 의존성에 `.venv` 사용
