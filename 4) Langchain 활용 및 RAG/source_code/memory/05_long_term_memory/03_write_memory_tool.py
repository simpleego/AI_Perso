"""
1-6-5. 장기 메모리 - (3) 도구에서 메모리 쓰기
스레드가 바뀌어도(새로운 대화) 같은 사용자의 정보가 유지됨을 확인
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from _common import check_api_key, GEMINI_MODEL

USER_ID = "user-456"


@tool
def update_user_info(info_type: str, info_value: str, runtime: ToolRuntime) -> str:
    """사용자 정보를 업데이트합니다.

    Args:
        info_type: 정보 타입 (예: "email", "phone", "address")
        info_value: 저장할 값
    """
    store = runtime.store
    namespace = ("users", USER_ID)

    # 기존 프로필 조회 후 병합 (없으면 새로 생성)
    existing = store.get(namespace, "profile")
    profile = dict(existing.value) if existing else {}
    profile[info_type] = info_value

    store.put(namespace, "profile", profile)  # 장기 메모리에 영구 저장
    return f"{info_type} 정보가 업데이트되었습니다."


@tool
def get_user_info(runtime: ToolRuntime) -> str:
    """저장된 사용자 정보를 조회합니다."""
    memory = runtime.store.get(("users", USER_ID), "profile")
    return f"사용자 정보: {memory.value}" if memory else "저장된 정보가 없습니다."


def main():
    check_api_key()
    store = InMemoryStore()

    agent = create_agent(
        GEMINI_MODEL,
        tools=[update_user_info, get_user_info],
        checkpointer=MemorySaver(),
        store=store,
    )

    # [스레드 2] 정보 저장
    config = {"configurable": {"thread_id": "thread-2"}}
    r1 = agent.invoke(
        {"messages": [("user", "내 이메일을 hong@example.com으로 저장해줘")]}, config=config)
    print(r1["messages"][-1].content)

    # [스레드 3] "새로운 스레드"지만 장기 메모리는 사용자 기준으로 공유됨
    config2 = {"configurable": {"thread_id": "thread-3"}}
    r2 = agent.invoke(
        {"messages": [("user", "내 이메일 알려줘")]}, config=config2)
    print(r2["messages"][-1].content)  # hong@example.com 조회 성공해야 정상


if __name__ == "__main__":
    main()
