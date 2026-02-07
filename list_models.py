import requests
api_key = "AIzaSyCaaK9bGlPFQfYwXkFqzLeISLYvXFY9wRY"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)
if response.status_code == 200:
    models = [m['name'] for m in response.json().get('models', [])]
    print("✅ Key is Valid! Available models:")
    for m in models:
        print(f" - {m}")
else:
    print(f"❌ Failed: {response.status_code}")
    print(response.text)
