"""
1-6-2. RunnableWithMessageHistory - 세션 기반 격리
서로 다른 session_id는 완전히 독립된 대화로 관리됨을 확인
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from _common import get_llm

store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def main():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    chain_with_history = RunnableWithMessageHistory(
        prompt | get_llm(),
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    # 사용자 A 세션: 이름을 알려줌
    config_a = {"configurable": {"session_id": "user-A"}}
    chain_with_history.invoke({"question": "제 이름은 영희입니다."}, config=config_a)

    # 사용자 B 세션: 다른 session_id → A의 대화를 전혀 알 수 없어야 함
    config_b = {"configurable": {"session_id": "user-B"}}
    rb = chain_with_history.invoke({"question": "제 이름이 뭐죠?"}, config=config_b)
    print("[B 세션] AI:", rb.content)  # 이름을 모른다고 답해야 정상

    # 다시 A 세션: 자신의 히스토리에서 이름을 기억
    ra = chain_with_history.invoke({"question": "제 이름이 뭐죠?"}, config=config_a)
    print("[A 세션] AI:", ra.content)  # "영희"라고 답해야 정상


if __name__ == "__main__":
    main()
