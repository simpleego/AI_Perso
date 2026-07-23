"""
1-6-2. RunnableWithMessageHistory - 프로덕션 고려사항: 토큰 제한 관리
대화가 길어질 때 trim_messages로 히스토리를 잘라 토큰 사용량을 억제
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import trim_messages, HumanMessage, AIMessage
from _common import get_llm

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def get_trimmed_history(session_id: str):
    """저장된 전체 히스토리에서 토큰 한도 내의 최근 메시지만 추출"""
    history = get_session_history(session_id)
    trimmed = trim_messages(
        history.messages,
        max_tokens=100,        # 유지할 최대 토큰 (실습용으로 작게 설정)
        strategy="last",       # 최근 메시지 우선
        token_counter=get_llm(),  # 모델 기반 정확한 토큰 계산
    )
    return trimmed


def main():
    # 긴 대화 히스토리를 인위적으로 채움
    history = get_session_history("long-chat")
    for i in range(1, 9):
        history.add_message(HumanMessage(content=f"{i}번째 질문"))
        history.add_message(AIMessage(content=f"{i}번째 답변"))

    print(f"전체 히스토리: {len(history.messages)}개 메시지")

    trimmed = get_trimmed_history("long-chat")
    print(f"트리밍 후: {len(trimmed)}개 메시지")
    for m in trimmed:
        print("  -", m.type, ":", m.content)


if __name__ == "__main__":
    main()
