"""
1-6-3. 다양한 메모리 저장 방식 - (1) 인메모리 저장소 (개발용)
가장 단순한 방식. 프로세스(서버) 재시작 시 데이터 소멸.
"""
from langchain_core.chat_history import InMemoryChatMessageHistory
from _chain import build_chain_with_history, demo_conversation

# 세션별 메모리 저장 (파이썬 딕셔너리 = 프로세스 메모리)
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


if __name__ == "__main__":
    chain = build_chain_with_history(get_session_history)
    demo_conversation(chain, "user_123")
    # 스크립트를 다시 실행하면 기억이 사라짐 (인메모리의 한계)
