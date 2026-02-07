
import json
import os
import subprocess
import sys
from voice_router import route_voice_text

def run_stt(audio_path: str) -> str:
    """stt_whisper.py를 호출해서 전사 텍스트를 받아온다."""
    # stt_whisper.py가 같은 폴더에 있다고 가정
    script_path = os.path.join(os.path.dirname(__file__), "stt_whisper.py")
    
    result = subprocess.run(
        [sys.executable, script_path, audio_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"stt_whisper.py error: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def main():
    # 텔레그램 등에서 파일 인자가 넘어옴
    if len(sys.argv) < 2:
        print("Usage: python voice_pipeline.py <audio_path>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"ERROR: Audio file not found at {audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # 1) STT 실행
        text = run_stt(audio_path)
        if not text:
            raise ValueError("Empty transcription received")

        # 2) 라우팅 (대화 vs 명령)
        routed = route_voice_text(text)

        # 3) 결과 JSON 출력 (OpenClaw가 파싱할 부분)
        out = {
            "mode": routed.mode,
            "raw_text": routed.raw_text,
            "cleaned_text": routed.cleaned_text,
            "reason": routed.reason,
            "source_file": audio_path
        }
        # 한글 깨짐 방지
        sys.stdout.reconfigure(encoding='utf-8')
        print(json.dumps(out, ensure_ascii=False, indent=2))

    except Exception as e:
        error_out = {
            "mode": "error",
            "error": str(e)
        }
        sys.stdout.reconfigure(encoding='utf-8')
        print(json.dumps(error_out, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()
