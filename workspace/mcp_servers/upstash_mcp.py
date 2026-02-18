import os
import uuid
from typing import Dict, Optional, List
from mcp.server.fastmcp import FastMCP
from upstash_vector import Index

# 1. MCP 서버 정의
mcp = FastMCP("Upstash-Global-Memory")

# 2. 클라이언트 초기화 헬퍼
def get_index() -> Index:
    """
    환경 변수에서 URL과 Token을 로드하여 Upstash Index 클라이언트를 반환합니다.
    """
    url = os.getenv("UPSTASH_VECTOR_REST_URL")
    token = os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    
    if not url or not token:
        raise ValueError(
            "Upstash 자격 증명이 설정되지 않았습니다.\n"
            ".env 파일에 'UPSTASH_VECTOR_REST_URL'과 'UPSTASH_VECTOR_REST_TOKEN'을 설정해주세요."
        )
    
    # Rest Client 초기화
    return Index(url=url, token=token)

@mcp.tool()
def save_global_memory(content: str, metadata: Optional[Dict[str, str]] = None) -> str:
    """
    [WRITE] 중요한 기억을 Upstash Vector(클라우드)에 영구 저장합니다.
    자동으로 임베딩되어 저장되므로, 텍스트만 입력하면 됩니다.
    
    Args:
        content: 기억할 내용 (예: "사용자는 매운 음식을 싫어함")
        metadata: 추가 정보 (예: {"category": "preference", "timestamp": "2024-02-18"})
    """
    try:
        index = get_index()
        memory_id = str(uuid.uuid4())
        
        # 텍스트와 메타데이터 저장 (Upstash가 설정된 모델로 자동 임베딩 수행)
        # 주의: Index 생성 시 'Embedding Model'을 선택해야 작동합니다.
        index.upsert(
            vectors=[
                (memory_id, content, metadata if metadata else {})
            ]
        )
        return f"✅ 기억 저장 완료 (ID: {memory_id})"
    except Exception as e:
        return f"❌ 저장 실패: {str(e)}"

@mcp.tool()
def query_global_memory(query: str, top_k: int = 3) -> str:
    """
    [READ] 관련된 기억을 Upstash Vector(클라우드)에서 검색합니다.
    
    Args:
        query: 검색할 질문이나 키워드 (예: "식성 관련해서 내가 뭐라고 했지?")
        top_k: 가져올 기억의 개수 (기본값: 3)
    """
    try:
        index = get_index()
        
        # 텍스트로 검색 (Data와 Metadata 포함)
        results = index.query(
            data=query, 
            top_k=top_k, 
            include_metadata=True, 
            include_data=True
        )
        
        if not results:
            return "📭 관련된 기억을 찾을 수 없습니다."
            
        formatted = []
        for res in results:
            score = res.score if res.score else 0.0
            formatted.append(f"- [유사도: {score:.2f}] {res.data} (메타: {res.metadata})")
            
        return "\n".join(formatted)
    except Exception as e:
        return f"❌ 검색 실패: {str(e)}"

@mcp.tool()
def delete_global_memory(memory_id: str) -> str:
    """
    [DELETE] 특정 기억을 삭제합니다.
    기억 조회 시 반환된 ID를 사용하세요.
    """
    try:
        index = get_index()
        index.delete([memory_id])
        return f"🗑️ 기억 삭제 완료 (ID: {memory_id})"
    except Exception as e:
        return f"❌ 삭제 실패: {str(e)}"

if __name__ == "__main__":
    mcp.run()
