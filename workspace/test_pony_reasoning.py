
import os
import requests
import json
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
env_path = r"D:\OpenClaw\.env"
load_dotenv(env_path)

def main():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        logger.error("❌ Error: OPENROUTER_API_KEY not found in .env")
        return

    logger.info("🦄 Testing OpenRouter Pony-Alpha with Reasoning...")
    
    # 1. First API call
    user_query = "How many r's are in the word 'strawberry'?"
    logger.info(f"User: {user_query}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional: Add HTTP referer/title for OpenRouter rankings
        "HTTP-Referer": "https://github.com/OpenClaw/OpenClaw", 
        "X-Title": "OpenClaw Antigravity",
    }
    
    payload1 = {
        "model": "openrouter/pony-alpha", # Or use "google/gemini-2.0-flash-thinking-exp:free" as widely available reasoning model if pony fails
        "messages": [
            {"role": "user", "content": user_query}
        ],
        "reasoning": {"enabled": True}
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload1),
            timeout=60
        )
        
        if response.status_code != 200:
            logger.error(f"❌ API Error: {response.text}")
            return

        resp_json = response.json()
        message = resp_json['choices'][0]['message']
        
        content = message.get('content', '')
        reasoning_details = message.get('reasoning_details')
        
        logger.info(f"\n🤖 Assistant: {content}")
        if reasoning_details:
             logger.info(f"\n🧠 Reasoning Details (tokens: {resp_json.get('usage', {}).get('completion_tokens_reasoning', 'N/A')}):\n{json.dumps(reasoning_details, indent=2)}")
        else:
             logger.info("\n(No explicit 'reasoning_details' field returned, checking usage stats...)")

        # 2. Second API call (Multi-turn with reasoning preservation)
        # Assuming the user wants to continue the conversation
        
        follow_up = "Are you sure? Think carefully."
        logger.info(f"\nUser: {follow_up}")

        messages = [
            {"role": "user", "content": user_query},
            {
                "role": "assistant",
                "content": content,
                # Key part: passing back reasoning_details
                "reasoning_details": reasoning_details 
            },
            {"role": "user", "content": follow_up}
        ]

        payload2 = {
            "model": "openrouter/pony-alpha",
            "messages": messages,
            "reasoning": {"enabled": True}
        }

        response2 = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload2),
            timeout=60
        )

        if response2.status_code != 200:
            logger.error(f"❌ API Error (Turn 2): {response2.text}")
            return

        resp_json2 = response2.json()
        message2 = resp_json2['choices'][0]['message']
        logger.info(f"\n🤖 Assistant (Turn 2): {message2.get('content')}")

    except Exception as e:
        logger.error(f"❌ Execution Error: {e}")

if __name__ == "__main__":
    main()
