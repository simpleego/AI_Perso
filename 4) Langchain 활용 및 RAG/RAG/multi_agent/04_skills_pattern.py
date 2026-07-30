"""실습 4: Skills - 필요한 전문 지침만 온디맨드로 공개."""

from langchain.agents import create_agent
from langchain.tools import tool


# 실제 환경에서는 각 스킬을 별도 파일/DB에서 읽는다고 가정한다.
SKILLS = {
    "졸업판정": {
        "description": "졸업 학점과 필수 요건을 단계별로 판정",
        "instructions": (
            "졸업판정 절차: ① 총 130학점 이상인지 확인 ② 전공 60학점 이상인지 확인 "
            "③ 졸업논문 통과 여부 확인 ④ 부족한 항목을 표로 제시한다."
        ),
    },
    "장학상담": {
        "description": "성적우수 장학금 자격을 판정",
        "instructions": (
            "장학상담 절차: 직전 학기 12학점 이상이며 평점 3.5 이상인지 확인하고 "
            "두 조건을 각각 통과/미통과로 설명한다."
        ),
    },
}


@tool
def load_skill(skill_name: str) -> str:
    """전문 작업에 필요한 스킬 지침을 온디맨드로 로드한다.

    Args:
        skill_name: 졸업판정 또는 장학상담
    """
    skill = SKILLS.get(skill_name)
    if skill is None:
        return f"사용 가능한 스킬: {list(SKILLS)}"
    return skill["instructions"]


@tool
def calculate_missing(required: int, completed: int) -> int:
    """필요 학점에서 이수 학점을 빼 부족 학점을 계산한다."""
    return max(required - completed, 0)


# 초기 프롬프트에는 긴 스킬 본문을 넣지 않고 이름과 설명만 공개한다.
skill_catalog = "\n".join(
    f"- {name}: {value['description']}" for name, value in SKILLS.items()
)
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[load_skill, calculate_missing],
    system_prompt=(
        "당신은 대학 상담 Agent입니다. 전문 절차가 필요한 경우 먼저 load_skill로 지침을 "
        "로드하고 그 지침을 따르세요. 초기 스킬 카탈로그:\n" + skill_catalog
    ),
)

question = "총 124학점, 전공 62학점이고 졸업논문은 통과했어. 졸업 가능 여부를 판정해줘."
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("호출:", message.tool_calls)
    elif message.type == "tool":
        print(f"도구 결과({message.name}):", message.content)

print("\n최종 답변:", result["messages"][-1].content)

# 실습 과제:
# 1. 장학 질문으로 바꾸어 졸업판정 스킬이 로드되지 않는지 확인한다.
# 2. 모든 스킬 본문을 초기 프롬프트에 넣은 경우와 문자 수를 비교한다.
