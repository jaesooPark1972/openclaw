import os
import json
import argparse
from pathlib import Path
import google.generativeai as genai

# Load Environment
def load_env():
    env_path = Path(r"C:\Users\JayPark1004\.openclaw\.env")
    if not env_path.exists():
        env_path = Path(r"D:\OpenClaw\.env")
    
    kv = {}
    if env_path.exists():
        for line in env_path.read_text(encoding='utf-8', errors='ignore').splitlines():
            if '=' in line and not line.strip().startswith('#'):
                k, v = line.split('=', 1)
                kv[k.strip()] = v.strip()
    return kv

ENV = load_env()
GEMINI_KEY = ENV.get("GEMINI_API_KEY") or ENV.get("GOOGLE_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def search_local_context(query, top_n=5):
    """
    Simulate NotebookLM 'Source' discovery using local_memory_search logic.
    """
    import subprocess
    cmd = ["python", r"C:\Users\JayPark1004\.openclaw\workspace\local_memory_search.py", query, "--top", str(top_n)]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return result.stdout

def grounded_ask(query, model_name="gemini-1.5-flash"):
    """
    Mimic NotebookLM by feeding discovered local sources into Gemini context.
    """
    sources = search_local_context(query)
    
    prompt = f"""
[NotebookLM Simulation Mode]
You are acting as an API bridge for NotebookLM. 
Below are the local source documents/fragments found in the user's workspace.
Please answer the query based ONLY on these sources. If the answer is not in the sources, say so.

SOURCE CONTEXT:
{sources}

USER QUERY:
{query}

ANSWER:
"""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="The question to ask based on your documents")
    parser.add_argument("--model", default="gemini-1.5-flash", help="Gemini model to use")
    args = parser.parse_args()

    if not GEMINI_KEY:
        print("ERROR: No Google/Gemini API key found in .env")
    else:
        print(f"--- NotebookLM API Bridge (Grounded via Gemini) ---")
        print(grounded_ask(args.query, args.model))
