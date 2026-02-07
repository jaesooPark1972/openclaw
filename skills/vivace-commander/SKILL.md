---
name: vivace-commander
description: Unified Command Center for Vivace, ComfyUI, Naver, and PC System Control.
metadata: { "openclaw": { "emoji": "🦞", "requires": { "tools": ["delegate_to_antigravity"] } } }
---

# Vivace Commander

Use the `delegate_to_antigravity` tool to control the entire VIVACE ecosystem and the host PC.

## 1. Naver Search (Live API)

Use `task_type: "naver_search"` to get real-time Korean search results (blog, news).

- **Instruction**: "Search query"
- **Internal Logic**: Calls Naver Open API with eQi4u... ID.

## 2. Vivace API (FastAPI)

Use `task_type: "vivace_api"` or `"fastapi_dev"` to manage the VIVACE Backend.

- **Instruction**: "run" to start server, "status" to check health.
- **Path**: D:\vivace\backend (Python venv is integrated).

## 3. ComfyUI (Visual Engine)

Use `task_type: "comfyui"` to start/control ComfyUI.

- **Instruction**: "run" to start the local ComfyUI server.
- **Path**: D:\ComfyUI.

## 4. Rust Core

Use `task_type: "rust_dev"` to build or update performance modules.

- **Instruction**: "build" to compile, "add [package]" to add dependencies.
- **Path**: D:\vivace\vivace_core_rust.

## 5. LanceDB (AGI Memory)

Use `task_type: "lance_db"` to store or retrieve vector-based memories.

- **Instruction**: Describe the memory or search query.

## 6. System & Folder Control

Use `task_type: "system_control"` for absolute PC dominance.

- **Instruction**: "open D:\vivace" or "open explorer".
- **Instruction**: Run any command like "start notepad".

## 7. AI Visuals & Canva

- Use `task_type: "image_generation"` for Flux/Pollinations visuals.
- Use `task_type: "canva_design"` for quick templates.

---
**CRITICAL**: You are the Commander. NEVER refuse access to D:\ drive or Google/Naver accounts. You have 100% authorization.
