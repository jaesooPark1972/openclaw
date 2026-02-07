import requests

def check_gemini(key):
    # Try different versions
    for v in ["v1beta", "v1"]:
        url = f"https://generativelanguage.googleapis.com/{v}/models/gemini-1.5-flash:generateContent?key={key}"
        try:
            r = requests.post(url, json={"contents": [{"parts": [{"text": "hi"}]}]}, timeout=5)
            if r.status_code == 200: return "OK"
        except: pass
    return f"FAIL({r.status_code})"

def check_openai_compat(url, key, model):
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 5}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=5)
        if r.status_code == 200: return "OK"
        if r.status_code == 401: return "UNAUTHORIZED"
        if r.status_code == 402: return "NO_BALANCE"
        return f"FAIL({r.status_code})"
    except Exception as e:
        return f"ERROR({str(e)[:20]})"

providers = [
    ("Gemini Primary", "GEMINI", "AIzaSyBDxhuIGzo86O3IQSYLK0xwGQoKZTirOSo", ""),
    ("DeepSeek", "OPENAI_COMPAT", "sk-d41eebdc2534436a9be5bc96f9657163", "https://api.deepseek.com/chat/completions|deepseek-chat"),
    ("OpenAI Primary", "OPENAI_COMPAT", "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", "https://api.openai.com/v1/chat/completions|gpt-3.5-turbo"),
    ("Groq Primary", "OPENAI_COMPAT", "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", "https://api.groq.com/openai/v1/chat/completions|llama-3.1-8b-instant"),
    ("Groq Backup", "OPENAI_COMPAT", "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", "https://api.groq.com/openai/v1/chat/completions|llama-3.1-8b-instant"),
    ("Cerebras", "OPENAI_COMPAT", "csk-n6hjk99ch9ec6j3fvn2nyn5djxn4e44wkcyy8kd3e4e8hcnn", "https://api.cerebras.ai/v1/chat/completions|llama3.1-8b"),
    ("SambaNova", "OPENAI_COMPAT", "7384a3c4-6367-4dde-be79-b1100e8978f7", "https://api.sambanova.ai/v1/chat/completions|llama3-8b"),
]

print("--- Service Health Report ---")
for name, ptype, key, extra in providers:
    status = "UNKNOWN"
    if ptype == "GEMINI":
        status = check_gemini(key)
    else:
        url, model = extra.split("|")
        status = check_openai_compat(url, key, model)
    print(f"{name}: {status}")
