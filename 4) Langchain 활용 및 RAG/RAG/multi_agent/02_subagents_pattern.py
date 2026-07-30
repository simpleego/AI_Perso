"""실습 2: Subagents - 감독자가 전문 Agent들을 도구처럼 호출."""

from langchain.agents import create_agent
from langchain.tools import tool


ACADEMIC_DOCS = {
    "수강신청": "기본 신청 가능 학점은 18학점이며 평점 4.0 이상은 21학점까지 가능하다.",
}
SCHOLARSHIP_DOCS = {
    "성적우수": "성적우수 장학금은 등록금의 50%를 지원한다.",
}


@tool
def search_academic(keyword: str) -> str:
    """학사규정 문서에서 정보를 검색한다."""
    return ACADEMIC_DOCS.get(keyword, "관련 학사규정 없음")


@tool
def search_scholarship(keyword: str) -> str:
    """장학금 규정 문서에서 정보를 검색한다."""
    return SCHOLARSHIP_DOCS.get(keyword, "관련 장학규정 없음")


academic_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_academic],
    system_prompt="학사규정 전문 워커입니다. 검색 결과에 근거해 간결하게 보고하세요.",
)
scholarship_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_scholarship],
    system_prompt="장학금 전문 워커입니다. 검색 결과에 근거해 간결하게 보고하세요.",
)


# 서브에이전트를 @tool로 감싸 감독자의 도구 목록에 등록한다.
@tool
def ask_academic_agent(question: str) -> str:
    """수강신청, 휴학, 졸업 등 학사규정 전문가에게 질문한다."""
    result = academic_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return result["messages"][-1].content


@tool
def ask_scholarship_agent(question: str) -> str:
    """장학금 조건, 금액, 신청 방법 전문가에게 질문한다."""
    result = scholarship_agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return result["messages"][-1].content


# Supervisor는 직접 세부 문서를 검색하지 않고 적합한 전문 Agent를 선택·조정한다.
supervisor = create_agent(
    model="openai:gpt-4o-mini",
    tools=[ask_academic_agent, ask_scholarship_agent],
    system_prompt=(
        "당신은 대학 종합지원 감독자입니다. 질문을 도메인별로 나누고 필요한 전문 Agent를 "
        "모두 호출한 뒤 결과를 하나의 답변으로 통합하세요. 출처 Agent를 표시하세요."
    ),
)

question = "성적이 4.0이면 신청 가능한 최대 학점과 성적우수 장학금 지원액을 함께 알려줘."
result = supervisor.invoke(
    {"messages": [{"role": "user", "content": question}]}
)

print("[감독자 메시지 흐름]")
for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("서브에이전트 호출:", message.tool_calls)
    elif message.type == "tool":
        print(f"{message.name} 결과:", message.content)

print("\n[통합 답변]", result["messages"][-1].content)

# 실습 과제: 질문을 단일 도메인으로 바꾸고 Supervisor가 불필요한 Agent를 호출하는지 확인하라.
