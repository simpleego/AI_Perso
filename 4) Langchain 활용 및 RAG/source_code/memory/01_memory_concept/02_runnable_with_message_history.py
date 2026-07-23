"""
1-6-1. 메모리의 필요성과 개념 - (2) RunnableWithMessageHistory (간단한 챗봇용)
세션별로 대화 기록을 저장해 두고, 매 호출마다 프롬프트에 자동 삽입한다.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from _common import get_llm

# 1. 세션별 메모리 저장소 (세션ID → 대화기록 객체)
store = {}


def get_session_history(session_id: str):
    """세션 ID마다 독립적인 대화 기록을 생성/반환"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def main():
    # 2. 모델 설정 (원본의 ChatAnthropic → 무료 Gemini로 교체)
    llm = get_llm(temperature=0)

    # 3. 프롬프트 템플릿: MessagesPlaceholder 위치에 이전 대화가 삽입됨
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다."),
        MessagesPlaceholder(variable_name="history"),  # ← 대화 기록 삽입 지점
        ("human", "{question}"),
    ])

    # 4. 기본 체인 생성
    chain = prompt | llm

    # 5. 메모리가 연결된 체인
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,            # 세션 기록을 가져오는 함수
        input_messages_key="question",  # 사용자 입력 키
        history_messages_key="history", # MessagesPlaceholder의 variable_name과 일치해야 함
    )

    # 6. 사용 예제: 같은 session_id로 호출하면 대화가 이어짐
    config = {"configurable": {"session_id": "user_123"}}

    response1 = chain_with_memory.invoke({"question": "안녕하세요"}, config=config)
    print("AI:", response1.content)
    print("-" * 50)

    response2 = chain_with_memory.invoke({"question": "내 이름은 김철수입니다."}, config=config)
    print("AI:", response2.content)
    print("-" * 50)

    # 이전 대화가 프롬프트에 포함되므로 이름을 기억함
    response3 = chain_with_memory.invoke({"question": "내 이름이 뭐였죠?"}, config=config)
    print("AI:", response3.content)


if __name__ == "__main__":
    main()
