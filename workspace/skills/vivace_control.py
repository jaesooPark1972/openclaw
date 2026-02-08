import sys
import json
import requests
import os

# Vivace Nexus API Base URL
# Ensure nexus_api.py is running on port 8080
API_BASE = "http://localhost:8080/vivace"

def send_to_vivace(action, data=None):
    """
    Unified function to interact with Vivace Nexus API.
    Used by OpenClaw agents to control Music/Video/Code generation.
    """
    if data is None: data = {}
    
    try:
        # 1. Music Generation
        if action == "generate_music":
            url = f"{API_BASE}/generate"
            print(f"🚀 [Vivace Control] Requesting Music Generation: {data.get('title', 'Untitled')}")
            resp = requests.post(url, json=data, timeout=10)
            return json.dumps({"status": resp.status_code, "response": resp.json()})

        # 2. Send Latest File to Telegram
        elif action == "send_latest":
            url = f"{API_BASE}/telegram/send_latest"
            print(f"🚀 [Vivace Control] Requesting File Dispatch to Telegram: {data.get('chat_id', 'Default')}")
            resp = requests.post(url, json=data, timeout=30)
            try:
                return json.dumps(resp.json())
            except json.JSONDecodeError:
                return json.dumps({"status": "error", "code": resp.status_code, "message": "Invalid JSON from server", "raw": resp.text[:200]})

        # 4. Render Simple Video
        elif action == "render_video":
            url = f"{API_BASE}/video/render_simple"
            print(f"🎬 [Vivace Control] Requesting Video Rendering...")
            # Video rendering takes time, so set a long timeout (e.g., 5 mins)
            try:
                resp = requests.post(url, json=data, timeout=300)
                return json.dumps(resp.json())
            except requests.exceptions.Timeout:
                return json.dumps({"status": "error", "message": "Rendering Time-out (Check server logs)"})
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})

        # 5. Generate Image (Universal)
        elif action == "generate_image" or action == "generate_nano_banana":
            url = f"{API_BASE}/image/generate"
            
            # Action-based Engine Selection
            if action == "generate_nano_banana":
                data['engine'] = 'nano-banana'
                prompt = data.get('prompt', '')
                # Flavor text for Nano-Banana style
                if "style" not in prompt.lower():
                     data['prompt'] = prompt + ", masterpiece, best quality, anime style, vibrant colors"
            else:
                data['engine'] = 'dall-e-3' # Default to robust DALL-E if unspecified

            print(f"🎨 [Vivace Control] Requesting Image via {data.get('engine')}: {data.get('prompt', '')[:30]}...")
            try:
                resp = requests.post(url, json=data, timeout=60)
                return json.dumps(resp.json())
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})

        # 3. Agent Team Deployment
        elif action == "deploy_team":
            url = f"{API_BASE}/agent/deploy"
            print(f"🚀 [Vivace Control] Deploying Agent Team for: {data.get('task')}")
            resp = requests.post(url, json=data, timeout=5)
            return json.dumps(resp.json())

        else:
            return json.dumps({"status": "error", "message": f"Unknown action: {action}"})

    except requests.exceptions.ConnectionError:
        return json.dumps({"status": "error", "message": "Vivace Nexus API is Offline (Check Port 8080)"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    # OpenClaw Agent Interface
    # Usage: python vivace_control.py [action] [arg]
    
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python vivace_control.py [action] [json_data_or_simple_arg]"}))
        sys.exit(1)

    action_arg = sys.argv[1]
    payload_arg = {}
    
    if len(sys.argv) > 2:
        raw_arg = sys.argv[2]
        # Try to parse as JSON first
        try:
            parsed = json.loads(raw_arg)
            if isinstance(parsed, dict):
                payload_arg = parsed
            else:
                raise ValueError("Not a dictionary")
        except:
            # If not JSON dict, treat as simple argument based on action
            if action_arg == "send_latest":
                # Treat raw arg as chat_id (string)
                payload_arg = {"chat_id": str(raw_arg).strip()}
            elif action_arg == "generate_music":
                payload_arg = {"prompt": str(raw_arg), "title": "Quick Gen"}
            else:
                payload_arg = {"data": str(raw_arg)}

    # Execute and print result for OpenClaw to capture
    result = send_to_vivace(action_arg, payload_arg)
    print(result)
