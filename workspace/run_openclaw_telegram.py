# ============================================================================
# OpenClaw + Ollama + Telegram Launcher
# ============================================================================
# Ollama (LLM) + OpenClaw Gateway + Telegram Integration
#
# .env auto-load from:
# - F:/AGen/.env (AGen environment)
# - ./openclaw.env (OpenClaw specific)
#
# Version: 1.0.2 (Fixed)
# ============================================================================

import asyncio
import subprocess
import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict

# ============================================================================
# LOAD ENV FROM AGEN
# ============================================================================

AGEN_ENV_PATH = Path("F:/AGen/.env")
OPENCLAW_ENV_PATH = Path("./openclaw.env")

def load_env():
    """Load environment variables"""
    env_paths = []
    
    if AGEN_ENV_PATH.exists():
        env_paths.append(AGEN_ENV_PATH)
        print(f"[Env] Found: {AGEN_ENV_PATH}")
    
    if OPENCLAW_ENV_PATH.exists():
        env_paths.append(OPENCLAW_ENV_PATH)
        print(f"[Env] Found: {OPENCLAW_ENV_PATH}")
    
    for env_path in env_paths:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
    
    if os.environ.get("TELEGRAM_TOKEN"):
        print("[Env] TELEGRAM_TOKEN: Loaded")
    else:
        print("[Env] TELEGRAM_TOKEN: Not set")

load_env()

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "ollama_host": os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
    "ollama_model": os.environ.get("OLLAMA_MODEL", "llama3.2:latest"),
    "telegram_token": os.environ.get("TELEGRAM_TOKEN", ""),
    "telegram_enabled": bool(os.environ.get("TELEGRAM_TOKEN")),
    "gateway_port": int(os.environ.get("OPENCLAW_GATEWAY_PORT", 8095)),
}

print(f"""
========================================
OpenClaw Launcher v1.0.2
========================================
Env from: {AGEN_ENV_PATH}
Telegram: {'Enabled' if CONFIG['telegram_enabled'] else 'Disabled'}
Ollama: {CONFIG['ollama_host']}
""")

# ============================================================================
# SERVICES
# ============================================================================

class ServiceManager:
    def __init__(self):
        self.services: Dict[str, dict] = {}
    
    def add_service(self, name: str, command: list, check_url: str = None):
        self.services[name] = {
            "command": command,
            "check_url": check_url,
            "status": "stopped",
            "process": None
        }
    
    async def start(self, name: str) -> bool:
        if name not in self.services:
            print(f"[{name}] Service not found")
            return False
        
        service = self.services[name]
        
        try:
            process = subprocess.Popen(
                service["command"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=os.getcwd()
            )
            
            service["process"] = process
            service["status"] = "running"
            print(f"[{name}] Started (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"[{name}] Failed: {e}")
            return False
    
    def get_status(self) -> Dict:
        return {
            name: {"status": s["status"]}
            for name, s in self.services.items()
        }


# ============================================================================
# OLLAMA CLIENT
# ============================================================================

class OllamaClient:
    def __init__(self):
        self.host = CONFIG["ollama_host"]
        self.model = CONFIG["ollama_model"]
    
    async def check_connection(self) -> bool:
        import httpx
        try:
            resp = httpx.get(f"{self.host}/api/tags", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                print(f"[Ollama] Connected: {len(data.get('models', []))} models")
                return True
        except Exception as e:
            print(f"[Ollama] Connection failed: {e}")
        return False
    
    async def generate(self, prompt: str) -> str:
        import httpx
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 2048}
        }
        try:
            resp = httpx.post(f"{self.host}/api/generate", json=payload, timeout=120)
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except Exception as e:
            print(f"[Ollama] Generation failed: {e}")
        return ""


# ============================================================================
# TELEGRAM BOT
# ============================================================================

# ============================================================================
# TELEGRAM BOT
# ============================================================================

class TelegramBot:
    def __init__(self):
        self.token = CONFIG["telegram_token"]
        self.offset = 0
        self.running = False
        self.db_conn = None
        self._init_db()

    def _init_db(self):
        """Initialize PostgreSQL connection and schema"""
        try:
            import psycopg2
            self.db_conn = psycopg2.connect(
                host="localhost",
                database="antigravity_db",
                user="user",
                password="password"
            )
            self.db_conn.autocommit = True
            with self.db_conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS telegram_history (
                        id SERIAL PRIMARY KEY,
                        chat_id BIGINT,
                        username TEXT,
                        role TEXT,
                        message TEXT,
                        context JSONB,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            print("[Telegram] DB Connected & Table Verified")
        except Exception as e:
            # Handle potential encoding errors during error printing (Korean Windows CP949 vs UTF-8)
            err_msg = str(e)
            try:
                print(f"[Telegram] DB Init Failed: {err_msg}")
            except UnicodeEncodeError:
                print(f"[Telegram] DB Init Failed: {err_msg.encode('utf-8', 'ignore').decode('utf-8')}")

    async def start(self):
        if not self.token:
            print("[Telegram] Token not configured")
            return
        
        self.running = True
        print(f"[Telegram] Bot started")
        await self._polling()
    
    async def _polling(self):
        import httpx
        while self.running:
            try:
                async with httpx.AsyncClient(timeout=35.0) as client:
                    resp = await client.get(
                        f"https://api.telegram.org/bot{self.token}/getUpdates",
                        params={"offset": self.offset, "timeout": 30}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        if data.get("ok"):
                            for update in data.get("result", []):
                                await self._handle_update(update)
                                self.offset = update["update_id"] + 1
            except Exception as e:
                # Safe error printing
                try:
                    print(f"[Telegram] Polling Error: {e}")
                except:
                    pass
                await asyncio.sleep(5)
    
    async def _handle_update(self, update: dict):
        message = update.get("message", {})
        text = message.get("text", "")
        chat_id = message.get("chat", {}).get("id")
        username = message.get("chat", {}).get("username", "unknown")
        
        if text and chat_id:
            try:
                print(f"[Telegram] Received from {username}: {text}")
            except:
                print(f"[Telegram] Received from {username}: (Text encoding error)")
            
            # 1. Log User Message
            await self._log_to_db(chat_id, username, "user", text)

            # 2. Check Commands
            if text.startswith("/archive"):
                await self._archive_history(chat_id)
                return

            try:
                # 3. Process with Memory & LLM
                response = await self._process_with_ollama(text)
                
                # 4. Send & Log Response
                await self._send_response(chat_id, response)
                await self._log_to_db(chat_id, "OpenClaw", "assistant", response)
            except Exception as e:
                print(f"[Telegram] Processing failed: {e}")
                await self._send_response(chat_id, "⚠️ I'm analyzing the void... (Error processing message)")

    async def _process_with_ollama(self, text: str) -> str:
        import httpx
        ollama = OllamaClient()
        
        # 1. Retrieve Memory (RAG)
        context_str = ""
        try:
            # Query God Gateway Nexus (Port 8095 for v5)
            async with httpx.AsyncClient() as client:
                mem_resp = await client.get(
                    "http://localhost:8095/api/memory/search",
                    params={"query": text},
                    timeout=5.0
                )
                if mem_resp.status_code == 200:
                    results = mem_resp.json().get("results", [])
                    if results:
                        context_str = "\n".join([f"- {r}" for r in results[:3]])
                        print(f"[Memory] Found {len(results)} relevant memories")
        except Exception as e:
            print(f"[Memory] Retrieval failed: {e}")

        # 2. Construct Prompt
        prompt = f"""You are OpenClaw (Antigravity), a highly advanced AI system.
        
[MEMORY CONTEXT]
{context_str}

[USER REQUEST]
{text}

[INSTRUCTION]
Respond to the user naturally. Use the memory context if relevant.
"""
        return await ollama.generate(prompt)
    
    async def _send_response(self, chat_id: str, text: str):
        import httpx
        payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"https://api.telegram.org/bot{self.token}/sendMessage", json=payload, timeout=10)
        except Exception as e:
            print(f"[Telegram] Send failed: {e}")

    async def _log_to_db(self, chat_id, username, role, message, context=None):
        """Log message to PostgreSQL and Vector Memory (God Gateway)"""
        # PostgreSQL Log
        if self.db_conn:
            try:
                with self.db_conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO telegram_history (chat_id, username, role, message, context) VALUES (%s, %s, %s, %s, %s)",
                        (chat_id, username, role, message, json.dumps(context) if context else None)
                    )
            except Exception as e:
                print(f"[DB Log Error] {e}")

        # God Gateway Memory Sync (Vector DB)
        try:
            import httpx
            memory_content = f"{username} ({role}): {message}"
            async with httpx.AsyncClient() as client:
                await client.post(
                    "http://localhost:8095/memory/add",
                    json={"content": memory_content, "metadata": {"chat_id": chat_id, "role": role, "timestamp": str(datetime.now())}},
                    timeout=2.0
                )
        except Exception as e:
            pass # Non-blocking

    async def _archive_history(self, chat_id: int):
        """Dump chat history and Upload to Google Drive"""
        if not self.db_conn:
            await self._send_response(chat_id, "❌ Database not connected.")
            return

        filename = f"telegram_archive_{chat_id}_{int(datetime.now().timestamp())}.json"
        
        # Ensure data directory exists
        data_dir = Path("D:/OpenClaw/workspace/data")
        data_dir.mkdir(parents=True, exist_ok=True)
        filepath = data_dir / filename

        try:
            # 1. Export from DB
            with self.db_conn.cursor() as cur:
                cur.execute("SELECT role, username, message, timestamp FROM telegram_history WHERE chat_id = %s ORDER BY timestamp", (chat_id,))
                rows = cur.fetchall()
            
            data = [{"role": r[0], "user": r[1], "msg": r[2], "time": str(r[3])} for r in rows]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            await self._send_response(chat_id, f"💾 Archive saved locally: `{filename}`")
            
            # 2. Upload to Google Drive
            await self._send_response(chat_id, "☁️ Uploading to Google Drive...")
            
            # Dynamic import to avoid path issues if file missing
            sys.path.append(str(Path.cwd() / "workspace"))
            try:
                import google_drive_uploader
                webview_link = google_drive_uploader.upload_to_drive(str(filepath))
                
                if webview_link:
                    await self._send_response(chat_id, f"✅ **Backup Complete!**\n[View on Google Drive]({webview_link})")
                else:
                    await self._send_response(chat_id, "⚠️ Upload failed (check console/logs).")
            except ImportError as e:
                 await self._send_response(chat_id, f"⚠️ Google Drive Module Error: {e}")

        except Exception as e:
            await self._send_response(chat_id, f"❌ Archive failed: {e}")


# ============================================================================
# MAIN
# ============================================================================

async def main():
    print("""
    ========================================
    OpenClaw + Ollama + Telegram Launcher
    ========================================
    """)
    
    manager = ServiceManager()
    
    # 1. Check Ollama
    print("\n[1/4] Checking Ollama...")
    ollama = OllamaClient()
    ollama_ready = await ollama.check_connection()
    
    if not ollama_ready:
        print("\n[Warning] Ollama not running. Attempting to start...")
        try:
            subprocess.Popen("start ollama serve", shell=True)
            print("[Ollama] Launch command sent... Waiting 10s...")
            await asyncio.sleep(10)
            if await ollama.check_connection():
                print("[Ollama] Successfully started!")
                ollama_ready = True
            else:
                print("[Error] Failed to auto-start Ollama. Please run 'ollama serve' manually.")
        except Exception as e:
             print(f"[Error] Auto-start failed: {e}")
    
    # 2. Start Gateway
    print("\n[2/4] Starting OpenClaw Gateway...")
    manager.add_service("gateway", [sys.executable, "mcp_servers/god_gateway_nexus_v5.py"])
    await manager.start("gateway")
    
    # 3. Start Creative Engine
    print("\n[3/4] Starting Creative Engine...")
    manager.add_service("creative", [sys.executable, "mcp_servers/openclaw_creative_unified.py"])
    await manager.start("creative")
    
    # 4. Start Telegram
    print("\n[4/4] Starting Telegram Bot...")
    bot = TelegramBot()
    
    if CONFIG["telegram_enabled"]:
        await bot.start()
    else:
        print("\n[Warning] Telegram token not set in F:/AGen/.env")
    
    # Status loop
    print("\n========================================\nSystem Started\n========================================\n")
    
    while True:
        status = manager.get_status()
        print("--- Status ---")
        for name, info in status.items():
            icon = "OK" if info["status"] == "running" else "XX"
            print(f"  [{icon}] {name}")
        if ollama_ready:
            print("  [OK] ollama")
        else:
            print("  [XX] ollama (not connected)")
        print()
        await asyncio.sleep(10)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\nError: {e}")
