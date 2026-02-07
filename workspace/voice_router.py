class RoutedVoice:
    def __init__(self, mode, raw_text, cleaned_text, reason=None):
        self.mode = mode
        self.raw_text = raw_text
        self.cleaned_text = cleaned_text
        self.reason = reason

def route_voice_text(text):
    text = text.strip()
    
    # 1. 안전 필터 (Simple Safeguards)
    dangerous_keywords = ["전체 삭제", "포맷", "시스템 종료", "format c:"]
    for word in dangerous_keywords:
        if word in text:
            return RoutedVoice("rejected", text, text, f"Safety violation: {word}")

    # 2. 명령 감지 (Commands)
    # "비서야", "실행:", "Nexus" 등으로 시작하면 명령 모드
    command_triggers = ["비서야", "실행", "명령", "nexus", "넥서스", "antigravity"]
    
    lower_text = text.lower()
    for trigger in command_triggers:
        if lower_text.startswith(trigger):
            # 트리거 제거 후 cleaned_text 생성 (선택 사항)
            return RoutedVoice("command", text, text, f"Triggered by '{trigger}'")

    # 3. 기본 채팅 (Chat)
    return RoutedVoice("chat", text, text, None)
