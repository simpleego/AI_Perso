"""
1-6-4. 단기 메모리 패턴 - (5) 실전 예제: 고객 지원 챗봇
도구(tool) + 트리밍 + 요약 미들웨어를 조합한 종합 예제
[미들웨어 권장 순서] 삭제(민감 정보) → 요약(압축) → 트리밍(최종 크기 조정)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.agents.middleware import before_model, SummarizationMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from _common import check_api_key, GEMINI_MODEL


# 도구 정의: 에이전트가 필요할 때 스스로 호출
@tool
def get_order_status(order_id: str) -> str:
    """주문 상태를 조회합니다."""
    return f"주문 {order_id}는 배송 중입니다. (예상 도착: 2일 후)"


@before_model
def trim_context(state, runtime):
    """트리밍 미들웨어: 시스템 메시지 제외 최근 12개만 모델에 전달"""
    messages = state.get("messages", [])
    system_messages = [m for m in messages if m.type == "system"]
    others = [m for m in messages if m.type != "system"]
    return {"messages": system_messages + others[-12:]}


def main():
    check_api_key()

    # 요약 미들웨어: 대화가 길어지면 핵심 내용을 요약해 컨텍스트 압축
    summarization = SummarizationMiddleware(
        model=GEMINI_MODEL,
        max_tokens_before_summary=800,
        messages_to_keep=6,
    )

    agent = create_agent(
        GEMINI_MODEL,
        tools=[get_order_status],           # 주문 조회 도구 등록
        checkpointer=MemorySaver(),
        middleware=[summarization, trim_context],  # 요약 → 트리밍 순서
    )

    config = {"configurable": {"thread_id": "customer-001"}}

    # 1차 상호작용: 도구 호출 유도
    r1 = agent.invoke(
        {"messages": [("user", "안녕하세요, 주문 A123 상태 알려주세요.")]}, config=config)
    print("AI:", r1["messages"][-1].content, "\n" + "-" * 50)

    # 2차 상호작용: 이전 대화(주문 A123)를 기억한 상태에서 답변
    r2 = agent.invoke(
        {"messages": [("user", "배송은 언제쯤 완료되나요?")]}, config=config)
    print("AI:", r2["messages"][-1].content, "\n" + "-" * 50)

    # 긴 대화 후 메모리 패턴 동작 확인
    for i in range(1, 6):
        agent.invoke({"messages": [("user", f"추가 질문 {i}: 교환/환불 규정이 궁금해요.")]}, config=config)

    final = agent.invoke(
        {"messages": [("user", "지금까지 무슨 얘기했죠?")]}, config=config)
    print("AI:", final["messages"][-1].content)


if __name__ == "__main__":
    main()
