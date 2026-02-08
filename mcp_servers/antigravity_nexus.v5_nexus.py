
import sys
import os
import subprocess
import json
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Union

# -------------------------------------------------------------------------
# 🦞 ANTIGRAVITY NEXUS: STRATEGIC GOD MODE (v3.2 - OpenCode & VSCode)
# -------------------------------------------------------------------------
# Integrates: AGen, Vivace, ComfyUI, Rust, ToonMaker, Ollama, OpenCode, VSCode
# Validated by: Antigravity Chief Architect
# -------------------------------------------------------------------------

import requests

# 1. SMART DISCOVERY SYSTEM
DRIVES = ["F:", "E:", "D:", "C:"]

def find_domain_path(candidates: List[str]) -> Path:
    for drive in DRIVES:
        root = Path(drive) / "/"
        if not root.exists(): continue
        for folder in candidates:
            if ":" in folder: 
                p = Path(folder)
                if p.exists(): return p
                continue
            p = root / folder
            if p.exists(): return p
    return Path(candidates[0])

# 2. DOMAIN CONFIGURATION
DOMAINS = {
    "agen": find_domain_path(["AGen", "AgEn"]),
    "vivace": find_domain_path(["Vivace", "AGen/Vivace"]),
    "comfyui": find_domain_path(["ComfyUI-Easy-Install", "ComfyUI"]),
    "rust": find_domain_path(["Rust", "RustProjects"]),
    "ollama": find_domain_path(["Ollama", "AppData/Local/Ollama"]), 
    "openclaw": find_domain_path(["D:/OpenClaw", "OpenClaw"]),
    "toonmaker": find_domain_path(["D:/ToonMaker", "ToonMaker"]),
    "opencode": find_domain_path(["oh-my-opencode-3.0.0-beta.13", "OpenCode", "oh-my-opencode"]),
    "vscode": find_domain_path([str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Microsoft VS Code/Code.exe")]),
}

# 3. SETUP FASTMCP
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("Antigravity-God-Nexus")
except ImportError:
    raise ImportError("FastMCP required. Install 'mcp'.")

# -------------------------------------------------------------------------
# 🧠 CORE POWERS EXPANSION
# -------------------------------------------------------------------------

@mcp.tool()
async def delegate_to_antigravity(instruction: str, context_files: Optional[List[str]] = None) -> str:
    """
    [Strategic] Delegates a high-level architectural or creative task to Antigravity via the Master API.
    Use this when you need: System Design, Complex Reasoning, Story Creation, or Master Planning.
    """
    url = "http://localhost:8080/api/antigravity/consult"
    try:
        payload = {
            "instruction": instruction,
            "context": {"files": context_files} if context_files else None
        }
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            return f"🏹 [Antigravity Core Response]\n\n{result.get('reply', 'No reply received.')}"
        else:
            return f"❌ Antigravity API Error: {resp.text}"
    except Exception as e:
        # Fallback logic if API is down
        return f"⚠️ API Connection Failed. Ensure Master API (port 8080) is running.\nError: {str(e)}"

@mcp.tool()
async def system_cmd(command: str, cwd: str = "D:/OpenClaw") -> str:
    """
    [CMD/Shell] Executes a raw command line instruction.
    WARNING: Use with caution.
    """
    try:
        process = subprocess.Popen(
            command, shell=True, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', errors='replace'
        )
        stdout, stderr = process.communicate()
        return f"🖥️ CMD Result:\n{stdout}\n{stderr}"
    except Exception as e:
        return f"❌ CMD Error: {str(e)}"

@mcp.tool()
async def system_vscode(action: str = "open", target_path: str = ".") -> str:
    """
    [VSCode] Controls Visual Studio Code.
    Args:
        action: 'open', 'new_window'
        target_path: File or folder path to open
    """
    cmd = ["code", target_path]
    if action == "new_window":
        cmd.insert(1, "-n")
        
    try:
        subprocess.Popen(cmd, shell=True)
        return f"📝 VSCode Opened: {target_path}"
    except Exception as e:
        return f"❌ VSCode Launch Error: {str(e)}"

@mcp.tool()
async def antigravity_opencode(project_path: str, mode: str = "open") -> str:
    """
    [OpenCode] Activates the specialized 'Oh My OpenCode' environment for Professional Coding.
    """
    opencode_root = DOMAINS["opencode"]
    if not opencode_root.exists():
        return f"❌ OpenCode not found at expected locations. (Checked: {opencode_root})"
    
    # Try to find an executable or launch script
    launcher = None
    if (opencode_root / "OpenCode.exe").exists():
        launcher = opencode_root / "OpenCode.exe"
    elif (opencode_root / "code.bat").exists():
        launcher = opencode_root / "code.bat"
    
    if launcher:
        cmd = [str(launcher), project_path]
        subprocess.Popen(cmd, shell=True)
        return f"💎 OpenCode Studio Launched for: {project_path}"
    else:
        # Fallback to standard VSCode with OpenCode Profile context if specific exe not found
        return await system_vscode(action="open", target_path=project_path)

@mcp.tool()
async def speak_to_telegram(text: str) -> str:
    """
    [TTS] 스피커(Mouth): 텍스트를 음성으로 변환하여 텔레그램으로 전송합니다.
    (반드시 D:/OpenClaw/.env에 TELEGRAM_CHAT_ID가 설정되어 있어야 합니다.)
    """
    import requests
    from dotenv import load_dotenv
    
    # Load Env
    env_path = r"D:/OpenClaw/.env"
    load_dotenv(env_path)
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID") # 이 ID가 있어야 전송 가능
    
    if not token or not chat_id:
        return "❌ Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in .env"
        
    # Generate TTS File
    tts_script = r"D:/OpenClaw/workspace/tts_reply.py"
    try:
        # Run tts_reply.py (It generates the file and prints the path)
        proc = subprocess.run(
            [sys.executable, tts_script, text],
            capture_output=True, text=True, encoding="utf-8"
        )
        if proc.returncode != 0:
            return f"❌ TTS Generation Error: {proc.stderr}"
            
        audio_path = proc.stdout.strip()
        if not os.path.exists(audio_path):
             # Backup: Look for known path
             audio_path = r"D:/OpenClaw/workspace/reply_voice.mp3"
             if not os.path.exists(audio_path):
                 return f"❌ Audio file not found: {audio_path}"
                 
        # Send to Telegram
        url = f"https://api.telegram.org/bot{token}/sendVoice"
        with open(audio_path, "rb") as f:
            resp = requests.post(url, data={"chat_id": chat_id}, files={"voice": f})
            
        if resp.status_code == 200:
            return f"🗣️ Voice sent to Telegram (ID: {chat_id}): '{text}'"
        else:
            return f"❌ Telegram API Error: {resp.text}"
            
    except Exception as e:
        return f"❌ Speak Error: {str(e)}"
            
# -------------------------------------------------------------------------
# 🔧 Service Control (Maintained from v3.1)
# -------------------------------------------------------------------------
@mcp.tool()
async def vivace_generate_music(genre_prompt: str, lyrics: str = "[Instrumental]") -> str:
    """
    [VIVACE] Generates high-fidelity AI music using ACE-STEP 1.5. 
    The resulting file will be sent to your Telegram once finished.
    Args:
        genre_prompt: Genre and style (e.g., 'heavy metal', 'kpop girl group')
        lyrics: Lyrics or structural tags (e.g., '[Chorus] I love AI')
    """
    from dotenv import load_dotenv
    load_dotenv(r"D:/OpenClaw/.env")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = "http://localhost:8080/api/vivace/generate"
    try:
        payload = {"prompt": genre_prompt, "lyrics": lyrics, "telegram_chat_id": chat_id}
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code == 200:
            return f"🎹 VIVACE Music Generation Started: {genre_prompt}\nFile will be sent to Telegram (ID: {chat_id}) when done."
        else:
            return f"❌ VIVACE API Error: {resp.text}"
    except Exception as e:
        return f"❌ Connection Error: Ensure VIVACE Nexus API is running on port 8080. ({str(e)})"

@mcp.tool()
async def vivace_generate_video(prompt: str) -> str:
    """
    [VIVACE] Generates SOTA AI video using Wan2.1.
    The resulting file will be sent to your Telegram once finished.
    Args:
        prompt: Detailed cinematic description of the video.
    """
    from dotenv import load_dotenv
    load_dotenv(r"D:/OpenClaw/.env")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    url = "http://localhost:8080/api/video/generate"
    try:
        payload = {"prompt": prompt, "telegram_chat_id": chat_id}
        resp = requests.post(url, json=payload, timeout=5)
        if resp.status_code == 200:
            return f"🎬 VIVACE Video Generation Started: {prompt}\nFile will be sent to Telegram (ID: {chat_id}) when done."
        else:
            return f"❌ VIVACE Video API Error: {resp.text}"
    except Exception as e:
        return f"❌ Connection Error: Ensure VIVACE Nexus API is running on port 8080. ({str(e)})"

@mcp.tool()
async def nexus_god_execute(command: str, domain: str = "system") -> str:
    """[God Mode] Legacy Alias for system_cmd with domain context."""
    cwd = DOMAINS.get(domain.lower(), Path("C:/"))
    if not cwd.exists(): return f"❌ Domain {domain} path not found."
    return await system_cmd(command, cwd=str(cwd))

if __name__ == "__main__":
    mcp.run()
