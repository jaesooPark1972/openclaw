"""
🦞 OpenClaw God Gateway Nexus v4.0 - Unified Commander
========================================================
Integrates: PostgreSQL, LanceDB (Vector), Everything Search, 
            AGen, Engram, Antigravity Nexus, Secretary, Skills, Workflows

Ports:
- API: 8085
- Vector DB: LanceDB (embedded)
- PostgreSQL: via MCP/postgres server

Author: OpenClaw Architecture Team
"""

import os
import sys
import json
import subprocess
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

# FastAPI Setup
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Database & Vector Search
import lancedb
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor

# MCP Tools (for integration with existing MCP servers)
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("God-Gateway-Nexus")
except ImportError:
    mcp = None
    print("⚠️ MCP not installed. Running in API-only mode.")

# ============================================================
# CONFIGURATION
# ============================================================
CONFIG = {
    "api_port": 8085,
    "lancedb_path": r"D:\OpenClaw\workspace\vector_db",
    "postgres_url": "postgresql://user:password@localhost:5432/antigravity_db",
    "everything_exe": r"C:\Program Files\Everything\Everything.exe",
    "domains": {
        "openclaw": r"D:\OpenClaw",
        "vivace": r"F:\Vivace",
        "comfyui": r"F:\ComfyUI-Easy-Install",
        "agen": r"F:\AGen",
        "rust": r"D:\Rust",
        "vscode": r"C:\Users\JayPark1004\.vscode",
    }
}

app = FastAPI(
    title="🦞 OpenClaw God Gateway Nexus",
    description="Unified Commander for all AI Systems",
    version="4.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
db = None
embedding_model = None

# ============================================================
# DATABASE SETUP
# ============================================================

def init_lancedb():
    """Initialize LanceDB for vector search"""
    global db, embedding_model
    try:
        os.makedirs(CONFIG["lancedb_path"], exist_ok=True)
        db = lancedb.connect(CONFIG["lancedb_path"])
        
        # Create tables if not exist
        if "memories" not in db.table_names():
            db.create_table("memories", schema=[
                ("id", "int64"),
                ("content", "text"),
                ("embedding", "vector(384)"),  # Default embedding size
                ("metadata", "binary"),
                ("created_at", "timestamp"),
            ])
        
        if "file_index" not in db.table_names():
            db.create_table("file_index", schema=[
                ("file_path", "text"),
                ("content", "text"),
                ("embedding", "vector(384)"),
                ("file_type", "text"),
                ("modified", "timestamp"),
            ])
        
        # Load embedding model
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ LanceDB initialized")
        return True
    except Exception as e:
        print(f"❌ LanceDB init failed: {e}")
        return False

def init_postgres():
    """Initialize PostgreSQL connection"""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="antigravity_db",
            user="user",
            password="password"
        )
        conn.autocommit = True
        print("✅ PostgreSQL connected")
        return conn
    except Exception as e:
        print(f"⚠️ PostgreSQL not available: {e}")
        return None

pg_conn = init_postgres()

# ============================================================
# MODELS
# ============================================================

class MemoryAddRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = []

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    mode: str = "hybrid"  # vector, keyword, hybrid

class CommandRequest(BaseModel):
    command: str
    domain: str = "openclaw"
    approved: bool = True

class WorkflowRequest(BaseModel):
    name: str
    steps: List[Dict[str, Any]]

# ============================================================
# VECTOR SEARCH ENDPOINTS
# ============================================================

@app.post("/memory/add")
async def add_memory(req: MemoryAddRequest):
    """Add a memory to vector DB"""
    if not db or not embedding_model:
        raise HTTPException(503, "Vector DB not initialized")
    
    try:
        embedding = embedding_model.encode(req.content).tolist()
        
        table = db.open_table("memories")
        table.add([
            {
                "content": req.content,
                "embedding": embedding,
                "metadata": json.dumps(req.metadata or {}),
                "created_at": datetime.now(),
            }
        ])
        
        return {"status": "added", "content_preview": req.content[:100]}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/memory/search")
async def search_memory(req: SearchRequest):
    """Search memories using vector similarity"""
    if not db or not embedding_model:
        raise HTTPException(503, "Vector DB not initialized")
    
    try:
        query_embedding = embedding_model.encode(req.query).tolist()
        table = db.open_table("memories")
        
        results = table.search(query_embedding).limit(req.top_k).to_list()
        
        return {
            "query": req.query,
            "results": results,
            "mode": req.mode
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/memory/index-domain")
async def index_domain(domain: str):
    """Index all files in a domain for semantic search"""
    if not db or not embedding_model:
        raise HTTPException(503, "Vector DB not initialized")
    
    domain_path = CONFIG["domains"].get(domain)
    if not domain_path or not Path(domain_path).exists():
        raise HTTPException(404, f"Domain {domain} not found")
    
    # Simple file content indexing (text files only)
    indexed = []
    for ext in [".py", ".md", ".txt", ".json", ".ts", ".js"]:
        for f in Path(domain_path).rglob(f"*{ext}"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")[:10000]
                if len(content) > 50:
                    embedding = embedding_model.encode(content[:500]).tolist()
                    
                    table = db.open_table("file_index")
                    table.add([{
                        "file_path": str(f),
                        "content": content[:500],
                        "embedding": embedding,
                        "file_type": ext,
                        "modified": datetime.fromtimestamp(f.stat().st_mtime),
                    }])
                    indexed.append(str(f))
            except Exception:
                continue
    
    return {"status": "indexed", "count": len(indexed), "domain": domain}

# ============================================================
# EVERYTHING SEARCH INTEGRATION
# ============================================================

@app.get("/search/everything")
async def everything_search(q: str, limit: int = 50):
    """Search files using Everything (Windows desktop search)"""
    try:
        # Use es.exe CLI if available
        es_path = r"C:\Program Files\Everything\es.exe"
        if not Path(es_path).exists():
            # Fallback to MCP Everything server
            return {"status": "fallback", "query": q, "message": "Use MCP Everything server"}
        
        result = subprocess.run(
            [es_path, "-n", str(limit), q],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        return {"query": q, "results": files[:limit], "count": len(files)}
    except Exception as e:
        raise HTTPException(500, str(e))

# ============================================================
# WORKFLOW EXECUTION
# ============================================================

@app.post("/workflow/run")
async def run_workflow(req: WorkflowRequest):
    """Execute a multi-step workflow"""
    results = []
    
    for i, step in enumerate(req.steps):
        step_name = step.get("name", f"step_{i}")
        action = step.get("action")
        params = step.get("params", {})
        
        try:
            if action == "command":
                result = await execute_command(params.get("cmd"), params.get("cwd", "D:/OpenClaw"))
            elif action == "mcp_call":
                result = await call_mcp_tool(params.get("tool"), params.get("args", {}))
            elif action == "http_request":
                result = await http_request(params.get("method"), params.get("url"), params.get("json"))
            else:
                result = {"status": "unknown_action", "action": action}
            
            results.append({"step": i, "name": step_name, "result": result})
        except Exception as e:
            results.append({"step": i, "name": step_name, "error": str(e)})
            break
    
    return {"workflow": req.name, "results": results}

# ============================================================
# DOMAIN CONTROL
# ============================================================

@app.get("/domain/{domain}/status")
async def domain_status(domain: str):
    """Get status of a domain service"""
    domains = {
        "openclaw": {"port": 18789, "status": "check_ws"},
        "vivace": {"port": 8080, "status": "check_http"},
        "secretary": {"port": 8091, "status": "check_http"},
        "comfyui": {"port": 8188, "status": "check_http"},
    }
    
    if domain not in domains:
        raise HTTPException(404, f"Unknown domain: {domain}")
    
    import requests
    info = domains[domain]
    
    try:
        if info["status"] == "check_http":
            resp = requests.get(f"http://localhost:{info['port']}/health", timeout=2)
            return {"domain": domain, "status": "running", "details": resp.json()}
        else:
            return {"domain": domain, "status": "unknown", "info": info}
    except:
        return {"domain": domain, "status": "stopped"}

@app.post("/domain/{domain}/execute")
async def domain_execute(domain: str, req: CommandRequest):
    """Execute command in a specific domain"""
    domain_path = CONFIG["domains"].get(domain)
    if not domain_path:
        raise HTTPException(404, f"Domain {domain} not configured")
    
    return await execute_command(req.command, domain_path)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

async def execute_command(cmd: str, cwd: str):
    """Execute shell command"""
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd
    )
    stdout, stderr = await proc.communicate()
    return {
        "command": cmd,
        "stdout": stdout.decode("utf-8", errors="replace"),
        "stderr": stderr.decode("utf-8", errors="replace"),
        "returncode": proc.returncode
    }

async def call_mcp_tool(tool_name: str, args: Dict[str, Any]):
    """Call an MCP tool (placeholder - requires actual MCP connection)"""
    return {"status": "mcp_call_pending", "tool": tool_name, "args": args}

async def http_request(method: str, url: str, json_data: Dict = None):
    """Make HTTP request"""
    import httpx
    client = httpx.AsyncClient()
    try:
        if method == "GET":
            resp = await client.get(url)
        else:
            resp = await client.post(url, json=json_data)
        return {"status": resp.status_code, "content": resp.text[:1000]}
    finally:
        await client.aclose()

# ============================================================
# GOD MODE ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "🦞 OpenClaw God Gateway Nexus v4.0",
        "status": "online",
        "endpoints": {
            "memory": "/memory/add, /memory/search, /memory/index-domain",
            "search": "/search/everything",
            "workflow": "/workflow/run",
            "domain": "/domain/{domain}/status, /domain/{domain}/execute",
        },
        "domains": list(CONFIG["domains"].keys()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "vector_db": db is not None,
        "postgres": pg_conn is not None,
        "timestamp": datetime.now().isoformat()
    }

# ============================================================
# MAIN
# ============================================================

# ============================================================
# SYSTEM SOVEREIGN (GOD MODE)
# ============================================================

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil not installed. God Mode stats will be limited.")

import shutil
import platform

class SystemSovereign:
    """
    The Omnipotent System Controller.
    Granted full permission by USER to manage, execute, and control the OS.
    """
    def __init__(self):
        self.os_type = platform.system()
        self.start_time = datetime.now()
        print("⚠️ SYSTEM SOVEREIGN MODULE LOADED: FULL CONTROL CAPABILITY")

    async def execute_shell(self, command: str, background: bool = False) -> Dict:
        """Execute any shell command with Sovereign authority"""
        try:
            if background:
                subprocess.Popen(command, shell=True)
                return {"status": "started", "mode": "background", "command": command}
            
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def kill_process(self, identifier: str) -> Dict:
        """Terminate process by PID or Name"""
        if not PSUTIL_AVAILABLE:
            return {"error": "psutil not available"}
            
        target_pid = None
        target_name = None

        try:
            if identifier.isdigit():
                target_pid = int(identifier)
                proc = psutil.Process(target_pid)
                proc.terminate()
                return {"status": "terminated", "pid": target_pid, "name": proc.name()}
            else:
                target_name = str(identifier)
                killed_count = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    if target_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        killed_count += 1
                return {"status": "terminated", "count": killed_count, "target": target_name}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def filesystem_action(self, action: str, path: str, content: str = None) -> Dict:
        """Direct Filesystem Control (Read/Write/Delete/Move)"""
        try:
            if action == "read":
                if not os.path.exists(path):
                    return {"error": "File not found"}
                with open(path, "r", encoding="utf-8") as f:
                    return {"content": f.read()}
            elif action == "write":
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content or "")
                return {"status": "written", "path": path}
            elif action == "delete":
                if not os.path.exists(path):
                    return {"error": "Path not found"}
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                return {"status": "deleted", "path": path}
            elif action == "list":
                if not os.path.exists(path):
                     return {"error": "Path not found"}
                return {"files": os.listdir(path)}
            return {"error": "Invalid action"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_full_system_status(self) -> Dict:
        """Get deeply detailed system metrics"""
        status = {
            "uptime": str(datetime.now() - self.start_time),
            "os": self.os_type,
            "timestamp": datetime.now().isoformat()
        }
        
        if PSUTIL_AVAILABLE:
            status.update({
                "cpu": {
                    "percent": psutil.cpu_percent(interval=None),
                    "cores": psutil.cpu_count()
                },
                "memory": psutil.virtual_memory()._asdict(),
                "disk": psutil.disk_usage('/')._asdict(),
            })
        return status

sovereign = SystemSovereign()

# God Mode Routes
from fastapi import APIRouter
god_router = APIRouter(prefix="/api/god", tags=["God Mode"])

class ShellCommand(BaseModel):
    command: str
    background: bool = False

class FileRequest(BaseModel):
    action: str
    path: str
    content: Optional[str] = None

@god_router.post("/shell")
async def god_shell(request: ShellCommand):
    return await sovereign.execute_shell(request.command, request.background)

@god_router.post("/process/kill")
async def god_kill_process(identifier: str):
    return await sovereign.kill_process(identifier)

@god_router.post("/fs")
async def god_filesystem(request: FileRequest):
    return await sovereign.filesystem_action(request.action, request.path, request.content)

@god_router.get("/status")
async def god_status():
    return await sovereign.get_full_system_status()

# Include the router
app.include_router(god_router)


if __name__ == "__main__":
    print("🚀 Starting God Gateway Nexus v4.0...")
    print(f"📡 API Server: http://localhost:{CONFIG['api_port']}")
    print(f"📦 Vector DB: {CONFIG['lancedb_path']}")
    
    # Initialize
    init_lancedb()
    
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=CONFIG["api_port"])
