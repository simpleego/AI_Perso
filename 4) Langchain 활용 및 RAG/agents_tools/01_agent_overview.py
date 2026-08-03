"""실습 1: Agent 개요 - create_agent와 ReAct 방식의 도구 선택 관찰."""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI


# 실제 데이터베이스에서 조회한 문서라고 가정한 학사 일정 데이터다.
ACADEMIC_SCHEDULE = {
    "수강신청": "2026년 8월 10일 09:00부터 8월 14일 18:00까지",
    "개강": "2026년 9월 1일",
    "수강정정": "2026년 9월 1일부터 9월 7일까지",
}


@tool
def search_academic_schedule(event: str) -> str:
    """학사 일정에서 행사 날짜를 조회한다.

    Args:
        event: 조회할 행사명. 예: 수강신청, 개강, 수강정정
    """
    # @tool은 함수 이름·docstring·타입 힌트로 도구 스키마를 자동 생성한다.
    return ACADEMIC_SCHEDULE.get(event, f"'{event}' 일정은 등록되어 있지 않습니다.")


@tool
def calculate_days(start_day: int, end_day: int) -> int:
    """두 날짜의 일(day) 번호를 받아 기간 차이를 계산한다.

    Args:
        start_day: 시작 날짜의 일
        end_day: 종료 날짜의 일
    """
    if end_day < start_day:
        raise ValueError("종료일은 시작일보다 빠를 수 없습니다.")
    return end_day - start_day


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# create_agent(): 모델, 도구 목록, 시스템 지시문을 결합해 Agent를 만든다.
agent = create_agent(
    model=model,
    tools=[search_academic_schedule, calculate_days],
    system_prompt=(
        "당신은 대학 학사도우미입니다. 일정 질문은 반드시 일정 조회 도구를 사용하세요. "
        "계산이 필요하면 계산 도구를 추가로 사용하고, 확인되지 않은 날짜를 만들지 마세요."
    ),
)

question = "수강정정은 언제이며 9월 1일부터 마지막 날까지 며칠 차이인가요?"

# invoke(): messages 상태를 입력하고 Agent의 도구 선택·실행·최종 답변 전체 상태를 받는다.
result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]}
)

print("[전체 메시지 흐름]")
for index, message in enumerate(result["messages"], start=1):
    tool_calls = getattr(message, "tool_calls", None)
    print(f"{index}. {message.type}: {message.content}")
    if tool_calls:
        print("   tool_calls:", tool_calls)

print("\n[최종 답변]")
print(result["messages"][-1].content)

# 실습 과제:
# 1. 도구 목록에서 calculate_days를 제거하고 답변 차이를 관찰한다.
# 2. "개강일은 언제야?"처럼 도구 하나만 필요한 질문과 메시지 수를 비교한다.
