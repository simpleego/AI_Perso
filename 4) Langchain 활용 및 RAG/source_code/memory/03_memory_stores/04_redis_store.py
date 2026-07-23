"""
1-6-3. 다양한 메모리 저장 방식 - (4) Redis 저장소
분산 환경에서 빠른 읽기/쓰기가 필요할 때 사용. TTL로 자동 만료 가능.
[사전 준비] pip install redis + 로컬에서 Redis 서버 실행 (docker run -p 6379:6379 redis)
"""
from langchain_community.chat_message_histories import RedisChatMessageHistory
from _chain import build_chain_with_history, demo_conversation


def get_redis_session_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379",
        ttl=3600,  # 1시간 후 자동 삭제 (캐시성 대화에 유용)
    )


if __name__ == "__main__":
    try:
        chain = build_chain_with_history(get_redis_session_history)
        demo_conversation(chain, "user_123")
    except Exception as e:
        print("[안내] Redis 서버에 연결할 수 없습니다. Redis 실행 후 다시 시도하세요.")
        print("에러:", e)
