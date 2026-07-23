"""
1-6-5. 장기 메모리 - (2) 도구에서 메모리 읽기
에이전트의 도구(tool)가 runtime.store를 통해 장기 메모리를 조회
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from _common import check_api_key, GEMINI_MODEL

USER_ID = "user-123"  # 실습 단순화를 위해 상수로 사용 (실전은 runtime.context 활용)


@tool
def get_user_preferences(runtime: ToolRuntime) -> str:
    """사용자 선호도를 조회합니다."""
    store = runtime.store              # ← 도구 안에서 장기 메모리 Store 접근
    memory = store.get(("users", USER_ID), "preferences")  # 네임스페이스 + 키로 조회
    if memory:
        return f"사용자 선호도: {memory.value}"
    return "저장된 선호도가 없습니다."


def main():
    check_api_key()

    # Store에 미리 데이터 저장 (다른 세션/시스템에서 저장했다고 가정)
    store = InMemoryStore()
    store.put(("users", USER_ID), "preferences", {"language": "ko", "theme": "dark"})

    agent = create_agent(
        GEMINI_MODEL,
        tools=[get_user_preferences],
        checkpointer=MemorySaver(),  # 단기 메모리 (스레드 내 대화)
        store=store,                 # 장기 메모리 (세션 간 공유) ← 핵심
    )

    config = {"configurable": {"thread_id": "thread-1"}}
    result = agent.invoke(
        {"messages": [("user", "내 설정 알려줘")]}, config=config)
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
