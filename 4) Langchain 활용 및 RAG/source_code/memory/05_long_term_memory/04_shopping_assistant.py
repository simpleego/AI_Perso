"""
1-6-5. 장기 메모리 - (4) 실전 예제: 개인화된 쇼핑 도우미
구매 이력을 장기 메모리에 축적하고, 이력 기반으로 상품을 추천하는 에이전트
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from _common import check_api_key, GEMINI_MODEL

USER_ID = "user-789"


@tool
def save_purchase(product_name: str, category: str, runtime: ToolRuntime) -> str:
    """구매한 상품을 이력에 저장합니다."""
    store = runtime.store
    namespace = ("users", USER_ID)

    # 기존 이력 조회 (리스트 형태로 누적)
    existing = store.get(namespace, "purchase-history")
    history = list(existing.value) if existing else []

    history.append({
        "product": product_name,
        "category": category,
        "date": datetime.now().isoformat(),
    })

    # 최근 100개만 유지 (메모리 설계 원칙: 최소 필요 원칙)
    store.put(namespace, "purchase-history", history[-100:])
    return f"{product_name} 구매 이력이 저장되었습니다."


@tool
def get_recommendations(runtime: ToolRuntime) -> str:
    """사용자 이력 기반으로 상품을 추천합니다."""
    memory = runtime.store.get(("users", USER_ID), "purchase-history")
    if not memory:
        return "구매 이력이 없습니다."

    history = memory.value
    # 카테고리별 구매 빈도 계산 → 최다 구매 카테고리 추천
    categories = {}
    for item in history:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
    top_category = max(categories, key=categories.get)

    return (f"이전에 {top_category} 카테고리를 {categories[top_category]}번 구매하셨네요. "
            f"{top_category} 관련 신상품을 추천드립니다.")


def main():
    check_api_key()

    agent = create_agent(
        GEMINI_MODEL,
        tools=[save_purchase, get_recommendations],
        checkpointer=MemorySaver(),   # 단기: 스레드 내 대화 흐름
        store=InMemoryStore(),        # 장기: 구매 이력 (세션 간 유지)
    )

    config = {"configurable": {"thread_id": "shopping-1"}}

    # 대화 1: 구매 기록
    r = agent.invoke(
        {"messages": [("user", "노트북을 구매했어요, 카테고리는 전자제품입니다.")]}, config=config)
    print("AI:", r["messages"][-1].content, "\n" + "-" * 50)

    # 대화 2: 추가 구매
    r = agent.invoke(
        {"messages": [("user", "마우스도 구매했습니다, 전자제품 카테고리요.")]}, config=config)
    print("AI:", r["messages"][-1].content, "\n" + "-" * 50)

    # 대화 3: 이력 기반 추천 (전자제품 2회 → 전자제품 추천)
    r = agent.invoke(
        {"messages": [("user", "뭔가 추천해줄 거 있나요?")]}, config=config)
    print("AI:", r["messages"][-1].content)


if __name__ == "__main__":
    main()
