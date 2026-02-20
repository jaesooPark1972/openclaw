# Ollama + Local Memory Fallback Mode

메모리 검색(OpenAI embeddings) 장애 시 운영 모드.

## 실행
```bash
python local_memory_search.py "검색할 질의"
```

## 운영 원칙
1. 추론: Ollama(qwen 계열) 우선
2. 기억 검색: `local_memory_search.py` + LanceDB/로컬 로그 우선
3. OpenAI embeddings 복구 전까지 `memory_search` 실패는 비차단 처리

## 권장 모델
- 일반 질의: qwen3:latest
- 코딩: qwen2.5-coder:7b
- OCR 후처리: qwen3:latest
