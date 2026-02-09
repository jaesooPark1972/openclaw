import os
import requests
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=r"D:\OpenClaw\.env")

def test_google_key():
    key = os.getenv("GOOGLE_API_KEY")
    print(f"\n[Test] Checking Google API Key: {key[:10]}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": "Hello"}]}]
    }
    
    try:
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code == 200:
            print("✅ Google API Key is VALID.")
            print(f"Response: {resp.text[:50]}...")
        else:
            print(f"❌ Google API Key FAILED. Status: {resp.status_code}")
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"❌ Google Connection Error: {e}")

def test_openrouter_key():
    key = os.getenv("OPENROUTER_API_KEY")
    print(f"\n[Test] Checking OpenRouter API Key: {key[:10]}...")
    
    url = "https://openrouter.ai/api/v1/user/key" # Check credit/validity
    headers = {"Authorization": f"Bearer {key}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        # OpenRouter auth check or just try a model list
        if resp.status_code == 200:
             print("✅ OpenRouter Key is VALID (Auth check).")
        else:
            # Fallback to chat completion if /auth endpoint is different
            url_chat = "https://openrouter.ai/api/v1/chat/completions"
            payload = {
                "model": "google/gemini-2.0-flash-exp:free", # Try a free model
                "messages": [{"role": "user", "content": "hi"}]
            }
            resp2 = requests.post(url_chat, headers=headers, json=payload)
            if resp2.status_code == 200:
                print("✅ OpenRouter Key is VALID (Chat check).")
            else:
                print(f"❌ OpenRouter Key FAILED. Status: {resp2.status_code}")
                print(f"Error: {resp2.text}")
    except Exception as e:
        print(f"❌ OpenRouter Connection Error: {e}")

if __name__ == "__main__":
    test_google_key()
    test_openrouter_key()
