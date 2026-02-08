import requests
import json

url = "http://localhost:8080/api/vivace/suggest_lyrics"
payload = {"title": "Gravity", "prompt": "Rock"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
