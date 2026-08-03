"""실습 1: Middleware 개요 - Agent 루프 전후의 Node-style 훅 관찰."""

import time

from langchain.agents import create_agent
from langchain.agents.middleware import before_agent, before_model, after_model, after_agent
from langchain.tools import tool


# 필요한 학사 문서는 이미 로드되었다고 가정한다.
DOCUMENTS = {
    "수강정정": "수강정정 기간은 개강일인 9월 1일부터 9월 7일까지이다.",
    "휴학": "일반휴학은 개강 전까지 포털에서 신청하고 지도교수 승인을 받아야 한다.",
}
events: list[str] = []
started_at = 0.0


@tool
def search_rule(keyword: str) -> str:
    """학사규정에서 키워드와 관련된 내용을 검색한다."""
    events.append("도구 실행")
    return DOCUMENTS.get(keyword, "관련 규정을 찾지 못했습니다.")


# before_agent/after_agent는 Agent 실행 전체에서 각각 한 번 실행된다.
@before_agent
def start_trace(request, state):
    global started_at
    started_at = time.perf_counter()
    events.append("1. before_agent")
    print("[before_agent] 실행 추적을 시작합니다.")
    return None


# before_model/after_model은 Agent 루프의 모델 호출마다 실행된다.
@before_model
def log_model_input(request, state):
    events.append("2. before_model")
    print("[before_model] 마지막 메시지:", state["messages"][-1].content)
    return None


@after_model
def log_model_output(request, state):
    events.append("3. after_model")
    message = state["messages"][-1]
    print("[after_model] 도구 호출 수:", len(getattr(message, "tool_calls", [])))
    return None


@after_agent
def finish_trace(request, state):
    events.append("4. after_agent")
    elapsed = time.perf_counter() - started_at
    print(f"[after_agent] 전체 실행 시간: {elapsed:.3f}초")
    return None


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_rule],
    middleware=[start_trace, log_model_input, log_model_output, finish_trace],
    system_prompt="학사규정 질문은 search_rule 도구로 확인한 뒤 답하세요.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "수강정정 기간을 알려줘."}]}
)

print("\n[최종 답변]", result["messages"][-1].content)
print("[관찰된 이벤트]", events)

# 실습 과제: 미들웨어 목록의 순서를 바꾸고 before/after 훅 출력 순서를 비교하라.
