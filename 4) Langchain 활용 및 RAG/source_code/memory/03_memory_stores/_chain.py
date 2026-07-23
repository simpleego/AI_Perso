"""3장 공통: 프롬프트 + Gemini 체인과 히스토리 연결 헬퍼"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from _common import get_llm


def build_chain_with_history(get_session_history):
    """저장소 함수(get_session_history)만 바꿔 끼우면 되는 공통 구조"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])
    chain = prompt | get_llm()
    return RunnableWithMessageHistory(
        chain,
        get_session_history,             # ← 저장소 백엔드만 교체하면 됨
        input_messages_key="question",
        history_messages_key="history",
    )


def demo_conversation(chain_with_history, session_id: str):
    """이름 기억 테스트용 공통 대화 시나리오"""
    config = {"configurable": {"session_id": session_id}}
    r1 = chain_with_history.invoke({"question": "제 이름은 민수입니다."}, config=config)
    print("AI:", r1.content)
    r2 = chain_with_history.invoke({"question": "제 이름이 뭐였죠?"}, config=config)
    print("AI:", r2.content)
