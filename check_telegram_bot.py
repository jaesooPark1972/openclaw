
import requests
import json
import sys

TOKENS = [
    "8249306655:AAE6snmV8AR63O-4-sFind-gSx8CjhjgFuk",
    "8184968462:AAGQiOe504_16q6AQ1X_axE3gsQ8lYs4AbI"
]

def check_tokens():
    for token in TOKENS:
        url = f"https://api.telegram.org/bot{token}/getMe"
        try:
            print(f"Checking token: {token[:10]}...")
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    user = data["result"]
                    print(f"✅ SUCCESS! Bot Name: {user.get('first_name')} | Username: @{user.get('username')} | ID: {user.get('id')}")
                else:
                    print(f"❌ Invalid response: {data}")
            else:
                print(f"❌ HTTP {resp.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 30)

if __name__ == "__main__":
    check_tokens()
