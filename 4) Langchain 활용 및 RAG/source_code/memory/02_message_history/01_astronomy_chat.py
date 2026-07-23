"""
1-6-2. RunnableWithMessageHistory - 구현 단계별 분석 + 대화 흐름
천문학 전문가 챗봇: "그 행성" 같은 지시어를 이전 대화 맥락으로 이해하는지 확인
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from _common import get_llm

# ── 1. 기본 컴포넌트 설정 ─────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 천문학 전문가입니다. 사용자와 친근한 대화를 나누며 천문학 질문에 답변해주세요."),
    MessagesPlaceholder(variable_name="history"),  # 대화 히스토리가 삽입될 위치
    ("human", "{question}"),
])

# ── 2. 메모리 저장소 구성 ─────────────────────────────────────
store = {}  # session_id → InMemoryChatMessageHistory


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """세션마다 독립적인 대화 히스토리 유지 (프로세스 종료 시 소멸)"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def main():
    # ── 3. 메모리 기능을 가진 체인 생성 ──────────────────────
    llm = get_llm()  # gpt-4o-mini → 무료 Gemini로 교체
    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,                          # 기본 체인 (prompt | llm)
        get_session_history,            # 세션 히스토리를 가져오는 함수
        input_messages_key="question",  # 새 사용자 입력을 식별하는 키
        history_messages_key="history", # MessagesPlaceholder와 반드시 일치
    )

    # ── 4. 대화 실행과 메모리 작동 과정 ──────────────────────
    config = {"configurable": {"session_id": "astronomy_chat_1"}}

    # 첫 번째 호출: 히스토리가 비어있음 → 시스템 + 사용자 메시지만 전달
    r1 = chain_with_history.invoke(
        {"question": "안녕하세요, 저는 지구과학을 공부하는 학생입니다."}, config=config)
    print("AI:", r1.content, "\n" + "-" * 50)

    # 두 번째 호출: 이전 대화가 history 자리에 삽입되어 함께 전달
    r2 = chain_with_history.invoke(
        {"question": "태양계에서 가장 큰 행성은 무엇인가요?"}, config=config)
    print("AI:", r2.content, "\n" + "-" * 50)

    # 세 번째 호출: "그 행성" = 직전 답변의 목성임을 컨텍스트로 이해
    r3 = chain_with_history.invoke(
        {"question": "그 행성의 위성은 몇 개나 되나요?"}, config=config)
    print("AI:", r3.content, "\n" + "-" * 50)

    # 실제로 모델에 전달되는 메시지 구조 확인
    print("\n[저장된 히스토리 메시지 구조]")
    for msg in store["astronomy_chat_1"].messages:
        print(f"  {type(msg).__name__}: {msg.content[:40]}...")


if __name__ == "__main__":
    main()
