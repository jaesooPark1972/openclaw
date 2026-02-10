from mcp.server.fastmcp import FastMCP
import httpx
import os

# Define the MCP server
mcp = FastMCP("OpenClaw-Secretary-Tools")

API_URL = "http://localhost:8091" # Secretary Orchestrator (secretary_api.py)

@mcp.tool()
async def secretary_add_task(content: str, priority: str = "normal", due_date: str = None) -> str:
    """
    Add a task to the personal secretary's todo list.
    Args:
        content: The task description
        priority: 'high', 'normal', 'low'
        due_date: 'today', 'tomorrow', or YYYY-MM-DD
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/tasks/add", json={
            "content": content, "priority": priority, "due_date": due_date
        })
        if resp.status_code == 200:
            return f"✅ Task added: {resp.json().get('id')}"
        return f"❌ Failed to add task: {resp.text}"

@mcp.tool()
async def secretary_list_tasks(status: str = "pending") -> str:
    """List pending tasks."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/tasks/list", params={"status": status})
        tasks = resp.json()
        if not tasks: return "No pending tasks."
        
        output = "📅 **Pending Tasks**:\n"
        for t in tasks:
            output += f"- [#{t['id']}] {t['content']} ({t['priority']})\n"
        return output

@mcp.tool()
async def secretary_complete_task(task_id: int) -> str:
    """Mark a task as completed."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/tasks/{task_id}/done")
        if resp.status_code == 200:
            return f"✅ Task #{task_id} marked as done."
        return f"❌ Failed: {resp.text}"

@mcp.tool()
async def secretary_ocr_scan(image_path: str, prompt: str = "Extract all text.") -> str:
    """
    Perform OCR on an image using the GPU-accelerated service (Ollama GLM-OCR).
    Use this tool when the user uploads an image or asks for text extraction.
    """
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{API_URL}/services/ocr", json={
            "image_path": image_path, "prompt": prompt
        })
        if resp.status_code == 200:
            return resp.json().get("text", "No text found.")
        return f"❌ OCR Error: {resp.text}"

@mcp.tool()
async def secretary_voice_speak(text: str, speaker_id: str = "default") -> str:
    """
    Generate speech from text using the GPU-accelerated Qwen-TTS engine.
    Use this when the user asks to 'read' something or 'speak'.
    Returns the path to the generated audio file.
    """
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(f"{API_URL}/services/tts", json={
            "text": text, "speaker_id": speaker_id
        })
        if resp.status_code == 200:
            path = resp.json().get("file")
            return f"🔊 Audio generated at: {path}"
        return f"❌ TTS Error: {resp.text}"

if __name__ == "__main__":
    mcp.run()
