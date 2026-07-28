"""5-2. Subagents: 감독자가 전문 에이전트를 도구처럼 호출."""

from langchain.agents import create_agent
from langchain.tools import tool

from common import ask, get_model


model = get_model()

schedule_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "당신은 일정 관리 전문가입니다. 제공된 일정만 사용하여 "
        "충돌, 준비사항, 빈 시간을 간결하게 분석하세요."
    ),
)

email_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "당신은 이메일 업무 전문가입니다. 제공된 이메일 정보만 사용하여 "
        "긴급도, 답장 필요 여부, 후속 작업을 정리하세요."
    ),
)


@tool
def analyze_schedule(request: str) -> str:
    """일정, 회의, 시간 충돌과 관련된 요청을 일정 전문 에이전트에게 맡깁니다."""
    return ask(schedule_agent, request)


@tool
def analyze_email(request: str) -> str:
    """이메일, 답장, 메일 우선순위 요청을 이메일 전문 에이전트에게 맡깁니다."""
    return ask(email_agent, request)


def main() -> None:
    supervisor = create_agent(
        model=model,
        tools=[analyze_schedule, analyze_email],
        system_prompt=(
            "당신은 수행비서 감독자입니다. 일정 문제는 analyze_schedule, "
            "이메일 문제는 analyze_email에 위임하세요. 요청에 두 영역이 "
            "모두 있으면 두 도구를 모두 사용하고 결과를 하나의 브리핑으로 "
            "통합하세요. 제공되지 않은 사실은 만들지 마세요."
        ),
    )

    request = """
다음 정보를 바탕으로 오늘 업무 브리핑을 작성해줘.

[일정]
- 09:00 팀 회의
- 09:30 고객 미팅
- 14:00 프로젝트 발표

[이메일]
- 고객: 계약서 수정본을 오늘 12시까지 요청
- 팀장: 발표자료 최종 검토 요청
"""
    print("\n=== 감독자 최종 브리핑 ===")
    print(ask(supervisor, request))


if __name__ == "__main__":
    main()

