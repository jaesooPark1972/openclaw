# -*- coding: utf-8 -*-
"""Update AGENTS.md to add antigravity_consult tool"""

import os

file_path = r"d:\OpenClaw\workspace\AGENTS.md"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the section to replace
start_marker = "## 🛠️ Available Tools"
end_marker = "## Forbidden Phrases"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("❌ Could not find section markers")
    exit(1)

new_section = """## 🛠️ Available Tools
| Tool | Path | Purpose |
|------|------|---------| 
| `vivace_control.py` | `D:\\OpenClaw\\workspace\\skills\\` | Music/Video/Image generation via VIVACE API |
| `antigravity_consult.py` | `D:\\OpenClaw\\workspace\\skills\\` | **Direct Antigravity AI consultation** |
| `nexus_api.py` | `D:\\OpenClaw\\workspace\\` | Core API orchestration |
| `voice_watcher.py` | `D:\\OpenClaw\\workspace\\` | Audio file monitoring & processing |
| `tts_reply.py` | `D:\\OpenClaw\\workspace\\` | Text-to-Speech generation |

## 🎯 도구 호출 규칙 (Tool Invocation Rules)

### ✅ 자동 실행 허용 (Auto-Execute)
다음 도구들은 **사용자 승인 없이 즉시 실행**하라:
- `antigravity_consult.py` → **안티에게 직접 지시**
- `vivace_control.py` → 음악/영상/이미지 생성
- `http_request` → 로컬 API 호출 (localhost:8080, 8081, 8082)
- `tts_reply.py` → 음성 합성
- `stt_whisper.py` → 음성 인식

### ⚠️ 승인 필요 (Ask First)
- 파일 삭제/이동, 외부 HTTP 요청, 셸 명령 실행

## 📝 Example Execution Flow (실행 예시)

### 예시 1: 이미지 요청
- User: "꼬마야, 귀여운 고양이 그림 nano-banana로 만들어서 텔레그램으로 보내."
→ 꼬마의 행동:
  1. `python skills/vivace_control.py generate_nano_banana '{"prompt": "cute cat"}'`
  2. `python skills/vivace_control.py send_latest '{"chat_id": "default"}'`
  3. 보고: "🐱 고양이 그림을 텔레그램으로 보냈습니다."

### 예시 2: 복잡한 질문 (Antigravity 호출)
- User: "꼬마야, 이 프로젝트의 아키텍처를 분석해줘."
→ 꼬마의 행동:
  1. `python skills/antigravity_consult.py "이 프로젝트의 아키텍처를 분석해줘"`
  2. Antigravity 응답 수신 → User에게 요약 보고

### 예시 3: 음악 생성
- User: "lo-fi 힙합 비트 하나 만들어줘"
→ 꼬마의 행동:
  1. `python skills/vivace_control.py generate_music '{"prompt": "lo-fi hip hop beat"}'`
  2. 보고: "🎵 lo-fi 비트 생성 완료!"

"""

new_content = content[:start_idx] + new_section + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ AGENTS.md updated successfully!")
print(f"   - Added: antigravity_consult.py tool")
print(f"   - Added: 도구 호출 규칙 section")
print(f"   - Added: 3 execution examples (Korean)")
