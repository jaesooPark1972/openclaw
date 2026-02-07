import requests
import time
import os
from dotenv import load_dotenv

env_path = r"D:\OpenClaw\.env"
load_dotenv(env_path)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

def get_id():
    print(f"🤖 Listening for messages on Bot (Token ends with ...{TOKEN[-5:]})...")
    print("👉 Please send a message (e.g., 'Hello') to your Telegram Bot now!")
    
    offset = None
    while True:
        try:
            params = {"timeout": 10}
            if offset:
                params["offset"] = offset
                
            resp = requests.get(URL, params=params).json()
            
            if "result" in resp:
                for update in resp["result"]:
                    # Update offset
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        chat = update["message"]["chat"]
                        chat_id = chat["id"]
                        first_name = chat.get("first_name", "User")
                        
                        print("\n✅ Message Received!")
                        print(f"👤 Name: {first_name}")
                        print(f"🆔 Chat ID: {chat_id}")
                        print("\n[Action Required]")
                        print(f"Add this line to D:\\OpenClaw\\.env :")
                        print(f"TELEGRAM_CHAT_ID={chat_id}")
                        return
                        
            time.sleep(1)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env")
    else:
        get_id()
