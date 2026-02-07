import os
import time
import json
import subprocess
import sys

# 설정
WATCH_DIR = r"C:\Users\JayPark1004\.openclaw\media\inbound"
PIPELINE_SCRIPT = r"D:\OpenClaw\workspace\voice_pipeline.py"
PROCESSED_FILES = set()

def process_file(filepath):
    """
    음성 파일 발견 -> 파이프라인(STT+Router) 실행 -> 결과 처리
    """
    print(f"\n🎧 New Audio Detected: {os.path.basename(filepath)}")
    
    # 1. Pipeline Execution
    try:
        result = subprocess.run(
            [sys.executable, PIPELINE_SCRIPT, filepath],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        output_json = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Pipeline Error: {e.stderr}")
        return
    except json.JSONDecodeError:
        print(f"❌ JSON Parse Error: {result.stdout}")
        return
    
    # 2. Result Handling
    mode = output_json.get("mode")
    text = output_json.get("cleaned_text", "")
    reason = output_json.get("reason", "")
    
    print(f"   Mode: {mode}")
    print(f"   Text: {text}")
    
    if mode == "rejected":
        print(f"🚫 Rejected: {reason}")
        return

    if not text:
        print("⚠️ No text transcribed.")
        return

    # 3. Inject into OpenClaw & Auto-Reply Flow
    print(f"🚀 Processing Message: '{text}'")
    
    try:
        # .env 로드 (토큰 정보 획득)
        from dotenv import load_dotenv
        load_dotenv(r"D:\OpenClaw\.env")
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        oc_token = "c0b4dc439175325c5ee573f71c05e0483126adf20b67f2a8" # openclaw.json의 gateway.auth.token

        # 1. OpenClaw Agent 호출 (Gateway에 연결하도록 토큰 주입)
        # 환경 변수에 OPENCLAW_TOKEN을 넣어주면 CLI가 게이트웨이에 자동 접속합니다.
        env = os.environ.copy()
        env["OPENCLAW_TOKEN"] = oc_token
        
        result = subprocess.run(
            ["openclaw", "agent", "--agent", "main", "--message", text],
            capture_output=True, text=True, encoding='utf-8', env=env
        )
        raw_output = result.stdout.strip()
        
        # 2. 실질적인 답변 추출 (로고 등 제외)
        lines = raw_output.splitlines()
        agent_reply = ""
        found_start = False
        for line in lines:
            if "◇" in line:
                found_start = True
                continue
            if found_start and line.strip() and not ("Exit code" in line):
                agent_reply += line.strip() + " "
        
        agent_reply = agent_reply.strip()
        if not agent_reply:
            agent_reply = lines[-1].strip() if lines else ""

        # 3. 음성 답변 전송
        if agent_reply and len(agent_reply) > 2:
            print(f"🤖 Extracted Reply: {agent_reply[:60]}...")
            
            if token and chat_id:
                tts_script = r"D:\OpenClaw\workspace\tts_reply.py"
                proc_tts = subprocess.run([sys.executable, tts_script, agent_reply], capture_output=True, text=True, encoding='utf-8')
                audio_path = proc_tts.stdout.strip()
                
                if audio_path and os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                    import requests
                    url = f"https://api.telegram.org/bot{token}/sendVoice"
                    with open(audio_path, "rb") as f:
                        requests.post(url, data={"chat_id": chat_id}, files={"voice": f})
                    print(f"🗣️ Voice Reply Sent to Telegram!")
                else:
                    print(f"⚠️ TTS Error or empty file: {audio_path}")
            else:
                print("⚠️ Missing Telegram Token or Chat ID.")
             
    except Exception as e:
        print(f"❌ Voice Loop Error: {e}")

def main():
    print(f"👀 Watching directory: {WATCH_DIR}...")
    
    if os.path.exists(WATCH_DIR):
        for f in os.listdir(WATCH_DIR):
            PROCESSED_FILES.add(f)
            
    while True:
        try:
            if not os.path.exists(WATCH_DIR):
                time.sleep(2)
                continue
                
            files = os.listdir(WATCH_DIR)
            for f in files:
                if f not in PROCESSED_FILES and f.endswith(('.ogg', '.mp3', '.wav', '.m4a')):
                    filepath = os.path.join(WATCH_DIR, f)
                    time.sleep(1) 
                    process_file(filepath)
                    PROCESSED_FILES.add(f)
            
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
