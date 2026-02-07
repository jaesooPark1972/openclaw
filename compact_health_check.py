import os
import requests
import json

def test_gemini(key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {"contents": [{"parts": [{"text": "hi"}]}]}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.status_code == 200, resp.status_code
    except Exception as e:
        return False, str(e)

def test_openai(key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.status_code == 200, resp.status_code
    except Exception as e:
        return False, str(e)

def test_deepseek(key):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.status_code == 200, resp.status_code
    except Exception as e:
        return False, str(e)

def test_groq(key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.status_code == 200, resp.status_code
    except Exception as e:
        return False, str(e)

keys = {
    "Gemini": "AIzaSyBDxhuIGzo86O3IQSYLK0xwGQoKZTirOSo",
    "DeepSeek": "sk-d41eebdc2534436a9be5bc96f9657163",
    "OpenAI": "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",
    "Groq": "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"
}

for name, key in keys.items():
    success, info = (False, "N/A")
    if name == "Gemini": success, info = test_gemini(key)
    elif name == "OpenAI": success, info = test_openai(key)
    elif name == "DeepSeek": success, info = test_deepseek(key)
    elif name == "Groq": success, info = test_groq(key)
    print(f"{name}: {'OK' if success else 'FAILED'} (Status: {info})")
