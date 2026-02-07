import os
import time
import requests
from dotenv import load_dotenv

# Load configuration
load_dotenv(r"D:\OpenClaw\.env")
WATCH_DIR = r"C:\Users\JayPark1004\.openclaw\media\inbound"
API_URL = "http://localhost:8080/api/voice/process"
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PROCESSED_FILES = set()

def process_file_turbo(filepath):
    """
    Calls the Turbo Nano API for instant STT -> Agent -> Telegram delivery
    """
    print(f"⚡ [Turbo] Processing: {os.path.basename(filepath)}")
    try:
        payload = {
            "file_path": filepath,
            "telegram_chat_id": CHAT_ID
        }
        resp = requests.post(API_URL, json=payload, timeout=60)
        if resp.status_code == 200:
            result = resp.json()
            input_text = result.get('input', 'Unknown')
            reply_text = result.get('reply', 'No reply')
            print(f"   ✅ Success: '{input_text[:30]}...' -> '{reply_text[:30]}...'")
        else:
            print(f"   ❌ API Error: {resp.status_code} - {resp.text}")
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")

def main():
    print(f"🚀 Turbo Voice Watcher Started. Monitoring: {WATCH_DIR}")
    
    # Initialize processed files to avoid re-processing old ones
    if os.path.exists(WATCH_DIR):
        for f in os.listdir(WATCH_DIR):
            PROCESSED_FILES.add(f)
            
    while True:
        try:
            if not os.path.exists(WATCH_DIR):
                time.sleep(2); continue
                
            files = os.listdir(WATCH_DIR)
            for f in files:
                if f not in PROCESSED_FILES and f.endswith(('.ogg', '.mp3', '.wav', '.m4a')):
                    filepath = os.path.join(WATCH_DIR, f)
                    
                    # Ensure file is fully written (incremental check)
                    prev_size = -1
                    while True:
                        if not os.path.exists(filepath): break
                        current_size = os.path.getsize(filepath)
                        if current_size == prev_size and current_size > 0: break
                        prev_size = current_size
                        time.sleep(0.3)
                    
                    if os.path.exists(filepath):
                        process_file_turbo(filepath)
                        PROCESSED_FILES.add(f)
            
            time.sleep(0.5) # Fast polling for responsiveness
        except KeyboardInterrupt: break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
