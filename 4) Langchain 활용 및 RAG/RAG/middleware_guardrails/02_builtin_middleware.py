"""실습 2: 내장 Middleware - 모델/도구 호출 제한과 자동 재시도."""

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    ToolRetryMiddleware,
)
from langchain.tools import tool


attempt_count = 0
DOCUMENTS = {
    "장학금": "성적우수 장학금은 직전 학기 12학점 이상, 평점평균 3.5 이상이 신청할 수 있다.",
    "신청기간": "장학금 신청 기간은 개강 30일 전부터 14일 전까지이다.",
}


@tool
def search_student_document(keyword: str) -> str:
    """학생지원 문서에서 핵심어를 검색한다."""
    global attempt_count
    attempt_count += 1

    # 일시적 네트워크 장애를 모의한다. ToolRetryMiddleware가 재시도한다.
    if attempt_count == 1:
        raise ConnectionError("실습용 일시적 검색 서버 오류")
    return DOCUMENTS.get(keyword, "관련 문서 없음")


# ModelCallLimitMiddleware: 무한 Agent 루프와 과도한 모델 비용을 방지한다.
model_limit = ModelCallLimitMiddleware(run_limit=5, exit_behavior="end")

# ToolCallLimitMiddleware: 지정 도구가 한 실행에서 과도하게 호출되는 것을 막는다.
tool_limit = ToolCallLimitMiddleware(
    tool_name="search_student_document",
    run_limit=3,
    exit_behavior="error",
)

# ToolRetryMiddleware: 일시적인 도구 실패를 설정 횟수만큼 자동 재시도한다.
tool_retry = ToolRetryMiddleware(
    max_retries=2,
    backoff_factor=1.0,
)

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_student_document],
    middleware=[model_limit, tool_limit, tool_retry],
    system_prompt=(
        "장학금 질문은 문서 검색 도구로 근거를 확인하세요. "
        "조건과 신청 기간이 모두 필요하면 각각 검색하세요."
    ),
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "성적우수 장학금 조건과 신청 기간을 알려줘."}]}
)

print("실제 도구 실행 시도 횟수:", attempt_count)
print("최종 답변:", result["messages"][-1].content)

# 실습 과제:
# 1. max_retries를 0으로 바꾸어 복원력 차이를 확인한다.
# 2. tool run_limit를 1로 낮춰 호출 제한이 동작하는 상황을 관찰한다.
