"""
1-6-4. 단기 메모리 패턴 - (3) 메시지 삭제 (Deletion)
RemoveMessage로 상태에서 "영구적으로" 메시지 제거 (트리밍과 달리 복구 불가)
실전: 민감 정보(비밀번호 등) 포함 메시지 삭제
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.agents.middleware import before_model
from langgraph.graph.message import RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from _common import check_api_key, GEMINI_MODEL

# 민감 정보 탐지 키워드
SENSITIVE_KEYWORDS = ["password", "비밀번호", "주민번호"]


@before_model
def remove_sensitive_info(state, runtime):
    """비밀번호/개인정보가 포함된 메시지를 상태에서 영구 삭제"""
    messages = state.get("messages", [])
    to_remove = []
    for msg in messages:
        content = msg.content if isinstance(msg.content, str) else str(msg.content)
        if any(keyword in content.lower() for keyword in SENSITIVE_KEYWORDS):
            # RemoveMessage(id=...)를 반환하면 해당 ID의 메시지가 삭제됨
            to_remove.append(RemoveMessage(id=msg.id))
    if to_remove:
        return {"messages": to_remove}
    return None  # 삭제할 것이 없으면 상태 변경 없음


def main():
    check_api_key()

    agent = create_agent(
        GEMINI_MODEL,
        tools=[],
        checkpointer=MemorySaver(),
        middleware=[remove_sensitive_info],
    )

    config = {"configurable": {"thread_id": "delete-demo"}}

    # 민감 정보가 포함된 메시지 전송 → 미들웨어가 삭제
    agent.invoke(
        {"messages": [("user", "제 비밀번호는 1234입니다. 기억해주세요.")]}, config=config)

    result = agent.invoke(
        {"messages": [("user", "아까 알려드린 비밀번호가 뭐였죠?")]}, config=config)
    print(result["messages"][-1].content)  # 삭제되어 기억하지 못해야 정상

    print("\n[현재 상태의 메시지들]")
    for m in result["messages"]:
        print(f"  {m.type}: {str(m.content)[:40]}")


if __name__ == "__main__":
    main()
