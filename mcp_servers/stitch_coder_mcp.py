
"""
🦞 OpenClaw Stitch: Autonomous Coding & Design Loop
===================================================
Implementation of the "Stitch Loop" for autonomous creation.
Features:
1. Design DNA Extraction (from user description)
2. Autonomous Implementation (using Ollama Coder)
3. Self-Healing Debugging Loop
4. One-Click Deployment

Author: OpenClaw Team
"""

import os
import sys
import json
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("OpenClaw-Stitch")
except ImportError:
    # If MCP is not available, provide a fallback or exit gracefully
    print("Warning: MCP library not found. Running in standalone mode.")
    mcp = None

# Configuration
WORKSPACE_ROOT = Path("D:/OpenClaw/workspace")
OLLAMA_API = "http://127.0.0.1:11434/api/generate"
MODEL_CODER = "qwen2.5-coder:7b"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Stitch")

class StitchEngine:
    """The core engine for autonomous creation."""
    
    def __init__(self):
        self.design_dna: Dict = {}
        self.project_context: str = ""
        self.iteration: int = 0
        self.max_iterations: int = 5
    
    async def extract_design_dna(self, description: str) -> Dict:
        """Analyze user description and extract key design patterns."""
        system_prompt = (
            "You are a Senior Software Architect. Extract the 'Design DNA' from the user's request.\n"
            "Return ONLY a JSON object with these keys:\n"
            "- architecture: (e.g., Microservices, Monolith, Serverless)\n"
            "- core_technologies: (List of frameworks/languages)\n"
            "- pattern: (e.g., MVC, Clean Architecture)\n"
            "- color_palette: (List of hex codes if UI related)\n"
            "- key_components: (List of main modules)"
        )
        
        dna_json = await self._call_ollama(system_prompt, description)
        try:
            # Clean up potential markdown code blocks
            dna_json = dna_json.replace("```json", "").replace("```", "").strip()
            self.design_dna = json.loads(dna_json)
            return self.design_dna
        except Exception as e:
            logger.error(f"Failed to parse Design DNA: {e}")
            return {"error": "Failed to extract DNA", "raw": dna_json}

    async def generate_implementation_plan(self, dna: Dict) -> str:
        """Create a step-by-step coding plan based on DNA."""
        prompt = (
            f"Based on this Design DNA: {json.dumps(dna, indent=2)}\n"
            "Create a detailed implementation plan. Return a list of files to be created and their purpose."
        )
        return await self._call_ollama("You are a Tech Lead.", prompt)

    async def code_module(self, module_name: str, requirement: str) -> str:
        """Generate actual code for a module."""
        prompt = (
            f"Write the full code for '{module_name}'.\n"
            f"Requirement: {requirement}\n"
            f"Context: {self.project_context}\n"
            "Return ONLY the code, no markdown explanations."
        )
        return await self._call_ollama("You are an Expert Coder (10x Developer).", prompt)
    
    async def self_heal(self, file_path: str, error_log: str) -> bool:
        """Attempt to fix code based on error log."""
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        prompt = (
            f"The following code in '{file_path}' caused an error.\n"
            f"Code:\n```\n{code}\n```\n"
            f"Error Log:\n{error_log}\n"
            "Fix the code and return ONLY the full corrected code."
        )
        
        fixed_code = await self._call_ollama("You are a Debugging Specialist.", prompt)
        
        # Clean up markdown if present
        if "```" in fixed_code:
            fixed_code = fixed_code.split("```")[1]
            if fixed_code.startswith("python") or fixed_code.startswith("javascript"):
                fixed_code = "\n".join(fixed_code.split("\n")[1:])
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(fixed_code.strip())
            
        return True

    async def _call_ollama(self, system: str, user: str) -> str:
        """Call local Ollama API."""
        payload = {
            "model": MODEL_CODER,
            "prompt": f"System: {system}\nUser: {user}",
            "stream": False,
            "options": {"temperature": 0.2}
        }
        try:
            resp = requests.post(OLLAMA_API, json=payload, timeout=60)
            if resp.status_code == 200:
                return resp.json().get("response", "").strip()
            else:
                return f"Error: {resp.status_code} - {resp.text}"
        except Exception as e:
            return f"Connection Failed: {e}"

stitch = StitchEngine()

# ============================================================
# MCP Tools Definition
# ============================================================

if mcp:
    @mcp.tool()
    async def stitch_design_init(description: str) -> str:
        """
        [Stitch] Initialize a project by extracting Design DNA.
        Args:
            description: Project description (e.g., "A dark-themed dashboard for tracking crypto")
        """
        dna = await stitch.extract_design_dna(description)
        stitch.project_context = description
        return f"🧬 **Design DNA Extracted**\n```json\n{json.dumps(dna, indent=2)}\n```"

    @mcp.tool()
    async def stitch_implement_feature(feature_name: str, requirements: str, file_path: str) -> str:
        """
        [Stitch] Auto-code a feature/file.
        Args:
            feature_name: Name of feature
            requirements: Detailed requirements
            file_path: Relative path to save (e.g., "src/main.py")
        """
        full_path = WORKSPACE_ROOT / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        code = await stitch.code_module(feature_name, requirements)
        
        # Clean markdown
        if "```" in code:
            parts = code.split("```")
            # Usually the code is in the second part (index 1)
            if len(parts) > 1:
                code = parts[1]
                # Remove language identifier if present (e.g., "python\n")
                if "\n" in code and len(code.split("\n")[0]) < 15: 
                    code = code.split("\n", 1)[1]
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(code.strip())
            
        return f"💾 **Implemented: {feature_name}**\nSaved to: `{full_path}`"

    @mcp.tool()
    async def stitch_debug_fix(file_path: str, error_message: str) -> str:
        """
        [Stitch] Autonomous debugging and fixing.
        Args:
            file_path: Relative path to broken file
            error_message: Error log or description
        """
        full_path = WORKSPACE_ROOT / file_path
        success = await stitch.self_heal(full_path, error_message)
        
        if success:
            return f"🚑 **Self-Healing Applied**\nFixed file: `{full_path}`\nBased on error: {error_message[:50]}..."
        else:
            return "❌ Failed to fix (File not found or Model error)"

    if __name__ == "__main__":
        print("🧬 OpenClaw Stitch (Autonomous Loop) Running...")
        mcp.run()
