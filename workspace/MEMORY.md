# MEMORY.md - AI Memory Core (Unified Bridge)

*This file defines how I remember things. Unlike static text files, my real-time memory is handled by high-performance databases.*

## 🧠 Memory Systems

| System | Technology | Purpose | Path/URL |
|--------|------------|---------|----------|
| **Fact Memory** | PostgreSQL | Relational facts, user settings, transaction logs | `postgres://localhost:5432/openclaw_db` |
| **Semantic Memory**| LanceDB | Vectorized knowledge, long-term semantic associations | `D:\OpenClaw\workspace\lancedb` |
| **Dynamic State** | JSON Logs | Short-term heartbeat signals, active task states | `D:\OpenClaw\workspace\HEARTBEAT.md` |

## 🛠️ Accessing My Memory

I do not manually edit this file to "remember" things. Instead, I use the **Memory MCP Server** (`memory_mcp.py`) which provides the following tools:

1.  **`remember_fact(agent_name, content)`**: Stores a specific fact in the PostgreSQL `agent_memory` table.
2.  **`recall_facts(agent_name)`**: Retrieves all stored facts for a specific agent from PostgreSQL.
3.  **`remember_semantic(text, metadata)`**: Vectorizes and stores text in LanceDB for future similarity search.
4.  **`recall_semantic(query, limit)`**: Performs a vector search in LanceDB to find relevant past experiences.

## 📍 Core Principles

- **Relational vs Semantic**: If it's a hard fact (e.g., "User's name is Jay"), use PostgreSQL. If it's an abstract concept or experience (e.g., "The feeling of the last music piece we made"), use LanceDB.
- **Persistence**: These databases are backed up to Google Drive via `google_drive_uploader.py`.
- **Privacy**: No sensitive user credentials should ever be stored in the content fields of these memories.

---

_This file is the "Map" to my brain. The "Brain" itself lives in the data._
