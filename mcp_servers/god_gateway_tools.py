"""
🦞 God Gateway MCP Tools - Everything Search & Engram Integration
==================================================================
Tools for: Everything Search, Engram Memory, Vector Search
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from typing import Optional, List

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("God-Gateway-Tools")
except ImportError:
    print("⚠️ MCP not installed")
    sys.exit(1)

# Configuration
EVERYTHING_EXE = r"C:\Program Files\Everything\Everything.exe"
ENGRAM_API = "http://localhost:8082"  # Engram MCP server
GOD_GATEWAY_API = "http://localhost:8085"

# ============================================================
# EVERYTHING SEARCH TOOLS
# ============================================================

@mcp.tool()
async def everything_search(query: str, limit: int = 50) -> str:
    """
    [Everything] Search for files on Windows desktop using Everything.
    Extremely fast file search across all drives.
    Args:
        query: Search query (Everything syntax supported)
        limit: Maximum results to return (default: 50)
    """
    try:
        result = subprocess.run(
            [EVERYTHING_EXE, "-n", str(limit), query],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        files = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        
        if not files:
            return f"🔍 No files found for: '{query}'"
        
        output = f"📂 **Search Results for '{query}'** ({len(files)} files)\n\n"
        for f in files[:20]:  # Limit output
            output += f"• {f}\n"
        
        if len(files) > 20:
            output += f"\n... and {len(files) - 20} more files"
        
        return output
    except Exception as e:
        return f"❌ Everything Search Error: {str(e)}"

@mcp.tool()
async def everything_search_code(query: str, extensions: str = "py,ts,js,md") -> str:
    """
    [Everything] Search for code files with specific extensions.
    Args:
        query: Code search query
        extensions: Comma-separated extensions (e.g., "py,ts,js")
    """
    exts = [e.strip() for e in extensions.split(",")]
    ext_pattern = " OR ".join([f"*.{e}" for e in exts])
    full_query = f'{query} {ext_pattern}'
    
    return await everything_search(full_query, limit=30)

@mcp.tool()
async def everything_find_large_files(min_size_mb: int = 100) -> str:
    """
    [Everything] Find large files on the system.
    Args:
        min_size_mb: Minimum file size in MB
    """
    size_filter = f"size:>{min_size_mb}mb"
    return await everything_search(size_filter, limit=20)

# ============================================================
# ENGRAM MEMORY TOOLS
# ============================================================

@mcp.tool()
async def engram_remember(content: str, tags: str = "", context: str = "") -> str:
    """
    [Engram] Store a semantic memory for later recall.
    Args:
        content: The information to remember
        tags: Comma-separated tags for filtering
        context: Source file or context path
    """
    try:
        import httpx
        
        # Try local Engram MCP first, then fallback to HTTP
        try:
            from mcp_engram import engram_remember as local_remember
            result = await local_remember(content, tags, context)
            return result
        except ImportError:
            pass
        
        # Fallback to HTTP API
        resp = httpx.post(
            f"{ENGRAM_API}/remember",
            json={"content": content, "tags": tags, "context": context},
            timeout=10
        )
        
        if resp.status_code == 200:
            return f"🧠 **Memory Stored**\n\nContent: {content[:200]}...\nTags: {tags}"
        else:
            return f"❌ Memory store failed: {resp.text}"
    except Exception as e:
        return f"❌ Engram Error: {str(e)}"

@mcp.tool()
async def engram_recall(query: str, n_results: int = 5) -> str:
    """
    [Engram] Recall memories related to a query.
    Args:
        query: Semantic search query
        n_results: Number of results to return
    """
    try:
        import httpx
        
        resp = httpx.post(
            f"{ENGRAM_API}/recall",
            json={"query": query, "n_results": n_results},
            timeout=10
        )
        
        if resp.status_code == 200:
            memories = resp.json()
            if not memories:
                return f"🔍 No memories found for: '{query}'"
            
            output = f"🧠 **Recalled Memories** for '{query}'\n\n"
            for i, m in enumerate(memories[:5]):
                output += f"{i+1}. {m.get('content', '')[:300]}...\n\n"
            
            return output
        else:
            return f"❌ Recall failed: {resp.text}"
    except Exception as e:
        return f"❌ Engram Error: {str(e)}"

@mcp.tool()
async def engram_search_code(function_name: str, language: str = "python") -> str:
    """
    [Engram] Search for previously saved code or functions.
    Args:
        function_name: Name of the function/class to find
        language: Programming language
    """
    query = f"{function_name} code implementation {language}"
    return await engram_recall(query, n_results=3)

# ============================================================
# GOD GATEWAY INTEGRATION
# ============================================================

@mcp.tool()
async def god_gateway_search(query: str, mode: str = "hybrid") -> str:
    """
    [God Gateway] Unified search across all indexed content.
    Uses vector search + keyword search hybrid.
    Args:
        query: Search query
        mode: 'vector', 'keyword', or 'hybrid'
    """
    try:
        import httpx
        
        resp = httpx.post(
            f"{GOD_GATEWAY_API}/memory/search",
            json={"query": query, "top_k": 5, "mode": mode},
            timeout=30
        )
        
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            
            if not results:
                return f"🔍 No results for: '{query}'"
            
            output = f"🔮 **God Gateway Search** for '{query}'\n\n"
            for r in results[:5]:
                content = r.get("content", r.get("text", ""))[:200]
                output += f"• {content}...\n\n"
            
            return output
        else:
            return f"❌ Search failed: {resp.text}"
    except Exception as e:
        return f"❌ God Gateway Error: {str(e)}"

@mcp.tool()
async def god_gateway_index_domain(domain: str) -> str:
    """
    [God Gateway] Index a domain for semantic search.
    Domains: openclaw, vivace, comfyui, agen, rust
    Args:
        domain: Domain name to index
    """
    try:
        import httpx
        
        resp = httpx.post(
            f"{GOD_GATEWAY_API}/memory/index-domain",
            params={"domain": domain},
            timeout=300  # Long timeout for indexing
        )
        
        if resp.status_code == 200:
            data = resp.json()
            return f"📦 **Indexing Complete**\n\nDomain: {domain}\nFiles indexed: {data.get('count', 0)}"
        else:
            return f"❌ Indexing failed: {resp.text}"
    except Exception as e:
        return f"❌ God Gateway Error: {str(e)}"

@mcp.tool()
async def god_gateway_get_status() -> str:
    """
    [God Gateway] Get status of all domains and services.
    """
    try:
        import httpx
        
        resp = httpx.get(f"{GOD_GATEWAY_API}/health", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return f"🟢 **God Gateway Status**\n\nStatus: {data.get('status')}\nVector DB: {'Active' if data.get('vector_db') else 'Inactive'}\nPostgreSQL: {'Active' if data.get('postgres') else 'Inactive'}"
        else:
            return "❌ Status check failed"
    except Exception as e:
        return f"❌ God Gateway Error: {str(e)}"

# ============================================================
# FILE OPERATIONS
# ============================================================

@mcp.tool()
async def file_find_recent(extension: str = "py", count: int = 10) -> str:
    """
    [Files] Find recently modified files.
    Args:
        extension: File extension (without dot)
        count: Number of files to return
    """
    query = f"*.{extension} recent"
    return await everything_search(query, limit=count)

@mcp.tool()
async def file_grep_in_codebase(pattern: str, extensions: str = "py,ts,js") -> str:
    """
    [Files] Search for patterns in code files.
    Args:
        pattern: Text pattern to search
        extensions: File extensions
    """
    return await everything_search_code(pattern, extensions)

# ============================================================
# GOD MODE: SYSTEM CONTROL (SOVEREIGN)
# ============================================================

@mcp.tool()
async def god_mode_shell(command: str, background: bool = False) -> str:
    """
    [GOD MODE] Execute ANY shell command with Administrator privileges.
    ⚠️ USE WITH CAUTION. Full system access granted.
    Args:
        command: Windows CMD/PowerShell command
        background: Run in background (True) or wait for output (False)
    """
    try:
        import httpx
        timeout = 60.0 if not background else 5.0
        
        resp = httpx.post(
            f"{GOD_GATEWAY_API}/api/god/shell",
            json={"command": command, "background": background},
            timeout=timeout
        )
        
        if resp.status_code == 200:
            result = resp.json()
            if background:
                return f"🚀 **Command Started in Background**\nPID: {result.get('pid', 'Unknown')}\nCommand: `{command}`"
            
            status_emoji = "✅" if result.get("status") == "success" else "❌"
            return f"{status_emoji} **Command Result**\n\nStdout:\n```\n{result.get('stdout', '')}\n```\nStderr:\n```\n{result.get('stderr', '')}\n```"
        else:
            return f"❌ HTTP Error: {resp.status_code}\n{resp.text}"
            
    except Exception as e:
        return f"💥 Execution Failed: {str(e)}"

@mcp.tool()
async def god_mode_kill(identifier: str) -> str:
    """
    [GOD MODE] Force terminate a process by PID or Name.
    Args:
        identifier: Process ID (int) or Image Name (e.g., 'chrome.exe')
    """
    try:
        import httpx
        resp = httpx.post(
            f"{GOD_GATEWAY_API}/api/god/process/kill",
            params={"identifier": identifier},
            timeout=10
        )
        return f"💀 **Kill Signal Sent**: {resp.json()}"
    except Exception as e:
        return f"❌ Kill Failed: {str(e)}"

@mcp.tool()
async def god_mode_fs(action: str, path: str, content: str = None) -> str:
    """
    [GOD MODE] Direct Filesystem Manipulation.
    Args:
        action: 'write', 'read', 'delete', 'list'
        path: Absolute path
        content: File content (only for 'write')
    """
    try:
        import httpx
        payload = {"action": action, "path": path}
        if content:
            payload["content"] = content
            
        resp = httpx.post(
            f"{GOD_GATEWAY_API}/api/god/fs",
            json=payload,
            timeout=30
        )
        return f"📂 **FS Action ({action})**: {resp.json()}"
    except Exception as e:
        return f"❌ FS Error: {str(e)}"

if __name__ == "__main__":
    print("🦞 God Gateway Tools (v2 - Sovereign Mode) Running...")
    mcp.run()
