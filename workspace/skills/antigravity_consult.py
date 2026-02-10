# -*- coding: utf-8 -*-
"""
🔮 Antigravity Consult Skill
OpenClaw 에이전트가 Antigravity API를 직접 호출하는 스킬.
"꼬마가 안티한테 직접 일을 시키는" 구조를 위한 핵심 도구.
"""

import sys
import json
import requests
import os

# Master API Endpoint (nexus_api.py가 8082에서 실행 중)
NEXUS_API_BASE = "http://localhost:8082"

def consult_antigravity(instruction: str, context: dict = None) -> dict:
    """
    Antigravity AI에게 지시를 보내고 결과를 받아옴.
    OpenClaw의 꼬마 에이전트가 이 함수를 호출하면,
    Antigravity가 실제 작업을 수행하고 결과를 리턴함.
    """
    url = f"{NEXUS_API_BASE}/api/antigravity/consult"
    
    payload = {
        "instruction": instruction,
        "context": context or {}
    }
    
    try:
        print(f"🔮 [Antigravity Consult] Sending: {instruction[:50]}...")
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ [Antigravity] Response received.")
            return {
                "status": "success",
                "instruction": instruction,
                "reply": result.get("reply", "No reply"),
                "timestamp": result.get("timestamp")
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "message": response.text[:200]
            }
            
    except requests.exceptions.ConnectionError:
        return {
            "status": "error",
            "message": "Nexus API is Offline. Check if nexus_api.py is running on port 8082."
        }
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "message": "Request timed out. The task may be too complex."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def query_status() -> dict:
    """현재 Nexus API 상태 확인"""
    try:
        resp = requests.get(f"{NEXUS_API_BASE}/health", timeout=5)
        return {"status": "online", "response": resp.json()}
    except:
        return {"status": "offline", "message": "Nexus API unreachable"}


if __name__ == "__main__":
    # CLI Interface for OpenClaw Agent
    # Usage: python antigravity_consult.py "instruction text"
    # Usage: python antigravity_consult.py status
    
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python antigravity_consult.py <instruction> OR python antigravity_consult.py status"
        }))
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "status":
        result = query_status()
    else:
        # Treat all other args as instruction
        instruction = " ".join(sys.argv[1:])
        result = consult_antigravity(instruction)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
