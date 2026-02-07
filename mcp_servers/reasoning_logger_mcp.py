import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("First-Principles-Logger")

LOG_FILE = "D:\\OpenClaw\\workspace\\reasoning_history.md"

@mcp.tool()
def log_reasoning_step(step_name: str, content: str) -> str:
    """
    제1원칙 사고의 각 단계를 문서로 기록합니다.
    Args:
        step_name: 단계 이름 (예: '문제 정의', '가정 분석', '본질 재설계')
        content: 기록할 내용
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    entry = f"\n## [{timestamp}] {step_name}\n\n{content}\n\n---\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)
    
    return f"Successfully logged {step_name} to reasoning_history.md"

if __name__ == "__main__":
    mcp.run()
