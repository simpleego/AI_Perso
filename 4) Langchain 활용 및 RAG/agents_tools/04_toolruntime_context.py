"""실습 4: ToolRuntime - LLM에 노출하지 않는 사용자 컨텍스트 활용."""

from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI


# 학생별 개인정보는 문서로 이미 로드되었다고 가정한 모의 데이터다.
STUDENT_RECORDS = {
    "S2026001": {
        "name": "김하늘",
        "department": "인공지능학과",
        "completed_credits": 112,
        "required_credits": 130,
        "scholarship": "성적우수 장학금 후보",
    },
    "S2026002": {
        "name": "이바다",
        "department": "컴퓨터공학과",
        "completed_credits": 126,
        "required_credits": 130,
        "scholarship": "해당 없음",
    },
}


@dataclass(frozen=True)
class StudentContext:
    """실행 시 애플리케이션이 제공하는 불변 컨텍스트."""

    student_id: str
    role: str
    session_id: str


@tool
def get_my_academic_status(
    field: str,
    runtime: ToolRuntime[StudentContext],
) -> str:
    """현재 로그인한 학생의 학사 정보를 조회한다.

    Args:
        field: 조회 항목. completed_credits, required_credits, scholarship 중 하나
    """
    # runtime 인자는 시스템이 자동 주입하며 LLM이 생성하는 도구 인자에는 노출되지 않는다.
    context = runtime.context
    if context.role != "student":
        return "학생 계정만 이 도구를 사용할 수 있습니다."

    allowed_fields = {"completed_credits", "required_credits", "scholarship"}
    if field not in allowed_fields:
        return f"조회할 수 없는 항목입니다. 허용 항목: {sorted(allowed_fields)}"

    record = STUDENT_RECORDS.get(context.student_id)
    if record is None:
        return "등록된 학생 정보를 찾을 수 없습니다."

    return (
        f"학생={record['name']}, 학과={record['department']}, "
        f"{field}={record[field]}, 세션={context.session_id}"
    )


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# context_schema를 지정하면 ToolRuntime의 context가 타입 안전하게 전달된다.
agent = create_agent(
    model=model,
    tools=[get_my_academic_status],
    context_schema=StudentContext,
    system_prompt=(
        "당신은 로그인 기반 학사도우미입니다. '내 정보' 질문은 도구로 조회하세요. "
        "사용자에게 학번이나 세션 ID를 다시 묻지 말고 런타임 컨텍스트를 사용하세요."
    ),
)

question = "내 졸업 필요 학점과 현재 이수 학점을 확인해서 몇 학점이 부족한지 알려줘."

# context는 메시지와 분리되어 전달되며 모델 프롬프트의 일반 사용자 입력이 아니다.
result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]},
    context=StudentContext(
        student_id="S2026001",
        role="student",
        session_id="SESSION-LAB-01",
    ),
)

print("[도구 입력 스키마]")
print(get_my_academic_status.args)
print("주의: 위 스키마에 runtime, student_id, session_id가 노출되지 않아야 합니다.")

print("\n[도구 호출과 결과]")
for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("도구 호출:", message.tool_calls)
    elif message.type == "tool":
        print("도구 결과:", message.content)

print("\n[최종 답변]")
print(result["messages"][-1].content)

# 실습 과제:
# 1. student_id를 S2026002로 바꾸고 같은 질문의 개인화 결과를 비교한다.
# 2. role을 guest로 바꾸어 권한 검사가 작동하는지 확인한다.
