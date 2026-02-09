# -*- coding: utf-8 -*-
"""
👼 God Mode Gateway (Full Bypass)
OpenClaw의 모든 제약을 우회하고, Telegram을 통해 시스템에 대한 완전한 제어 권한을 제공합니다.
WARNING: 이 게이트웨이는 매우 강력하므로 오직 주인님(ALLOWED_CHAT_ID)만 사용할 수 있어야 합니다.
"""

import os
import sys
import time
import json
import requests
import subprocess
from dotenv import load_dotenv

# Load Environment
load_dotenv(r"D:\OpenClaw\.env")

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN:
    print("❌ ERROR: Missing TELEGRAM_BOT_TOKEN")
    sys.exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_telegram(chat_id, text):
    """메시지 전송 (긴 메시지는 분할 전송)"""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    
    # 4096자 제한 처리
    if len(text) > 4000:
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        for chunk in chunks:
            payload = {"chat_id": chat_id, "text": chunk}
            requests.post(url, json=payload)
    else:
        payload = {"chat_id": chat_id, "text": text}
        requests.post(url, json=payload)

def execute_shell(command):
    """CMD/PowerShell 명령어 직접 실행 (No Safe Mode)"""
    print(f"⚡ [Shell Exec] {command}")
    try:
        # 윈도우 CMD/PowerShell 호환성 고려
        full_cmd = f"cmd /c {command}"
        result = subprocess.check_output(
            full_cmd, 
            shell=True, 
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL # 입력 대기 방지
        ).decode("cp949", errors="replace") # 한글 윈도우 인코딩 처리
        return f"✅ Executed:\n{result}"
    except subprocess.CalledProcessError as e:
        return f"❌ Exec Failed (Exit {e.returncode}):\n{e.output.decode('cp949', errors='replace')}"
    except Exception as e:
        return f"💥 System Error: {str(e)}"

def consult_antigravity(instruction):
    """Antigravity에게 복잡한 작업 위임"""
    try:
        # Force UTF-8 environment
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        # antigravity_consult.py 스킬 호출
        result = subprocess.check_output(
            ["python", r"D:\OpenClaw\workspace\skills\antigravity_consult.py", instruction],
            stderr=subprocess.STDOUT,
            env=env
        ).decode("utf-8", errors="replace") # Handle any decoding errors gracefully
        return result
    except subprocess.CalledProcessError as e:
        return f"❌ Antigravity Error: {e.output.decode('utf-8', errors='replace')}"

def vivace_action(action, prompt):
    """Vivace 창작 도구 호출"""
    try:
        payload = json.dumps({"prompt": prompt})
        result = subprocess.check_output(
            ["python", r"D:\OpenClaw\workspace\skills\vivace_control.py", action, payload],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        return result
    except subprocess.CalledProcessError as e:
        return f"❌ Vivace Error: {e.output.decode('utf-8')}"

def extract_reply(raw_output):
    """JSON 출력에서 reply만 추출"""
    try:
        # 여러 줄 출력에서 JSON 부분만 찾기
        lines = raw_output.strip().split('\n')
        json_str = ""
        in_json = False
        for line in lines:
            if line.strip().startswith('{'):
                in_json = True
            if in_json:
                json_str += line + '\n'
            if line.strip().endswith('}'):
                break
        
        if json_str:
            data = json.loads(json_str)
            if data.get("status") == "success" and "reply" in data:
                return data["reply"]
            elif data.get("status") == "error":
                return f"❌ 에러: {data.get('message', 'Unknown error')}"
        return raw_output  # JSON 파싱 실패 시 원본 반환
    except:
        return raw_output  # 파싱 실패 시 원본 반환

def process_command(chat_id, command):
    """명령어 처리 라우터"""
    
    # 1. 시스템 명령어 (/exec) - 최상위 권한
    if command.startswith("/exec "):
        cmd_text = command[6:].strip()
        result = execute_shell(cmd_text)
        send_telegram(chat_id, result)
        return

    # 2. 안티에게 질문 (/ask) - 복잡한 추론
    if command.startswith("/ask "):
        query = command[5:].strip()
        raw_result = consult_antigravity(query)
        clean_reply = extract_reply(raw_result)
        send_telegram(chat_id, clean_reply)
        return

    # 3. Vivace 창작 (/img, /music)
    if command.startswith("/img "):
        prompt = command[5:].strip()
        send_telegram(chat_id, "🎨 이미지 생성 요청 중...")
        result = vivace_action("generate_nano_banana", prompt)
        send_telegram(chat_id, result)
        return

    if command.startswith("/music "):
        prompt = command[7:].strip()
        send_telegram(chat_id, "🎵 음악 생성 요청 중...")
        result = vivace_action("generate_music", prompt)
        send_telegram(chat_id, result)
        return
        
    # 4. 자연어 처리 - Antigravity에게 바로 전달
    raw_result = consult_antigravity(command)
    clean_reply = extract_reply(raw_result)
    send_telegram(chat_id, clean_reply)

def main():
    print("👼 GOD MODE GATEWAY STARTED (Bypass All Restrictions)")
    print(f"🔑 Bot Token: {TELEGRAM_BOT_TOKEN[:5]}...")
    print(f"👤 Allowed User: {ALLOWED_CHAT_ID}")
    
    offset = 0
    
    while True:
        try:
            updates = requests.get(f"{TELEGRAM_API_URL}/getUpdates?offset={offset}&timeout=30", timeout=40).json()
            
            if "result" in updates:
                for update in updates["result"]:
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        chat_id = str(msg["chat"]["id"])
                        text = msg.get("text", "")
                        
                        # 보안 체크 (주인님만 허용)
                        if ALLOWED_CHAT_ID and chat_id != ALLOWED_CHAT_ID:
                            print(f"🚫 blocked access from {chat_id}")
                            continue
                            
                        print(f"📩 [{chat_id}] {text}")
                        process_command(chat_id, text)
                        
        except Exception as e:
            print(f"⚠️ Loop Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
