import os
import sys
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# .env 로드 (OpenClaw 기준)
env_path = r"D:\OpenClaw\.env"
load_dotenv(env_path)

def main():
    # 1. 인자 파싱
    parser = argparse.ArgumentParser(description="Whisper STT Client (OpenAI-centered)")
    parser.add_argument("audio_path", help="Path to the audio file")
    args = parser.parse_args()
    
    audio_path = args.audio_path
    
    # 2. 파일 확인
    if not os.path.exists(audio_path):
        print(f"❌ Error: File not found: {audio_path}", file=sys.stderr)
        sys.exit(1)
        
    # 3. API 키 확인 (비용 절감 우선 - Groq 우선)
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        api_key = groq_key.strip()
        base_url = "https://api.groq.com/openai/v1"
        model = "whisper-large-v3"
        provider = "Groq"
    else:
        # Fallback to OpenAI (Paid)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            api_key = openai_key.strip()
            base_url = None
            model = "whisper-1"
            provider = "OpenAI"
        else:
            print("❌ Error: No API Key (GROQ or OPENAI) found in .env", file=sys.stderr)
            sys.exit(1)

    # 4. 클라이언트 초기화
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 5. Whisper API 호출
    try:
        with open(audio_path, "rb") as f:
            # transcription result is plain text due to response_format="text"
            transcription = client.audio.transcriptions.create(
                model=model,
                file=f,
                language="ko", # 한글 강제 인식
                response_format="text"
            )
        
        # 6. 결과 출력 (Windows 한글 깨짐 방지)
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass
            
        print(transcription.strip())

    except Exception as e:
        print(f"❌ STT Error ({provider}): {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
