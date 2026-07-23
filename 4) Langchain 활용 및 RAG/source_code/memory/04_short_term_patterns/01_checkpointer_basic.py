"""
1-6-4. 단기 메모리 패턴 - (1) 단기 메모리 활성화 (checkpointer)
create_agent에 checkpointer만 전달하면 스레드별 대화 상태가 자동 저장됨
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from _common import check_api_key, GEMINI_MODEL


def main():
    check_api_key()

    # Checkpointer 생성 (메모리 기반) - 프로덕션에서는 PostgresSaver 등 사용
    checkpointer = MemorySaver()

    agent = create_agent(
        GEMINI_MODEL,              # 무료 Gemini 모델
        tools=[],
        checkpointer=checkpointer, # ← 메모리 활성화 핵심
    )

    # thread_id: 대화 세션을 구분하는 고유 식별자
    config = {"configurable": {"thread_id": "conversation-1"}}

    result1 = agent.invoke(
        {"messages": [("user", "안녕하세요, 제 이름은 철수입니다.")]}, config=config)
    print(result1["messages"][-1].content)

    # 같은 thread_id → 이전 대화를 이어서 사용
    result2 = agent.invoke(
        {"messages": [("user", "제 이름이 뭐죠?")]}, config=config)
    print(result2["messages"][-1].content)  # "철수" 기억


if __name__ == "__main__":
    main()
