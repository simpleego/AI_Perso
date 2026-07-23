"""
1-6-4. 단기 메모리 패턴 - (2) 메시지 트리밍 (Trimming)
@before_model 미들웨어: 모델 호출 "직전"에만 메시지를 일시 제한 (상태는 유지)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langgraph.checkpoint.memory import MemorySaver
from _common import check_api_key, GEMINI_MODEL


@before_model  # 모델 호출 전에 실행되는 훅
def keep_last_n_messages(state, runtime):
    """메시지 개수 기반 트리밍: 시스템 메시지 + 최근 10개만 모델에 전달"""
    messages = state.get("messages", [])

    # 시스템 메시지는 항상 유지 (역할/지침 손실 방지)
    system_messages = [m for m in messages if m.type == "system"]
    other_messages = [m for m in messages if m.type != "system"]

    recent_messages = other_messages[-10:]  # 최근 10개만 유지
    return {"messages": system_messages + recent_messages}


def main():
    check_api_key()

    agent = create_agent(
        GEMINI_MODEL,
        tools=[],
        checkpointer=MemorySaver(),
        middleware=[keep_last_n_messages],  # 미들웨어로 트리밍 적용
    )

    config = {"configurable": {"thread_id": "trim-demo"}}

    # 긴 대화를 시뮬레이션 (트리밍이 없으면 토큰이 계속 누적됨)
    agent.invoke({"messages": [("user", "제 이름은 철수입니다.")]}, config=config)
    for i in range(1, 6):
        agent.invoke({"messages": [("user", f"잡담 {i}: 오늘 날씨 어때요?")]}, config=config)

    result = agent.invoke({"messages": [("user", "제 이름 기억나요?")]}, config=config)
    print(result["messages"][-1].content)
    # 트리밍 윈도우(10개) 안에 이름 메시지가 남아있으면 기억, 밀려났으면 잊음
    print(f"\n[상태에 저장된 전체 메시지 수] {len(result['messages'])}개 (상태 자체는 유지됨)")


if __name__ == "__main__":
    main()
