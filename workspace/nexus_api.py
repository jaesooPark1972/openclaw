from openai import OpenAI
import lancedb
import edge_tts
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict
import subprocess
import requests
import os
import psycopg2
import time
import threading
import sys
import json
import asyncio
from collections import deque
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv(r"D:/OpenClaw/.env")

# Force UTF-8 environment
os.environ["PYTHONIOENCODING"] = "utf-8"

app = FastAPI(title="VIVACE Master API (v5.0 - Turbo Nano)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths & Config
VIVACE_ROOT = "E:/vivace_music/ace_step_1_5"
VIDEO_ROOT = "E:/vivace_video/wan2_1"
DIST_PATH = "E:/vivace_music/vivace-studio/dist"
RUST_CORE_PATH = "E:/vivace_music/vivace-core/target/release/vivace-core.exe"
MUSIC_OUTPUT_DIR = os.path.join(VIVACE_ROOT, "gradio_outputs")
VIDEO_OUTPUT_DIR = VIDEO_ROOT 
INBOUND_DIR = "C:/Users/JayPark1004/.openclaw/media/inbound"
DB_URL = os.getenv("DATABASE_URL", "postgres://postgres:2903@localhost:5432/openclaw_db")
LANCEDB_PATH = r"D:/OpenClaw/workspace/lancedb"
OPENCLAW_TOKEN = "c0b4dc439175325c5ee573f71c05e0483126adf20b67f2a8"

# State tracking
terminal_logs = deque(maxlen=200)
active_tasks = {"music": False, "video": False, "transcription": False}
start_time = time.time()

# Shared AI Clients (Nano-Mode Optimization)
def get_stt_client():
    groq_key = os.getenv("GROQ_API_KEY", "").strip(" \"'\n\t")
    if groq_key and groq_key.startswith("gsk_"):
        return OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1"), "whisper-large-v3"
    api_key = os.getenv("OPENAI_API_KEY", "").strip(" \"'\n\t")
    return OpenAI(api_key=api_key), "whisper-1"

class MusicGenRequest(BaseModel):
    prompt: str
    lyrics: Optional[str] = ""
    telegram_chat_id: Optional[str] = None

class GenRequest(BaseModel):
    prompt: str
    telegram_chat_id: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class VoiceProcessRequest(BaseModel):
    file_path: str
    telegram_chat_id: Optional[str] = None

class ConsultRequest(BaseModel):
    instruction: str
    context: Optional[Dict] = None

class PonyChatRequest(BaseModel):
    user_prompt: str
    system_prompt: Optional[str] = "You are Pony Alpha, a helpful AI assistant."
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7

# --- Helpers ---

def get_gpu_stats():
    try:
        cmd = "nvidia-smi --query-gpu=memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu --format=csv,noheader,nounits"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        vals = [v.strip() for v in output.split(',')]
        return {"total": int(vals[0]), "used": int(vals[1]), "free": int(vals[2]), "utilization": int(vals[3]), "temperature": int(vals[4]), "model": "GTX 1070"}
    except: return {"error": "Nvidia-SMI not responsive"}

def send_to_telegram(chat_id: str, text: str = None, file_path: str = None):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or not chat_id: return
    url = f"https://api.telegram.org/bot{token}/"
    try:
        if file_path:
            # .ogg (Opus) -> sendVoice (Bubble), .mp4 -> sendVideo, Others -> sendAudio/Document
            if file_path.endswith(".ogg"):
                method, file_key = "sendVoice", "voice"
            elif file_path.endswith(".mp4"):
                method, file_key = "sendVideo", "video"
            elif file_path.endswith((".mp3", ".wav", ".flac", ".m4a")):
                method, file_key = "sendAudio", "audio"
            else:
                method, file_key = "sendDocument", "document"
            
            with open(file_path, "rb") as f:
                requests.post(url + method, data={"chat_id": chat_id}, files={file_key: f})
        if text:
            requests.post(url + "sendMessage", data={"chat_id": chat_id, "text": text})
    except Exception as e:
        terminal_logs.append(f"[ERROR] Telegram Delivery Failed: {e}")

async def call_openclaw_nano(text: str):
    """
    [Nano-Mode v5] Direct Brain Bypass - Using Cerebras
    Cerebras offers truly free unlimited inference.
    """
    cerebras_key = os.getenv("CEREBRAS_API_KEY", "").strip(" \"'\n\t")
    if not cerebras_key:
        return "Error: Missing CEREBRAS_API_KEY"

    client = OpenAI(
        api_key=cerebras_key,
        base_url="https://api.cerebras.ai/v1"
    )

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b",
            messages=[
                {"role": "system", "content": "You are Nexus, the AI Brain of Antigravity system. You help the user with their requests concisely. Answer in Korean."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error talking to Cerebras: {str(e)}"

# --- API Endpoints ---

@app.on_event("startup")
async def startup_event():
    terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [SYSTEM] master control hub (Turbo Nano) initialised.")
    os.makedirs(MUSIC_OUTPUT_DIR, exist_ok=True)

@app.get("/api/status")
async def get_status():
    uptime = int(time.time() - start_time)
    gpu = get_gpu_stats()
    return {
        "status": "online",
        "version": "5.0-TurboNano",
        "uptime": uptime,
        "hardware": {"gpu": gpu},
        "modules": {
            "vivace": "busy" if active_tasks["music"] else "ready",
            "video": "busy" if active_tasks["video"] else "ready",
            "voice_turbo": "ready",
            "nano_mode": "enabled",
            "postgres": "connected"
        }
    }

@app.post("/api/voice/process")
async def process_voice(req: VoiceProcessRequest):
    """Zero-Latency Voice Pipeline: STT -> Nano Agent -> TTS -> Telegram"""
    if not os.path.exists(req.file_path): raise HTTPException(status_code=404, detail="File not found")
    
    try:
        active_tasks["transcription"] = True
        client, model = get_stt_client()
        
        # 1. STT (Whisper)
        with open(req.file_path, "rb") as f:
            text = client.audio.transcriptions.create(model=model, file=f, language="ko", response_format="text").strip()
        
        terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [VOICE] STT: {text}")
        
        # 2. Agent Reply (Nano-Path)
        reply = await call_openclaw_nano(text)
        terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [VOICE] Reply: {reply[:50]}...")
        
        # 3. TTS (Inline Edge-TTS -> FFmpeg OGG OPUS 변환)
        mp3_temp = r"D:\OpenClaw\workspace\reply_voice_temp.mp3"
        audio_reply_path = r"D:\OpenClaw\workspace\reply_voice.ogg"
        try:
            # Step 3-1: Edge-TTS -> MP3
            communicate = edge_tts.Communicate(reply, "ko-KR-SunHiNeural")
            await communicate.save(mp3_temp)
            
            # Step 3-2: FFmpeg MP3 -> OGG OPUS (Telegram Voice Bubble 규격)
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-i", mp3_temp,
                "-c:a", "libopus",
                "-b:a", "48k",
                "-ar", "24000",
                "-ac", "1",
                "-application", "voip",
                audio_reply_path
            ]
            subprocess.run(ffmpeg_cmd, capture_output=True, check=True)
            terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [VOICE] TTS+OPUS: {audio_reply_path}")
            
            # 임시 파일 정리
            if os.path.exists(mp3_temp): os.remove(mp3_temp)
        except Exception as tts_err:
            terminal_logs.append(f"[ERROR] TTS: {str(tts_err)}")
            audio_reply_path = ""
        
        # 4. Telegram Send
        if req.telegram_chat_id:
            send_to_telegram(req.telegram_chat_id, text=f"💬 {text}\n\n🤖 {reply}", file_path=audio_reply_path if audio_reply_path else None)
            
        return {"input": text, "reply": reply, "audio": audio_reply_path}
        
    except Exception as e:
        terminal_logs.append(f"[ERROR] Voice Pipeline: {str(e)}")
        return {"error": str(e)}
    finally:
        active_tasks["transcription"] = False

@app.get("/api/logs")
async def get_logs(): return list(terminal_logs)

@app.post("/api/antigravity/consult")
async def consult_antigravity(req: ConsultRequest):
    """
    [Antigravity Bridge] Direct consultation endpoint for complex architectural/creative tasks.
    Delegates the instruction to the OpenClaw agent and returns the response.
    """
    terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [CONSULT] Request: {req.instruction[:50]}...")
    
    # Execute via the nano-mode agent bridge
    reply = await call_openclaw_nano(req.instruction)
    
    if not reply or "Error:" in reply:
        terminal_logs.append(f"[ERROR] Consult Failed: {reply}")
    else:
        terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [CONSULT] Reply received.")
        
    return {
        "instruction": req.instruction,
        "reply": reply,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/chat/pony")
async def chat_pony(req: PonyChatRequest):
    """
    [Pony Alpha API] Direct Interface with Reasoning Capabilities.
    Uses 'requests' to handle custom 'reasoning_details' parameters.
    """
    or_key = os.getenv("OPENROUTER_API_KEY")
    # Fallback to OpenAI key if specific OpenRouter key not found (though OpenRouter key is preferred)
    if not or_key: or_key = os.getenv("OPENAI_API_KEY")
    
    if not or_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not found in environment")
        
    try:
        start_t = time.time()
        
        headers = {
            "Authorization": f"Bearer {or_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/OpenClaw/OpenClaw",
            "X-Title": "OpenClaw Antigravity"
        }
        
        # 1. First Call (Reasoning Enabled)
        payload = {
            "model": "openrouter/pony-alpha",
            "messages": [
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.user_prompt}
            ],
            "reasoning": {"enabled": True}
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=120
        )
        
        if response.status_code != 200:
            return {"error": f"OpenRouter API Error: {response.text}"}
            
        resp_json = response.json()
        message = resp_json['choices'][0]['message']
        content = message.get('content', '')
        reasoning_details = message.get('reasoning_details')
        
        # Log reasoning stats
        tokens_reasoning = resp_json.get('usage', {}).get('completion_tokens_reasoning', 0)
        terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [PONY] Reasoning extracted (Tokens: {tokens_reasoning})")
        
        # 2. (Optional) Self-Correction Loop / Verification
        # If specific flag or high temperature is set, we could trigger the 2nd loop. 
        # For now, we return the reasoning so the Agent can decide.
        # But if the user specifically requested the "Are you sure?" loop application:
        
        # Let's perform the 2nd loop automatically for maximum reliability ("Antigravity Mode")
        # to ensure the answer is double-checked.
        
        msgs_v2 = [
            {"role": "user", "content": req.user_prompt},
            {
                "role": "assistant", 
                "content": content,
                "reasoning_details": reasoning_details # KEY: Passing back reasoning
            },
            {"role": "user", "content": "Review your reasoning and answer. Are you sure? Think carefully."}
        ]
        
        payload_v2 = {
            "model": "openrouter/pony-alpha",
            "messages": msgs_v2,
            "reasoning": {"enabled": True}
        }
        
        response_v2 = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, 
            data=json.dumps(payload_v2),
            timeout=120
        )
        
        final_content = content
        final_reasoning = reasoning_details
        
        if response_v2.status_code == 200:
            resp_v2_json = response_v2.json()
            msg_v2 = resp_v2_json['choices'][0]['message']
            final_content = msg_v2.get('content')
            final_reasoning = msg_v2.get('reasoning_details', reasoning_details)
            terminal_logs.append(f"{time.strftime('[%H:%M:%S]')} [PONY] Self-Correction loop complete.")
            
        duration = time.time() - start_t
        
        return {
            "model": "openrouter/pony-alpha",
            "content": final_content,
            "reasoning_details": final_reasoning, # Return this to the agent
            "latency": duration
        }
            
    except Exception as e:
        curr_err = str(e)
        terminal_logs.append(f"[ERROR] Pony Alpha: {curr_err}")
        return {"error": curr_err}

@app.post("/api/vivace/generate")
async def generate_music(req: MusicGenRequest):
    try:
        active_tasks["music"] = True
        args = [os.path.join(VIVACE_ROOT, ".venv/Scripts/python.exe"), "-u", "generate_one_cli.py", "--prompt", req.prompt, "--steps", "15", "--offload", "True"]
        if req.lyrics: args.extend(["--lyrics", req.lyrics])
        proc = subprocess.Popen(args, cwd=VIVACE_ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=0)
        threading.Thread(target=log_reader, args=(proc.stdout, "[MUSIC]", "music", req.telegram_chat_id), daemon=True).start()
        return {"status": "started"}
    except Exception as e: return {"error": str(e)}

@app.get("/api/db/vector/stats")
async def get_vector_stats():
    try:
        db = lancedb.connect(LANCEDB_PATH)
        return {"tables": db.table_names(), "path": LANCEDB_PATH}
    except Exception as e: return {"error": str(e)}

def log_reader(pipe, prefix="", engine_key=None, telegram_chat_id=None, save_path=None):
    captured_file = save_path
    try:
        with pipe:
            for line in iter(pipe.readline, ''):
                timestamp = time.strftime("[%H:%M:%S]")
                terminal_logs.append(f"{timestamp} {prefix} {line.strip()}")
                if "FULL_PATH:" in line: captured_file = line.split("FULL_PATH:")[1].strip()
                if engine_key and ("SUCCESS" in line or "DONE" in line):
                    active_tasks[engine_key] = False
                    if telegram_chat_id and captured_file and os.path.exists(captured_file):
                        send_to_telegram(telegram_chat_id, text=f"✅ {engine_key.upper()} Complete!", file_path=captured_file)
    finally:
        if engine_key: active_tasks[engine_key] = False

# Static & Mounting
if os.path.exists(MUSIC_OUTPUT_DIR): app.mount("/media/music", StaticFiles(directory=MUSIC_OUTPUT_DIR), name="music")
if os.path.exists(DIST_PATH): app.mount("/", StaticFiles(directory=DIST_PATH, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8080)
    args, _ = parser.parse_known_args()
    
    uvicorn.run(app, host="0.0.0.0", port=args.port)
