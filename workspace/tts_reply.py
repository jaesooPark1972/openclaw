import os
import sys
import asyncio
from dotenv import load_dotenv

# 1. Load Environment Variables (D:/OpenClaw/.env)
env_path = r"D:\OpenClaw\.env"
load_dotenv(env_path)

def generate_openai_tts(text, output_path):
    """
    OpenAI TTS (tts-1)를 사용하여 음성 합성. 
    OGG/Opus 포맷으로 출력하여 텔레그램 보이스톡 호환성 확보.
    """
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip().strip('"').strip("'")
    if not api_key or not api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI Key (sk-... required)")
        
    client = OpenAI(api_key=api_key)
    
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
        response_format="opus" # 텔레그램 최적화: Opus 코덱 기반 OGG
    )
    # response.stream_to_file 는 바이너리 데이터를 직접 쓰므로 .ogg 확장자와 일치함
    response.stream_to_file(output_path)

async def generate_edge_tts(text, output_path):
    """Edge-TTS를 Fallback으로 사용 (OGG 코덱 설정)"""
    import edge_tts
    voice = "ko-KR-SunHiNeural"
    # 텔레그램 보이스 호환을 위해 opus 코덱 요청
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts_reply.py <text_to_speak>")
        sys.exit(1)
        
    text = sys.argv[1]
    
    # .ogg 확장자로 변경하여 텔레그램 sendVoice 호환성 극대화
    filename = "reply_voice.ogg"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    if os.path.exists(filepath):
        try: os.remove(filepath)
        except: pass

    success = False
    
    # 1. Edge-TTS 시도 (무료 우선)
    try:
        import asyncio
        asyncio.run(generate_edge_tts(text, filepath))
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            success = True
            print(f"✅ Edge-TTS Success: {filepath}", file=sys.stderr)
    except Exception as e:
        print(f"⚠️ [Edge-TTS Fail] {e}", file=sys.stderr)

    # 2. 실패 시 OpenAI TTS (유료 fallback)
    if not success:
        try:
            generate_openai_tts(text, filepath)
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                success = True
                print(f"✅ OpenAI TTS Success (Fallback): {filepath}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ [OpenAI TTS Fail] {e}", file=sys.stderr)

    if success:
        try: sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError: pass
        print(filepath)
    else:
        print("❌ All TTS methods failed", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
