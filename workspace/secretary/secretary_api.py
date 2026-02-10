import os
import time
import json
import sqlite3
import requests
import threading
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import subprocess

# --- Config ---
OLLAMA_URL = "http://localhost:11434"
TTS_SERVER_URL = "http://localhost:8092"  # Dedicated Qwen3-TTS Server
DB_PATH = r"D:\OpenClaw\workspace\secretary\tasks.db"
GPU_LOCK_FILE = r"D:\OpenClaw\workspace\secretary\gpu.lock"

app = FastAPI(title="OpenClaw Secretary Core (Orchestrator)")

# --- GPU Lock Mechanism ---
# Simple file-based lock + In-memory check for this process
_internal_lock = threading.Lock()

def acquire_gpu_lock(owner: str, timeout: int = 10) -> bool:
    """
    Attempts to acquire the GPU lock. 
    Returns True if successful, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Check if lock file exists and is stale (older than 30s)
        if os.path.exists(GPU_LOCK_FILE):
            try:
                mtime = os.path.getmtime(GPU_LOCK_FILE)
                if time.time() - mtime > 30:
                    os.remove(GPU_LOCK_FILE) # Break stale lock
                else:
                    time.sleep(0.5)
                    continue
            except:
                time.sleep(0.5)
                continue
        
        # Try to create lock file
        try:
            with open(GPU_LOCK_FILE, "x") as f:
                f.write(owner)
            return True
        except FileExistsError:
            time.sleep(0.1)
    
    return False

def release_gpu_lock():
    try:
        if os.path.exists(GPU_LOCK_FILE):
            os.remove(GPU_LOCK_FILE)
    except:
        pass

# --- DB Setup ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, 
                  status TEXT DEFAULT 'pending', 
                  created_at TEXT, 
                  due_date TEXT,
                  priority TEXT DEFAULT 'normal')''')
    conn.commit()
    conn.close()

init_db()

# --- Models ---
class Task(BaseModel):
    content: str
    priority: str = "normal"
    due_date: Optional[str] = None

class OCRRequest(BaseModel):
    image_path: str
    prompt: Optional[str] = "Extract all text from this image."

class TTSRequest(BaseModel):
    text: str
    speaker_id: Optional[str] = "default"

# --- Endpoints ---

@app.get("/health")
def health():
    return {"status": "ok", "gpu_locked": os.path.exists(GPU_LOCK_FILE)}

# 1. Task Management (CRUD)
@app.post("/tasks/add")
def add_task(task: Task):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (content, priority, due_date, created_at) VALUES (?, ?, ?, ?)",
              (task.content, task.priority, task.due_date, datetime.now().isoformat()))
    conn.commit()
    tid = c.lastrowid
    conn.close()
    return {"status": "success", "id": tid}

@app.get("/tasks/list")
def list_tasks(status: str = "pending"):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

@app.post("/tasks/{task_id}/done")
def complete_task(task_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return {"status": "updated"}

# 2. OCR Service (Ollama / GLM-OCR)
@app.post("/services/ocr")
async def run_ocr(req: OCRRequest):
    if not os.path.exists(req.image_path):
        raise HTTPException(404, "Image file not found")
    
    # 1. Acquire Lock
    if not acquire_gpu_lock("ocr_service"):
        raise HTTPException(503, "GPU is busy. Please try again later.")
    
    try:
        # 2. Unload any heavy active models if needed (optional via API)
        # requests.post(f"{OLLAMA_URL}/api/generate", json={"model": "qwen3:8b", "keep_alive": 0})
        
        # 3. Call Ollama with Vision Support
        # Using `glm-ocr` or `llava`
        if not req.image_path: return {"error": "No path"}
        
        # Convert image to base64 if Ollama API needs it, or use `ollama run` subprocess
        # Using requests to Ollama /api/generate is cleaner but requires base64.
        # Let's use `subprocess` for `ollama run` to handles file paths easily if supported? 
        # Actually standard Ollama API requires base64.
        
        import base64
        with open(req.image_path, "rb") as img_file:
            b64_data = base64.b64encode(img_file.read()).decode('utf-8')
            
        payload = {
            "model": "glm-ocr", # User's specified model
            "prompt": req.prompt,
            "images": [b64_data],
            "stream": False
        }
        
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json().get("response", "")
        
        return {"text": result}
        
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        release_gpu_lock()

# 3. TTS Service (Proxy to Qwen-TTS Server)
@app.post("/services/tts")
async def run_tts(req: TTSRequest):
    # 1. Acquire Lock
    if not acquire_gpu_lock("tts_service"):
        raise HTTPException(503, "GPU is busy. Please try again later.")
    
    try:
        # 2. Force Unload Ollama to free VRAM for TTS
        try:
            # Setting keep_alive to 0 unloads the model immediately
            requests.post(f"{OLLAMA_URL}/api/generate", json={"model": "qwen3:8b", "keep_alive": 0}, timeout=2)
        except:
            pass # Continue even if unload fails
            
        # 3. Call TTS Server
        resp = requests.post(f"{TTS_SERVER_URL}/generate", json=req.dict(), timeout=60)
        resp.raise_for_status()
        return resp.json() # Returns path to audio file
        
    except Exception as e:
        raise HTTPException(500, str(e))
    finally:
        release_gpu_lock()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8091)
