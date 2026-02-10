# 🦞 OpenClaw Model Organization Guide

## Overview

AI 모델들을 C: 드라이브에서 D: 드라이브로 이동하여 공간을 확보하고 체계적으로 정리합니다.

---

## 현재 상태 (C: 드라이브)

| 위치 | 크기 | 모델 |
|------|------|------|
| `C:\Users\JayPark1004\.cache\huggingface` | ~18GB | MusicGen, ACE-Step, Wan2.1 등 |
| `C:\AI-Models\` | ~5GB | Qwen3-8B-Coder (GGUF) |
| `F:\AGen\models\` | ~3GB | brain.gguf |

---

## 이동 후 구조 (D: 드라이브)

```
D:\Models\
├── huggingface\                    # HuggingFace 캐시
│   ├── hub\
│   │   ├── models--ACE-Step\        # ACE-Step 오디오 모델
│   │   ├── models--facebook\         # MusicGen, Hubert
│   │   ├── models--Wan-AI\          # Wan2.1 비디오
│   │   └── models--Supertone\       # Supertone TTS
│   └── modules\                     # Transformers 모듈
│
├── llm\                             # LLM 모델
│   ├── quantized\                   # GGUF 양자화 모델
│   │   ├── Qwen3-8B-Coder-Q4_K_M.gguf
│   │   └── brain.gguf
│   └── original\                    # 원본 모델 (필요시)
│
├── diffusion\                       # 이미지 생성 모델
│   ├── checkpoints\                 # SD, SDXL, Flux 등
│   ├── vae\                         # VAE 모델
│   └── loras\                       # LoRA adapters
│
├── audio\                          # 오디오 모델
│   ├── musicgen\
│   │   ├── musicgen-large\          # 3.4GB
│   │   └── musicgen-medium\         # 3.2GB
│   ├── rvc\                         # RVC 모델
│   └── tts\                         # TTS 모델
│
├── video\                          # 비디오 모델
│   └── wan2.1-t2v-1.3b\            # Wan2.1 T2V
│
└── embedding\                       # 임베딩 모델
    └── all-MiniLM-L6-v2\            # 91MB
```

---

## 이동 방법

### 1. 안전 모드 (권장)
```bash
D:\OpenClaw\workspace\god_gateway\move_models_to_d_drive.bat
```
- 원본을 삭제하지 않고 복사만 수행
- 문제가 생기면 원본으로 복구 가능

### 2. 실행 후 확인
```bash
tree D:\Models\ /F
```

---

## 설정 업데이트 (필요시)

### Ollama 모델 경로 변경
```bash
# 환경 변수 설정
set OLLAMA_MODELS=D:\Models\ollama\models

# 또는 config 수정
# C:\Users\%USERNAME%\.ollama\config.json
```

### ComfyUI 모델 경로
```
E:\ComfyUI-Easy-Install\ComfyUI\models\checkpoints
→ D:\Models\diffusion\checkpoints (심볼릭 링크 권장)
```

### AGen 모델 경로
```python
# AGen 설정 파일
F:\AGen\config\paths.yaml
```

---

## 심볼릭 링크 생성 (고급)

```bash
# ComfyUI 체크포인트 링크
mklink /J "E:\ComfyUI-Easy-Install\ComfyUI\models\checkpoints" "D:\Models\diffusion\checkpoints"

# AGen 모델 링크
mklink /J "F:\AGen\models" "D:\Models\llm"

# 음악 모델 링크
mklink /J "C:\Users\%USERNAME%\.cache\huggingface\hub\models--facebook--musicgen-large" "D:\Models\audio\musicgen\musicgen-large"
```

---

## 체크리스트

- [ ] `move_models_to_d_drive.bat` 실행
- [ ] `D:\Models\` 구조 확인
- [ ] Ollama 설정 확인 (필요시)
- [ ] ComfyUI 작동 확인
- [ ] AGen 작동 확인
- [ ] C: 드라이브 공간 확인

---

## 문제 해결

### 모델이 로드되지 않는 경우
```bash
# 경로 확인
echo %HUGGINGFACE_HUB_CACHE%
echo %OLLAMA_MODELS%

# 캐시 클리어 (필요시)
huggingface-cli cache purge
```

### Everything Search 재인덱스
```bash
# Everything → Tools → Rebuild Index
```

---

## 참고

- **절감 예상 공간**: 약 25-30GB
- **이동 시간**: 모델 크기에 따라 10-30분
- **원본 유지**: C: 드라이브 모델은 삭제하지 않음 (수동 삭제 권장)
