# ============================================================================
# Ollama Model Manager
# ============================================================================
# 모델 목록 확인, 풀링, 삭제 관리
#
# Usage:
#   python ollama_model_manager.py list    # 모델 목록
#   python ollama_model_manager.py pull llama3.2  # 모델 풀링
#   python ollama_model_manager.py rm anthropic/xxx  # 모델 삭제
# ============================================================================

import subprocess
import sys
import json
import requests
from typing import List, Dict

OLLAMA_HOST = "http://localhost:11434"


def get_models() -> List[Dict]:
    """Ollama 모델 목록 조회"""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if resp.status_code == 200:
            return resp.json().get("models", [])
    except Exception as e:
        print(f"Error: {e}")
    return []


def list_models():
    """모델 목록 출력"""
    print("\n" + "=" * 50)
    print("OLLAMA MODEL LIST")
    print("=" * 50)
    
    models = get_models()
    
    if not models:
        print("No models found. Ollama may not be running.")
        print("\nStart Ollama with: ollama serve")
        return
    
    for model in models:
        name = model.get("name", "unknown")
        size = model.get("size", 0)
        size_gb = size / (1024**3) if size else 0
        
        # 모델 파싱
        if ":" in name:
            base, tag = name.split(":", 1)
        else:
            base, tag = name, "latest"
        
        print(f"\n  [{tag:15}] {base}")
        print(f"  Size: {size_gb:.2f} GB")
    
    print("\n" + "=" * 50)
    print(f"Total: {len(models)} models")
    print("=" * 50)


def pull_model(model_name: str):
    """모델 풀링"""
    print(f"\nPulling model: {model_name}")
    print("-" * 30)
    
    try:
        payload = {"name": model_name}
        resp = requests.post(f"{OLLAMA_HOST}/api/pull", json=payload, stream=True)
        
        if resp.status_code == 200:
            print("Pulling...")
            for line in resp.iter_lines():
                if line:
                    data = json.loads(line)
                    status = data.get("status", "")
                    if "digest" in data:
                        print(f"  {status}: {data['digest'][:12]}")
                    else:
                        print(f"  {status}")
            print("\nModel pulled successfully!")
        else:
            print(f"Failed: {resp.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")


def delete_model(model_name: str):
    """모델 삭제"""
    print(f"\nDeleting model: {model_name}")
    
    try:
        resp = requests.delete(f"{OLLAMA_HOST}/api/delete", json={"name": model_name})
        if resp.status_code == 200:
            print("Model deleted!")
        else:
            print(f"Failed: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")


def check_connection():
    """Ollama 연결 확인"""
    print(f"\nChecking Ollama at {OLLAMA_HOST}...")
    
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/version", timeout=5)
        if resp.status_code == 200:
            version = resp.json().get("version", "unknown")
            print(f"Ollama Version: {version}")
            return True
    except Exception as e:
        print(f"Connection failed: {e}")
        print("\nStart Ollama with: ollama serve")
    return False


def show_recommended_models():
    """권장 모델 목록"""
    print("""
========================================
RECOMMENDED MODELS FOR OPENCLAW
========================================

Lightweight (2-4GB VRAM):
  - llama3.2:1b
  - qwen2.5:0.5b
  - phi3:3.8b

Standard (4-8GB VRAM):
  - llama3.2:3b
  - llama3.1:8b
  - qwen2.5:7b
  - mistral:7b

Multimodal (Vision):
  - llava:7b
  - qwen2-vl:7b

Coding:
  - deepseek-coder:6.7b
  - codellama:7b

========================================
Pull command example:
  ollama pull llama3.2:3b
========================================
""")


def fix_openclaw_config():
    """OpenClaw 설정에서 잘못된 모델 경로 수정"""
    print("\nChecking OpenClaw config...")
    
    config_files = [
        "openclaw_config.json",
        "config/openclaw.json",
        ".env"
    ]
    
    target_model = "anthropic/qwen2.5-coder:7b"
    replace_model = "qwen2.5:7b"  # 올바른 경로
    
    for config_file in config_files:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                content = f.read()
            
            if target_model in content:
                print(f"Found in: {config_file}")
                content = content.replace(target_model, replace_model)
                with open(config_file, 'w') as f:
                    f.write(content)
                print(f"Fixed: {target_model} -> {replace_model}")
    
    print("\nConfiguration fixed!")
    print("Restart OpenClaw with: python workspace/run_openclaw_telegram.py")


import os


def main():
    if len(sys.argv) < 2:
        print("""
========================================
Ollama Model Manager
========================================

Usage:
  python ollama_model_manager.py <command>

Commands:
  list              - Show installed models
  pull <model>      - Pull a model
  rm <model>        - Remove a model
  check             - Check Ollama connection
  recommended       - Show recommended models
  fix               - Fix OpenClaw config

Examples:
  python ollama_model_manager.py list
  python ollama_model_manager.py pull llama3.2:3b
  python ollama_model_manager.py check
========================================
""")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_models()
    elif command == "pull":
        if len(sys.argv) < 3:
            print("Usage: pull <model_name>")
        else:
            pull_model(sys.argv[2])
    elif command == "rm":
        if len(sys.argv) < 3:
            print("Usage: rm <model_name>")
        else:
            delete_model(sys.argv[2])
    elif command == "check":
        check_connection()
    elif command == "recommended":
        show_recommended_models()
    elif command == "fix":
        fix_openclaw_config()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
