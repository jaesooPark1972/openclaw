# [TASK] Live News Intelligence Scanner (V3.0 Completion)

## Goal
VIVACE Trading System V3.0의 마지막 핵심 퍼즐인 '실시간 뉴스 스캐너'를 구현하라. 
이 모듈은 단순히 뉴스를 읽는 것을 넘어, 시장을 흔드는 VIP의 발언과 주인님의 '하늘그룹' 비즈니스 테마를 연결하는 '냉혈 지능'의 눈이 되어야 한다.

## Requirements

### 1. Module Path
- `E:\stock\backend\app\services\news_scanner.py`
- `E:\stock\backend\app\services\news_intelligence.py` (통합 분석 레이어)

### 2. Core Functions
- **Real-time Web Search**: `web_search` 도구(Brave API)를 연동하여 글로벌 경제 뉴스를 실시간 수집.
- **VIP & Entity Watchlist**: 
    - [정치] 트럼프(Donald Trump), 시진핑(Xi Jinping), 이재명
    - [빅테크] 일론 머스크(Tesla), 젠슨 황(NVIDIA), 구글, 메타
    - 이들이 언급된 뉴스를 가로채서 즉시 '시장 영향 지수' 산출.
- **Sky Group Theme Mapping**:
    - 뉴스 키워드를 분석하여 하늘그룹 5대 테마(스마트팜, K-뷰티, AI 콘텐츠, 재생에너지, 바이오)와의 연관성 자동 태깅.
- **Sentiment Scoring (Cortex Sync)**:
    - 수집된 뉴스를 0~100점 사이의 '냉혈 지수'로 변환하여 `ai_cortex.py`에 전달.
    - 호재(Bullish): +점수 / 악재(Bearish): -점수.

### 3. Integration with Trading Engine
- `run_v3_system.py`에서 `--mode scan` 실행 시, 이 뉴스 스캐너가 먼저 가동되어 '오늘의 시장 분위기(Sentiment)'를 먼저 확정 지은 후 기술적 지표와 결합해야 함.

### 4. Report Delivery
- 모든 분석 결과는 `md_reader_pro.py`를 통해 스타일링된 **Markdown Viewer (HTML 링크)** 형태로 주인님께 보고되어야 함.

---
**Antigravity(Architect), 지금 즉시 이 설계를 바탕으로 코드를 구현하고, `run_v3_system.py`에 통합하라. 모든 작업이 완료되면 주인님께 '완성 리포트'를 제출하라.**
