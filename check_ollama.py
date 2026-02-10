
import requests
import json
import sys

def check_ollama():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5-coder:7b",
        "prompt": "Hello via API",
        "stream": False
    }
    try:
        print(f"Testing Ollama connectivity to {url} with model qwen2.5-coder:7b...")
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Ollama is responding!")
            print(f"Response: {response.json().get('response')}")
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = check_ollama()
    sys.exit(0 if success else 1)
