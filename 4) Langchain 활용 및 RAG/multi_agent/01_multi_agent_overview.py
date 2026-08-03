"""실습 1: 멀티 에이전트 개요 - 전문화와 병렬 실행의 효과."""

import asyncio
import time

from langchain.agents import create_agent
from langchain.tools import tool


# 각 부서 문서는 이미 로드되었다고 가정한 모의 데이터다.
ACADEMIC_DOCS = {
    "휴학": "일반휴학은 포털에서 신청하고 지도교수 승인을 받아야 한다.",
}
SCHOLARSHIP_DOCS = {
    "성적우수": "직전 학기 12학점 이상, 평점평균 3.5 이상이면 신청할 수 있다.",
}


@tool
def search_academic_rule(keyword: str) -> str:
    """학사팀 규정에서 휴학·복학·수강 관련 내용을 검색한다."""
    return ACADEMIC_DOCS.get(keyword, "학사팀 문서에서 찾지 못했습니다.")


@tool
def search_scholarship_rule(keyword: str) -> str:
    """학생지원팀 규정에서 장학금 관련 내용을 검색한다."""
    return SCHOLARSHIP_DOCS.get(keyword, "장학금 문서에서 찾지 못했습니다.")


# 각 Agent는 자기 도메인의 도구와 짧은 컨텍스트만 가진다.
academic_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_academic_rule],
    system_prompt="당신은 학사팀 전문가입니다. 학사규정 도구로 확인한 정보만 답하세요.",
)
scholarship_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[search_scholarship_rule],
    system_prompt="당신은 학생지원팀 전문가입니다. 장학규정 도구로 확인한 정보만 답하세요.",
)


async def ask(agent, question: str) -> str:
    """ainvoke()로 전문 Agent를 비동기 실행하고 최종 답변만 반환한다."""
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return result["messages"][-1].content


async def main() -> None:
    started = time.perf_counter()

    # asyncio.gather(): 서로 독립적인 두 전문 Agent를 동시에 실행한다.
    academic_answer, scholarship_answer = await asyncio.gather(
        ask(academic_agent, "일반휴학 신청 절차는?"),
        ask(scholarship_agent, "성적우수 장학금 신청 조건은?"),
    )

    print("[학사 Agent]\n", academic_answer)
    print("\n[장학 Agent]\n", scholarship_answer)
    print(f"\n병렬 실행 시간: {time.perf_counter() - started:.2f}초")


asyncio.run(main())

# 실습 과제:
# 1. 두 Agent를 await로 순차 실행하여 걸린 시간을 비교한다.
# 2. 모든 도구를 한 Agent에 넣었을 때 도구 선택과 시스템 프롬프트 길이를 비교한다.
