import requests
import os

# New key from F:\AGen\.env
api_key = "AIzaSyCaaK9bGlPFQfYwXkFqzLeISLYvXFY9wRY"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

payload = {
    "contents": [{
        "parts": [{"text": "Hello, are you working?"}]
    }]
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ SUCCESS: Gemini API key is valid and working!")
        print("Response:", response.json().get('candidates')[0].get('content').get('parts')[0].get('text'))
    else:
        print(f"❌ FAILED: Status Code {response.status_code}")
        print("Error:", response.text)
except Exception as e:
    print(f"⚠️ ERROR: {str(e)}")
