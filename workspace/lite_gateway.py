# -*- coding: utf-8 -*-
"""
🚀 OpenClaw Lite Gateway (Bypass Solution)
OpenClaw Gateway의 복잡성을 우회하고, Telegram과 Vivace/Antigravity를 직접 연결하는 초경량 게이트웨이.
- 의존성: requests, subprocess (표준 라이브러리 위주)
- 모델: Groq (Llama-3.3-70b) - 빠르고 안정적
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
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # 보안을 위해 내 채팅 ID만 허용

if not TELEGRAM_BOT_TOKEN or not GROQ_API_KEY:
    print("❌ ERROR: Missing TELEGRAM_BOT_TOKEN or GROQ_API_KEY in .env")
    sys.exit(1)

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# LLM System Prompt
SYSTEM_PROMPT = """
You are 'Little OpenClaw', a highly capable AI assistant for Antigravity & Vivace system.
You have direct access to system tools.

CORE RULE:
1. If the user asks for music/video/image, you MUST output a JSON tool call.
2. If the user asks a question, Answer directly.
3. ALWAYS reply in KOREAN (한국어).

AVAILABLE TOOLS (Output JSON format):
- {"tool": "vivace_control", "action": "generate_music", "prompt": "..."}
- {"tool": "vivace_control", "action": "generate_nano_banana", "prompt": "..."}
- {"tool": "antigravity_consult", "instruction": "..."}
- {"tool": "nexus_api", "endpoint": "...", "payload": {...}}

EXAMPLE:
User: "고양이 그림 그려줘"
You: {"tool": "vivace_control", "action": "generate_nano_banana", "prompt": "cute cat"}

User: "안녕"
You: 안녕하세요! 무엇을 도와드릴까요?
"""

def send_telegram_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"⚠️ Telegram Send Error: {e}")

def call_groq_llm(user_message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.5,
        "max_tokens": 1024
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ Groq API Error: {response.text}"
    except Exception as e:
        return f"❌ LLM Connection Error: {e}"

def execute_tool(tool_json):
    try:
        cmd = json.loads(tool_json)
    except:
        return None # Not a JSON tool call
    
    tool_name = cmd.get("tool")
    
    print(f"⚙️ Executing Tool: {tool_name}")
    
    if tool_name == "vivace_control":
        action = cmd.get("action")
        # Ensure prompt is a string
        prompt_data = cmd.get("prompt", "")
        if isinstance(prompt_data, dict):
            prompt_data = json.dumps(prompt_data)
        
        # Call vivace_control.py
        try:
            # We pass action as arg1, and the rest as JSON string in arg2
            payload = json.dumps(cmd)
            result = subprocess.check_output(
                ["python", r"D:\OpenClaw\workspace\skills\vivace_control.py", action, payload],
                stderr=subprocess.STDOUT
            ).decode("utf-8")
            return f"✅ Vivace Execution:\n{result}"
        except subprocess.CalledProcessError as e:
            return f"❌ Tool Error:\n{e.output.decode('utf-8')}"

    elif tool_name == "antigravity_consult":
        instruction = cmd.get("instruction")
        try:
            result = subprocess.check_output(
                ["python", r"D:\OpenClaw\workspace\skills\antigravity_consult.py", instruction],
                stderr=subprocess.STDOUT
            ).decode("utf-8")
            # Parse result to just get the reply part if possible
            try:
                res_json = json.loads(result)
                if "reply" in res_json:
                    return f"🔮 Antigravity:\n{res_json['reply']}"
            except:
                pass
            return f"🔮 Antigravity Result:\n{result}"
        except subprocess.CalledProcessError as e:
            return f"❌ Consult Error:\n{e.output.decode('utf-8')}"
            
    return None

def main():
    print("🚀 OpenClaw Lite Gateway Started...")
    print(f"🤖 Bot: {TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"🧠 LLM: Groq (Llama-3.3)")
    
    offset = 0
    
    while True:
        try:
            # Polling
            response = requests.get(f"{TELEGRAM_API_URL}/getUpdates?offset={offset}&timeout=30", timeout=40)
            if response.status_code == 200:
                result = response.json()
                if result["ok"]:
                    for update in result["result"]:
                        offset = update["update_id"] + 1
                        
                        if "message" in update and "text" in update["message"]:
                            chat_id = str(update["message"]["chat"]["id"])
                            text = update["message"]["text"]
                            
                            # Security Check (Optional)
                            if ALLOWED_CHAT_ID and chat_id != ALLOWED_CHAT_ID:
                                print(f"⚠️ Unauthorized access attempt from {chat_id}")
                                continue
                                
                            print(f"📩 [{chat_id}] {text}")
                            
                            # 1. LLM Thinking
                            llm_reply = call_groq_llm(text)
                            print(f"🧠 LLM: {llm_reply[:50]}...")
                            
                            # 2. Tool Execution Check
                            tool_result = execute_tool(llm_reply)
                            
                            if tool_result:
                                # Send Tool Result
                                send_telegram_message(chat_id, tool_result)
                            else:
                                # Just Chat Response
                                send_telegram_message(chat_id, llm_reply)
                                
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🛑 Stopping Gateway...")
            break
        except Exception as e:
            print(f"⚠️ Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
