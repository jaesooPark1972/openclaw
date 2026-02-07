# 🦞 OpenClaw Vivace System v2.0 Manual

## 1. System Overview (시스템 개요)

OpenClaw Vivace는 단순한 AI 비서를 넘어, **실제 업무를 즉시 수행하는 "에이전트 시스템"**입니다.
현재 시스템은 **Groq (Llama 3.3 70B)** 모델을 메인 두뇌로 사용하여 초고속 응답을 자랑하며, **Antigravity Server**를 통해 외부 도구들을 직접 제어합니다.

---

## 2. Productivity Commands (생산성 업무)

"Antigravity"에게 시키면 모든 구글 워크스페이스 도구를 1초 만에 실행합니다.

| 작업 (Task) | 명령어 예시 (Command) | 결과 (Action) |
| :--- | :--- | :--- |
| **새 문서 작성** | "새 구글 문서 만들어줘", "워드 펴봐" | 빈 Google Doc 생성 링크 제공 |
| **엑셀/시트** | "엑셀 시트 켜줘", "스프레드시트 만들어" | 빈 Google Sheet 생성 링크 제공 |
| **PPT/발표** | "새 슬라이드 만들어", "PPT 준비해" | 빈 Google Slide 생성 링크 제공 |
| **메모/노트** | "메모장 켜줘", "Keep 열어봐" | Google Keep 실행 |
| **화이트보드** | "화이트보드 켜줘", "그림판 열어" | Excalidraw 실행 (협업 가능) |

---

## 3. Creative Commands (창작 및 디자인)

복잡한 디자인 툴을 헤맬 필요 없이, 원하는 것을 제게 말하세요.

| 작업 (Task) | 명령어 예시 (Command) | 결과 (Action) |
| :--- | :--- | :--- |
| **디자인 검색** | "Canva에서 'AI 스타트업' 로고 찾아줘" | Canva 템플릿 검색 결과로 직행 |
| **이미지 생성** | "'사이버펑크 서울 야경' 그림 그려줘" | 고화질 AI 이미지(Flux 모델) 즉시 생성 |
| **(추천)** | "유튜브 썸네일 디자인 찾아줘" | Canva 썸네일 템플릿 페이지로 이동 |

---

## 4. Intelligence & Search (정보 및 검색)

Brave Search API가 연동되어 실시간 인터넷 정보를 가져옵니다.

* **뉴스:** "오늘자 AI 관련 주요 뉴스 3개만 요약해줘."
* **검색:** "엔비디아 현재 주가 검색해줘."
* **학습:** "양자 컴퓨터 원리가 뭐야?"

---

## 5. Bio-Acoustic Analysis (생체 음향 분석)

OpenClaw만의 독자 기술입니다. 주파수 데이터가 생물학적으로 타당한지 검증합니다.

* **명령:** "주파수 850Hz가 인간이 낼 수 있는 소리야?"
* **결과:** "Valid Human Vocal Range" 또는 "Impossible" 판정.

---

## 6. System Status & Troubleshooting

* **현재 상태:** ✅ **Online** (Port: 18789)
* **연결 봇:** @park_vivace_bot (텔레그램)
* **Brain:** Groq Llama 3.3 70B (Fast & Smart)
* **에러 발생 시:**
  * 만약 응답이 없다면 바탕화면의 `Run_OpenClaw` 아이콘을 더블클릭하여 서버를 재시작하세요.
  * 429(Too Many Requests) 에러는 자동으로 Groq 모델로 우회하여 해결됩니다.

---
**Antigravity Chief Architect**
*Developed by Vivace Team*
