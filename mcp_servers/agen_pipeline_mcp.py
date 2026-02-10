"""
🎵 AGen Pipeline MCP - Music, Vision, Video Generation Tools
=============================================================
Integrates with AGen system for:
- Music generation (Full song with lyrics, vocals, mixing)
- Vision/Image generation
- Video generation
- Creative workflows
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("AGen-Pipeline-Tools")
except ImportError:
    print("⚠️ MCP not installed")
    sys.exit(1)

# Configuration
AGEN_PATH = r"F:\AGen"
AGEN_PYTHON = r"F:\AGen\.venv_titan\Scripts\python.exe"
VIVACE_API = "http://localhost:8080"
COMFYUI_API = "http://localhost:8188"

# ============================================================
# MUSIC GENERATION TOOLS
# ============================================================

@mcp.tool()
async def agenz_music_create_full_song(
    title: str,
    theme: str,
    genre: str = "kpop",
    language: str = "ko",
    bpm: int = 120
) -> str:
    """
    [AGen] Create a full song with lyrics, composition, vocals, and mixing.
    Args:
        title: Song title
        theme: Theme/prompt for the song
        genre: Music genre (kpop, ballad, rock, etc.)
        language: Language of lyrics
        bpm: Beats per minute
    """
    try:
        # Call AGen MCP server if available
        try:
            from mcp_agen_music import create_full_song
            result = await create_full_song(
                title=title,
                theme=theme,
                genre=genre,
                language=language,
                bpm=bpm
            )
            return f"🎵 **Song Creation Started**\n\nTitle: {title}\nGenre: {genre}\nTheme: {theme}\n\nResult: {result}"
        except ImportError:
            pass
        
        # Fallback: Call AGen script directly
        script_path = Path(AGEN_PATH) / "create_song.py"
        if not script_path.exists():
            return f"❌ AGen script not found: {script_path}"
        
        proc = subprocess.run(
            [AGEN_PYTHON, str(script_path), "--title", title, "--theme", theme, "--genre", genre],
            capture_output=True,
            text=True,
            timeout=600  # 10 min timeout
        )
        
        if proc.returncode == 0:
            return f"✅ **Song Created Successfully**\n\n{proc.stdout}"
        else:
            return f"❌ **Song Creation Failed**\n\n{proc.stderr}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def agenz_generate_lyrics(theme: str, language: str = "ko") -> str:
    """
    [AGen] Generate lyrics for a song based on theme.
    Args:
        theme: Theme/prompt for lyrics
        language: Language (ko, en, ja, zh)
    """
    try:
        from mcp_agen_music import generate_music_lyrics
        result = await generate_music_lyrics(theme=theme, language=language)
        return f"📝 **Generated Lyrics**\n\nTheme: {theme}\n\n{result}"
    except ImportError:
        return f"🎵 **Lyrics for '{theme}'**\n\n[Verse 1]\n...\n\n[Chorus]\n...\n\n(Note: Use AGen MCP server for full lyrics generation)"

# ============================================================
# VISION/IMAGE TOOLS
# ============================================================

@mcp.tool()
async def agenz_generate_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024
) -> str:
    """
    [AGen Vision] Generate an image using Flux/Sota Vision.
    Args:
        prompt: Image description
        width: Image width
        height: Image height
    """
    try:
        from mcp_sota_vision import generate_image
        result = await generate_image(prompt=prompt, width=width, height=height)
        return f"🖼️ **Image Generation Started**\n\nPrompt: {prompt}\nSize: {width}x{height}\n\nResult: {result}"
    except ImportError:
        pass
    
    # Fallback: Call ComfyUI
    try:
        import httpx
        
        # Simplified ComfyUI payload
        payload = {
            "prompt": {
                "inputs": [
                    {"class_type": "CLIPTextEncode", "inputs": {"text": prompt}},
                    {"class_type": "KSampler", "inputs": {"steps": 20}},
                ]
            }
        }
        
        resp = httpx.post(f"{COMFYUI_API}/prompt", json=payload, timeout=30)
        if resp.status_code == 200:
            return f"🎨 **ComfyUI Job Submitted**\n\nPrompt: {prompt}\nSize: {width}x{height}\n\nCheck ComfyUI UI for progress."
        else:
            return f"❌ ComfyUI Error: {resp.text}"
    except Exception as e:
        return f"❌ Image Gen Error: {str(e)}"

@mcp.tool()
async def agenz_analyze_image(image_path: str, question: str = "Describe this image") -> str:
    """
    [AGen Vision] Analyze an image using vision model.
    Args:
        image_path: Path to image file
        question: Question about the image
    """
    try:
        from mcp_vision import analyze_image_file
        result = await analyze_image_file(file_path=image_path, prompt=question)
        return f"👁️ **Image Analysis**\n\nImage: {image_path}\nQuestion: {question}\n\nResult: {result}"
    except ImportError:
        return f"🔍 **Analysis for {image_path}**\n\n(Note: Use Vision MCP server for analysis)"

# ============================================================
# VIDEO TOOLS
# ============================================================

@mcp.tool()
async def agenz_generate_video(prompt: str) -> str:
    """
    [AGen Video] Generate a 6-second video using CogVideoX.
    Args:
        prompt: Video description
    """
    try:
        from mcp_sota_video import generate_video
        result = await generate_video(prompt=prompt)
        return f"🎬 **Video Generation Started**\n\nPrompt: {prompt}\n\nResult: {result}"
    except ImportError:
        return f"🎬 **Video for '{prompt}'**\n\n(Note: Use SOTA Video MCP server for generation)"

# ============================================================
# VIVACE INTEGRATION
# ============================================================

@mcp.tool()
async def vivace_music_generate(genre: str, lyrics: str = "[Instrumental]", title: str = "") -> str:
    """
    [Vivace] Generate high-fidelity AI music using ACE-STEP 1.5.
    Args:
        genre: Genre and style
        lyrics: Lyrics or tags
        title: Optional song title
    """
    try:
        import httpx
        
        resp = httpx.post(
            f"{VIVACE_API}/api/vivace/generate",
            json={"prompt": genre, "lyrics": lyrics, "title": title},
            timeout=5
        )
        
        if resp.status_code == 200:
            return f"🎹 **Vivace Music Generation Started**\n\nGenre: {genre}\nTitle: {title}\n\nFile will be sent to Telegram when done."
        else:
            return f"❌ Vivace Error: {resp.text}"
    except Exception as e:
        return f"❌ Connection Error: Ensure Vivace API is running on port 8080. ({str(e)})"

@mcp.tool()
async def vivace_video_generate(prompt: str) -> str:
    """
    [Vivace] Generate AI video using Wan2.1.
    Args:
        prompt: Cinematic video description
    """
    try:
        import httpx
        
        resp = httpx.post(
            f"{VIVACE_API}/api/video/generate",
            json={"prompt": prompt},
            timeout=5
        )
        
        if resp.status_code == 200:
            return f"🎬 **Vivace Video Generation Started**\n\nPrompt: {prompt}\n\nFile will be sent to Telegram when done."
        else:
            return f"❌ Vivace Video Error: {resp.text}"
    except Exception as e:
        return f"❌ Connection Error: Ensure Vivace API is running on port 8080. ({str(e)})"

# ============================================================
# CREATIVE WORKFLOW TOOLS
# ============================================================

@mcp.tool()
async def agenz_plan_storyboard(song_context: str, genre: str = "Cinematic") -> str:
    """
    [AGen Creative] Plan a 4-scene storyboard for a music video.
    Args:
        song_context: Song title, lyrics, or mood
        genre: Visual style (Cyberpunk, Noir, Fantasy, etc.)
    """
    try:
        from mcp_creative import plan_storyboard
        result = await plan_storyboard(song_context=song_context, genre=genre)
        return f"🎬 **Storyboard Plan**\n\nSong: {song_context}\nGenre: {genre}\n\n{result}"
    except ImportError:
        return f"📋 **Storyboard for '{song_context}'**\n\nScene 1: [Description]\nScene 2: [Description]\nScene 3: [Description]\nScene 4: [Description]\n\n(Note: Use Creative MCP server for full storyboard)"

@mcp.tool()
async def agenz_optimize_prompt(raw_prompt: str, target_engine: str = "comfyui") -> str:
    """
    [AGen Creative] Optimize a prompt for specific AI engines.
    Args:
        raw_prompt: Original description
        target_engine: Target (comfyui, flux, sdxl)
    """
    try:
        from mcp_creative import optimize_prompt_for_engine
        result = await optimize_prompt_for_engine(raw_prompt=raw_prompt, target_engine=target_engine)
        return f"✨ **Optimized Prompt** ({target_engine})\n\nOriginal: {raw_prompt}\n\nOptimized: {result}"
    except ImportError:
        return f"🔧 **Optimized for {target_engine}**\n\n{raw_prompt}\n\n(Note: Use Creative MCP server for optimization)"

# ============================================================
# STATUS TOOLS
# ============================================================

@mcp.tool()
async def agenz_check_engine_status() -> str:
    """
    [AGen] Check status of AGen inference engines.
    """
    try:
        from mcp_agen_music import check_engine_status
        result = await check_engine_status()
        return f"🔧 **AGen Engine Status**\n\n{result}"
    except ImportError:
        return "🔧 **Engine Status**\n\n(Note: Use AGen MCP server for status)"

@mcp.tool()
async def agenz_get_ontology() -> str:
    """
    [AGen] Get the system ontology (hierarchy of all engines).
    Shows how different engines connect.
    """
    try:
        from mcp_ontology import get_system_ontology
        result = await get_system_ontology()
        return f"🧠 **System Ontology**\n\n{result}"
    except ImportError:
        return "🧠 **System Architecture**\n\n(Note: Use Ontology MCP server for details)"

if __name__ == "__main__":
    mcp.run()
