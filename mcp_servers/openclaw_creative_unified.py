"""
🦞 OpenClaw Unified Creative Engine v2.0
=========================================
Vivace + ToonMaker + ComfyUI 완전 연동

Features:
- Music Generation (Vivace ACE-STEP)
- Video Generation (Vivace Wan2.1)
- Image Generation (ComfyUI, Flux, SDXL)
- RVC Voice Conversion (ToonMaker)
- TTS & Voice Synthesis
- Media Assembly

Author: OpenClaw Architecture Team
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# FastAPI Setup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# MCP Setup
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("OpenClaw-Creative")
except ImportError:
    mcp = None

# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {
    "vivace_api": "http://localhost:8080",
    "comfyui_api": "http://localhost:8188",
    "secretary_api": "http://localhost:8091",
    "vivace_root": r"F:\Vivace",
    "toonmaker_root": r"E:\toonmaker",
    "comfyui_root": r"E:\ComfyUI-Easy-Install",
    # ACE 1.5 Model Path
    "ace15_root": r"E:\vivace_music\ace_step_1_5",
    "ace15_checkpoints": [
        "acestep-5Hz-lm-0.6B",
        "acestep-5Hz-lm-1.7B",
        "acestep-v15-turbo"
    ]
}

app = FastAPI(
    title="OpenClaw Unified Creative Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODELS
# ============================================================

class MusicRequest(BaseModel):
    title: str = ""
    prompt: str
    lyrics: str = "[Instrumental]"
    genre: str = "kpop"
    # ACE 1.5 Options
    use_ace15: bool = True
    ace15_model: str = "acestep-v15-turbo"  # 0.6B, 1.7B, v15-turbo

class ImageRequest(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024
    steps: int = 20

class VideoRequest(BaseModel):
    prompt: str
    duration: int = 6

class TTSRequest(BaseModel):
    text: str
    voice: str = "default"

class MediaAssemblyRequest(BaseModel):
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    image_paths: List[str] = []

# ============================================================
# ENGINES
# ============================================================

class ACE15Engine:
    """ACE 1.5 Audio Generation (Vivace Embedded)"""
    
    def __init__(self):
        self.root = CONFIG["ace15_root"]
        self.checkpoints = CONFIG["ace15_checkpoints"]
    
    async def get_available_models(self) -> List[str]:
        """사용 가능한 ACE 1.5 모델 목록"""
        available = []
        for model in self.checkpoints:
            model_path = Path(self.root) / "checkpoints" / model
            if model_path.exists():
                available.append(model)
        return available
    
    async def generate_music(
        self,
        prompt: str,
        lyrics: str = "[Instrumental]",
        model: str = "acestep-v15-turbo",
        duration: int = 180
    ) -> Dict:
        """ACE 1.5로 음악 생성"""
        model_path = Path(self.root) / "checkpoints" / model
        
        if not model_path.exists():
            return {"status": "error", "message": f"Model not found: {model}"}
        
        # Vivace API 호출 (ACE 1.5 지원)
        try:
            import httpx
            resp = httpx.post(
                f"{CONFIG['vivace_api']}/api/ace/generate",
                json={
                    "prompt": prompt,
                    "lyrics": lyrics,
                    "model": str(model_path),
                    "duration": duration
                },
                timeout=120
            )
            return {"status": "submitted", "engine": "ACE-1.5", "model": model}
        except Exception as e:
            # Direct execution fallback
            return {
                "status": "direct_execution",
                "command": f"python {self.root}/generate.py --prompt '{prompt}' --model {model}",
                "model_path": str(model_path)
            }
    
    async def get_model_info(self, model: str) -> Dict:
        """모델 정보 조회"""
        return {
            "model": model,
            "path": str(Path(self.root) / "checkpoints" / model),
            "size": "Check file size"
        }


class VivaceEngine:
    """Vivace (음악/비디오 생성)"""
    
    def __init__(self):
        self.ace15 = ACE15Engine()
    
    async def generate_music(self, req: MusicRequest) -> Dict:
        """음악 생성 (ACE 1.5 지원)"""
        if req.use_ace15:
            return await self.ace15.generate_music(
                prompt=req.prompt,
                lyrics=req.lyrics,
                model=req.ace15_model
            )
        
        # Fallback to original Vivace API
        try:
            import httpx
            resp = httpx.post(
                f"{CONFIG['vivace_api']}/api/vivace/generate",
                json=req.model_dump(),
                timeout=30
            )
            return {"status": "submitted", "result": resp.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def generate_music(self, req: MusicRequest) -> Dict:
        try:
            import httpx
            resp = httpx.post(
                f"{CONFIG['vivace_api']}/api/vivace/generate",
                json=req.model_dump(),
                timeout=30
            )
            return {"status": "submitted", "result": resp.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def generate_video(self, req: VideoRequest) -> Dict:
        try:
            import httpx
            resp = httpx.post(
                f"{CONFIG['vivace_api']}/api/video/generate",
                json=req.model_dump(),
                timeout=30
            )
            return {"status": "submitted", "result": resp.json()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class ComfyUIEngine:
    """ComfyUI (이미지 생성)"""
    
    async def generate_image(self, req: ImageRequest) -> Dict:
        try:
            import httpx
            workflow = {
                "prompt": {
                    "inputs": [
                        {"class_type": "CLIPTextEncode", "inputs": {"text": req.prompt}},
                        {"class_type": "KSampler", "inputs": {"steps": req.steps}},
                        {"class_type": "SaveImage", "inputs": {"filename_prefix": f"openclaw_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}}
                    ]
                }
            }
            resp = httpx.post(f"{CONFIG['comfyui_api']}/prompt", json=workflow, timeout=30)
            return {"status": "submitted", "job_id": resp.json().get("prompt_id")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class ToonMakerEngine:
    """ToonMaker (RVC)"""
    
    async def get_voice_models(self) -> List[str]:
        voice_dir = Path(CONFIG["toonmaker_root"]) / "models" / "rvc"
        if voice_dir.exists():
            return [f.name for f in voice_dir.glob("*.pth")]
        return []

class SecretaryEngine:
    """Secretary (TTS)"""
    
    async def generate_tts(self, req: TTSRequest) -> Dict:
        try:
            import httpx
            resp = httpx.post(
                f"{CONFIG['secretary_api']}/services/tts",
                json={"text": req.text, "speaker_id": req.voice},
                timeout=60
            )
            return {"status": "success", "file": resp.json().get("file")}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class MediaEditor:
    """미디어 편집"""
    
    async def assemble(self, req: MediaAssemblyRequest) -> Dict:
        return {"status": "assembly_started", "components": req.model_dump()}

# Initialize
vivace = VivaceEngine()
comfyui = ComfyUIEngine()
toonmaker = ToonMakerEngine()
secretary = SecretaryEngine()
editor = MediaEditor()

# ============================================================
# API ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "OpenClaw Unified Creative Engine v2.0",
        "status": "online",
        "engines": ["vivace", "comfyui", "toonmaker", "secretary"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/music/generate")
async def generate_music(req: MusicRequest):
    return await vivace.generate_music(req)

@app.post("/image/generate")
async def generate_image(req: ImageRequest):
    return await comfyui.generate_image(req)

@app.post("/video/generate")
async def generate_video(req: VideoRequest):
    return await vivace.generate_video(req)

@app.post("/tts/generate")
async def generate_tts(req: TTSRequest):
    return await secretary.generate_tts(req)

@app.get("/voice/models")
async def list_voice_models():
    return {"models": await toonmaker.get_voice_models()}

# --- ACE 1.5 ---
@app.get("/ace15/models")
async def list_ace15_models():
    """사용 가능한 ACE 1.5 모델 목록"""
    return {
        "models": CONFIG["ace15_checkpoints"],
        "root": CONFIG["ace15_root"]
    }

@app.post("/ace15/generate")
async def generate_ace15_music(
    prompt: str,
    lyrics: str = "[Instrumental]",
    model: str = "acestep-v15-turbo"
):
    """ACE 1.5 음악 생성"""
    return await vivace.ace15.generate_music(prompt, lyrics, model)

@app.post("/media/assemble")
async def assemble_media(req: MediaAssemblyRequest):
    return await editor.assemble(req)

# ============================================================
# MCP TOOLS
# ============================================================

if mcp:
    @mcp.tool()
    async def creative_generate_music(title: str = "", prompt: str = "", lyrics: str = "[Instrumental]", genre: str = "kpop") -> str:
        """
        [Creative] Vivace를 사용하여 음악을 생성합니다.
        """
        req = MusicRequest(title=title, prompt=prompt, lyrics=lyrics, genre=genre)
        result = await vivace.generate_music(req)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_generate_image(prompt: str, width: int = 1024, height: int = 1024) -> str:
        """
        [Creative] ComfyUI를 사용하여 이미지를 생성합니다.
        """
        req = ImageRequest(prompt=prompt, width=width, height=height)
        result = await comfyui.generate_image(req)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_generate_video(prompt: str, duration: int = 6) -> str:
        """
        [Creative] Vivace Wan2.1을 사용하여 비디오를 생성합니다.
        """
        req = VideoRequest(prompt=prompt, duration=duration)
        result = await vivace.generate_video(req)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_generate_tts(text: str, voice: str = "default") -> str:
        """
        [Creative] TTS 음성을 생성합니다.
        """
        req = TTSRequest(text=text, voice=voice)
        result = await secretary.generate_tts(req)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_get_voice_models() -> str:
        """
        [Creative] 사용 가능한 RVC 음성 모델 목록을 반환합니다.
        """
        models = await toonmaker.get_voice_models()
        return json.dumps({"models": models}, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_ace15_generate(
        prompt: str,
        lyrics: str = "[Instrumental]",
        model: str = "acestep-v15-turbo"
    ) -> str:
        """
        [Creative] ACE 1.5로 음악을 생성합니다.
        Models: ace-step-5Hz-lm-0.6B, ace-step-5Hz-lm-1.7B, ace-step-v15-turbo
        """
        result = await vivace.ace15.generate_music(prompt, lyrics, model)
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_ace15_list_models() -> str:
        """
        [Creative] 사용 가능한 ACE 1.5 모델 목록을 반환합니다.
        """
        available = await vivace.ace15.get_available_models()
        return json.dumps({
            "available_models": available,
            "all_models": CONFIG["ace15_checkpoints"]
        }, indent=2, ensure_ascii=False)
    
    @mcp.tool()
    async def creative_get_status() -> str:
        """
        [Creative] 크리에이티브 엔진 상태를 확인합니다.
        """
        return """Creative Engine Status
========================
Status: Online

Available Features:
- Music Generation (Vivace ACE-STEP)
- Video Generation (Wan2.1)
- Image Generation (ComfyUI)
- TTS Synthesis
- RVC Voice Conversion
- Media Assembly"""

if __name__ == "__main__":
    print("Starting OpenClaw Unified Creative Engine v2.0...")
    uvicorn.run(app, host="0.0.0.0", port=8096)
