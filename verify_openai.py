import os
import requests

api_key = os.environ.get("OPENAI_API_KEY")
url = "https://api.openai.com/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Successfully authenticated with OpenAI API.")
        models = response.json().get("data", [])
        gpt_models = [m['id'] for m in models if 'gpt' in m['id']]
        print(f"Available GPT models: {gpt_models[:10]}")
    else:
        print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
