import requests
import time
import json

url = "http://localhost:8090/api/chat/pony"
payload = {
    "user_prompt": "Hello Pony!",
    "max_tokens": 10
}

try:
    start_time = time.time()
    response = requests.post(url, json=payload, timeout=30)
    end_time = time.time()
    
    latency = end_time - start_time
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success! Latency: {latency:.2f}s")
        print(f"Content: {data.get('content', 'No content')}")
    else:
        print(f"❌ Failed! Status Code: {response.status_code}")
        print(f"Error: {response.text}")
except Exception as e:
    print(f"❌ Connection Error: {str(e)}")
