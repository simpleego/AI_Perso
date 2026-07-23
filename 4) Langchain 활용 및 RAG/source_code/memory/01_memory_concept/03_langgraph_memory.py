"""
1-6-1. 메모리의 필요성과 개념 - (3) LangGraph 기반 메모리 (LangChain 1.0 권장)
create_agent + checkpointer 조합으로 대화 상태를 자동 저장한다.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from _common import check_api_key, GEMINI_MODEL


def main():
    check_api_key()

    # 체크포인터: 스레드별 대화 상태를 자동으로 저장/복원
    checkpointer = InMemorySaver()

    agent_with_memory = create_agent(
        model=GEMINI_MODEL,        # "google_genai:gemini-2.5-flash" (무료 API 키)
        tools=[],
        checkpointer=checkpointer, # ← 이 한 줄로 단기 메모리 활성화
    )

    # thread_id로 대화(스레드)를 구분 - 같은 thread_id면 대화가 이어짐
    config = {"configurable": {"thread_id": "conversation_1"}}

    response1 = agent_with_memory.invoke(
        {"messages": [{"role": "user", "content": "안녕하세요"}]}, config=config)
    print("AI:", response1["messages"][-1].content)
    print("-" * 50)

    response2 = agent_with_memory.invoke(
        {"messages": [{"role": "user", "content": "내 이름은 김철수입니다."}]}, config=config)
    print("AI:", response2["messages"][-1].content)
    print("-" * 50)

    # 체크포인터에 저장된 이전 메시지들이 자동으로 컨텍스트에 포함됨
    response3 = agent_with_memory.invoke(
        {"messages": [{"role": "user", "content": "내 이름이 뭐였죠?"}]}, config=config)
    print("AI:", response3["messages"][-1].content)


if __name__ == "__main__":
    main()
