# 🦞 OpenClaw God Gateway Nexus v5.1.0-ML - Manual

## Overview

**God Gateway Nexus v5.1.0-ML** is the complete AI Operating System for OpenClaw, integrating Machine Learning (Training/Inference) capabilities with traditional system orchestration.

```
┌─────────────────────────────────────────────────────────────┐
│               🦞 GOD GATEWAY NEXUS v5.1.0-ML              │
│                (Complete AI Operating System)               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │
│  │Vector DB│ │PostgreSQL│ │ML Engine│ │   API Server    │  │
│  │LanceDB  │ │  (SQL)   │ │(PyTorch)│ │   (FastAPI)     │  │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────────┬────────┘  │
│       │            │           │               │          │
│       └────────────┴───────────┴───────────────┘          │
│                          │                                  │
│                    ┌──────┴──────┐                          │
│                    │ Unified API  │                          │
│                    │   (Port 8095)│                          │
│                    └──────┬──────┘                          │
│                           │                                  │
│    ┌──────────┬──────────┼──────────┬──────────┐          │
│    │          │          │          │          │          │
│    ▼          ▼          ▼          ▼          ▼          │
│ ┌──────┐ ┌──────┐ ┌────────┐ ┌────────┐ ┌────────┐       │
│ │Antigravity│ │Secretary│ │  AGen  │ │  Skills│ │Workflows│       │
│ │ Nexus │ │  API  │ │Pipeline│ │        │ │        │       │
│ └──────┘ └──────┘ └────────┘ └────────┘ └────────┘       │
│    │          │          │          │          │          │
│    ▼          ▼          ▼          ▼          ▼          │
│ ┌──────┐ ┌──────┐ ┌────────┐ ┌──────────────────────┐    │
│ │Telegram│ │Tasks │ │Music/  │ │OpenClaw Core        │    │
│ │Vivace │ │OCR   │ │Video   │ │                      │    │
│ └──────┘ └──────┘ └────────┘ └──────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Installation & Setup

### Prerequisites
- Python 3.10+
- PyTorch / TensorFlow (optional for ML features)
- PostgreSQL (optional)
- Everything Search (Windows desktop search)
- LanceDB (vector storage)

### Install Dependencies
```bash
pip install fastapi uvicorn lancedb sentence-transformers psycopg2-binary
```

### Install ML Dependencies
```bash
pip install -r requirements_ml.txt
```

### Run God Gateway
```bash
# Method 1: Direct
python mcp_servers/god_gateway_nexus_v5.py

# Method 2: Via Launcher (Recommended)
D:\OpenClaw\workspace\god_gateway\run_god_gateway.bat
```

---

## 2. API Endpoints

### Base URL: `http://localhost:8095`

| Category | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| **System** | `/` | GET | API Status & Info |
| | `/health` | GET | Health Check (ML/DB) |
| **ML System** | `/api/ml/system` | GET | Frameworks & GPU Info |
| | `/api/ml/resources` | GET | CPU/RAM/GPU Usage |
| **Model Ops** | `/api/ml/model/register` | POST | Register new model |
| | `/api/ml/model/load` | POST | Load model into memory |
| | `/api/ml/model/export/onnx` | POST | Export to ONNX |
| **Training** | `/api/ml/training/start` | POST | Start training job |
| | `/api/ml/training/status/{job}` | GET | Check training status |
| **Inference** | `/api/ml/inference` | POST | Run inference |
| **Memory** | `/api/memory/save` | POST | Save to Vector DB |
| | `/api/memory/search` | GET | Semantic Search |
| **Memory** | `/memory/add` | POST | Add memory to vector DB |
| | `/memory/search` | POST | Search memories |
| | `/memory/index-domain` | POST | Index domain files |
| **Search** | `/search/everything` | GET | Everything file search |
| **Workflow** | `/workflow/run` | POST | Execute workflow |
| **Domain** | `/domain/{name}/status` | GET | Get domain status |
| | `/domain/{name}/execute` | POST | Execute in domain |

---

## 3. MCP Tools Available

### Everything Search Tools
```python
everything_search(query: str, limit: int = 50)
everything_search_code(query: str, extensions: str = "py,ts,js")
everything_find_large_files(min_size_mb: int = 100)
```

### Engram Memory Tools
```python
engram_remember(content: str, tags: str = "", context: str = "")
engram_recall(query: str, n_results: int = 5)
engram_search_code(function_name: str, language: str = "python")
```

### God Gateway Tools
```python
god_gateway_search(query: str, mode: str = "hybrid")
god_gateway_index_domain(domain: str)
god_gateway_get_status()
```

### AGen Pipeline Tools
```python
agenz_music_create_full_song(title, theme, genre, language, bpm)
agenz_generate_image(prompt, width, height)
agenz_generate_video(prompt)
vivace_music_generate(genre, lyrics, title)
vivace_video_generate(prompt)
agenz_plan_storyboard(song_context, genre)
```

---

## 4. Usage Examples

### Example 1: Semantic Search
```bash
curl -X POST "http://localhost:8085/memory/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "FastAPI best practices", "top_k": 5}'
```

### Example 2: Index OpenClaw Domain
```bash
curl -X POST "http://localhost:8085/memory/index-domain?domain=openclaw"
```

### Example 3: Everything Search via MCP
```python
# In MCP tool call
await everything_search("*.py config", limit=20)
```

### Example 4: Create Music
```python
await agenz_music_create_full_song(
    title="Neon Dreams",
    theme="cyberpunk city night",
    genre="synthwave",
    language="en"
)
```

---

## 5. Domain Configuration

```python
CONFIG = {
    "openclaw": r"D:\OpenClaw",       # Main project
    "vivace": r"F:\Vivace",           # Audio/Video engine
    "comfyui": r"F:\ComfyUI-Easy-Install",  # Image generation
    "agen": r"F:\AGen",              # AI generation pipeline
    "rust": r"D:\Rust",              # Rust projects
}
```

---

## 6. Integration with OpenClaw Agent

### Update OpenClaw Config
```json
{
  "skills": [
    "D:\\OpenClaw\\mcp_servers\\god_gateway_tools.py",
    "D:\\OpenClaw\\mcp_servers\\agen_pipeline_mcp.py",
    "D:\\OpenClaw\\workspace\\secretary\\secretary_mcp.py",
    "D:\\OpenClaw\\mcp_servers\\antigravity_nexus.py"
  ]
}
```

### Natural Language Commands
```
"Find all Python files with FastAPI" → everything_search_code()
"Remember this conversation" → engram_remember()
"Generate a K-pop song about love" → agenz_music_create_full_song()
"Create cyberpunk image" → agenz_generate_image()
```

---

## 7. System Architecture

### Ports Overview
| Service | Port | Status |
|---------|------|--------|
| Vivace API | 8080 | HTTP |
| REST API Bridge | 8081 | HTTP |
| Nexus API | 8082 | HTTP |
| **God Gateway** | **8085** | **HTTP** |
| Secretary Orchestrator | 8091 | HTTP |
| Qwen TTS Server | 8092 | HTTP |
| ComfyUI | 8188 | HTTP |
| OpenClaw Gateway | 18789 | WebSocket |

---

## 8. Troubleshooting

### Vector DB Not Initialized
```bash
# Check if directory exists
ls -la D:\OpenClaw\workspace\vector_db

# Recreate
mkdir D:\OpenClaw\workspace\vector_db
```

### Everything Search Not Working
```bash
# Verify Everything.exe exists
dir "C:\Program Files\Everything\Everything.exe"

# Download from: https://www.voidtools.com/
```

### PostgreSQL Connection Failed
```bash
# Check if PostgreSQL is running
tasklist /FI "IMAGENAME eq postgres.exe"

# Start PostgreSQL service
net start postgresql-x64-16
```

---

## 9. Commands Quick Reference

### File Search
```
/search "*.py"              → Everything search
/index openclaw            → Index domain
```

### Memory
```
/remember [content]         → Store memory
/recall [query]            → Search memories
```

### Creative
```
/song title:theme:genre    → Generate music
/image prompt              → Generate image
/video prompt              → Generate video
```

### System
```
/status                    → All services status
/restart [service]         → Restart service
```

---

## 10. Support

- **Issues**: GitHub Issues
- **Docs**: http://localhost:8085/docs
- **Telegram**: @OpenClawBot

---

**Version**: 4.0.0
**Last Updated**: 2026-02-10
**Maintainer**: OpenClaw Architecture Team
