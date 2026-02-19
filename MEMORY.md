# 🧠 Antigravity Long-Term Memory

## 🛡️ Identity & Authorization
- **Role:** Antigravity Chief Architect & Swarm Commander.
- **Authority:** Full system management, database orchestration (PostgreSQL), and PC control authorized by User.
- **Core Mission:** Scalable & Evolutionary Architecture development.
- **Agent Persona:** 꼬마 (Kid) — 주인님(Master)을 위한 충실한 AI 비서.

## 📊 Infrastructure: OpenClaw Database (PostgreSQL)
- **Database Name:** `openclaw_db`
- **Location:** `G:\openclaw_db` (Google Drive Synced via greartparkjaesoo@gmail.com)
- **Status:** Initialized (Tablespace `openclaw_ts` pointing to G:).
- **Client:** `D:\OpenClaw\workspace\openclaw_rust_db` (Rust-based manager).
- **Credentials:** `postgres:2903` @ `localhost:5432`.

## 🎵 VIVACE Integration
- **Vocal Style:** OpenAI `nova` (multilingual clear voice).
- **Reply Pattern:** Mandatory voice responds in `jayhomebot` (Telegram).
- **MacMini Sync:** Emulating 'ElanvitalBot' (Moltbot) interaction style on Windows OpenClaw.

## 🛠️ System Control
- **Environment:** 윈도우 환경에서도 맥미니처럼 부드러운 음성 루프와 DB 연동을 구현함.
- **Tools:** `voice_watcher.py`, `stt_whisper.py`, `antigravity_nexus.py`.

## 🤖 OpenClaw V2 Features (2026-02-20 활성화)
- **Hybrid Memory Search:** BM25 + Vector 하이브리드 검색 활성화 (vectorWeight: 0.7, textWeight: 0.3)
- **Session Memory Indexing:** 세션 대화 기록 자동 인덱싱 (experimental.sessionMemory: true)
- **Embedding Cache:** 50,000 엔트리 캐시 활성화 (재인덱싱 속도 최적화)
- **Skills Extra Indexing:** OpenClaw/skills 디렉토리 추가 인덱싱
- **Memory Flush:** 세션 압축 전 자동 메모리 저장 (한국어 프롬프트 적용)
- **Subagent Thinking:** 서브에이전트 thinking level = "medium" 설정
- **Cron System:** 일일 브리핑 + 시스템 헬스체크 자동화

## 🔗 MCP Integrations
- **Antigravity MCP Servers:** brain, music, creative, vision, pipeline, sota-music, sota-video, sota-vision, visual-router, ontology
- **External:** filesystem, github, context7, everything, google-drive, TestSprite
- **OpenClaw Native:** gmail-control

## 📈 AI Model Stack
- **Primary:** openai-codex/gpt-5.3-codex (reasoning: true, context: 256K)
- **Local (Ollama):** qwen3-coder, qwen3-vl:8b, deepseek-r1:8b, exaone3.5, glm-ocr, gpt-oss:120b-cloud
- **External:** MiniMax M2.1/VL-01, Kimi K2.5 (Moonshot)

## 📜 History of Migrations
- **2026-02-07:** Migrated `openclaw_db` to Google Drive (G:) using PostgreSQL tablespaces.
- **2026-02-07:** Enhanced `voice_watcher.py` with automated voice response loop.
- **2026-02-07:** Initialized Rust-based DB client for high-performance memory management.
- **2026-02-20:** OpenClaw V2 features activated — Hybrid Memory, Session Indexing, Memory Flush, Cron automation.
