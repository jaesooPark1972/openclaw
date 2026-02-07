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
    'nova' 보이스는 한국어와 영어 모두 자연스럽게 처리하며, 학원(VIVACE)과 동일한 설정입니다.
    """
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY", "").strip().strip('"').strip("'")
    if not api_key or not api_key.startswith("sk-"):
        raise ValueError("Invalid OpenAI Key (sk-... required)")
        
    client = OpenAI(api_key=api_key)
    
    # OpenAI TTS는 별도의 language 파라미터가 없으며, 
    # 한국어 지원 보이스(nova, shimmer, alloy 등)를 선택하면 입력 텍스트의 언어를 자동 감지합니다.
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",  # 학원 스타일: 선명하고 중립적인 nova 보이스 권장
        input=text
    )
    # response.stream_to_file 는 구버전 방식이지만 현재 환경에서 호환됨
    response.stream_to_file(output_path)

async def generate_edge_tts(text, output_path):
    """Edge-TTS를 Fallback으로 사용 (매우 안정적/한글 전용)"""
    import edge_tts
    # 한글 전용 여성 음성 (SunHi)
    voice = "ko-KR-SunHiNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)

def main():
    if len(sys.argv) < 2:
        print("Usage: python tts_reply.py <text_to_speak>")
        sys.exit(1)
        
    # 인자로 받은 텍스트 (명령줄 인자는 OS 인코딩에 영향을 받을 수 있음)
    text = sys.argv[1]
    
    filename = "reply_voice.mp3"
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    # 덮어쓰기 위해 기존 파일 삭제
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except:
            pass

    success = False
    
    # 1. OpenAI TTS 시도 (학원 방식)
    try:
        generate_openai_tts(text, filepath)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            success = True
    except Exception as e:
        print(f"⚠️ [OpenAI TTS Fail] {e}", file=sys.stderr)

    # 2. 실패 시 Edge-TTS로 Fallback (한글 전용 음성 보장)
    if not success:
        try:
            asyncio.run(generate_edge_tts(text, filepath))
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                success = True
        except Exception as e:
            print(f"⚠️ [Edge-TTS Fail] {e}", file=sys.stderr)

    if success:
        # 파일 경로 출력 (caller인 antigravity_nexus.py에서 캡처함)
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
        print(filepath)
    else:
        print("❌ All TTS methods failed", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
