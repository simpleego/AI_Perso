"""실습 3: 커스텀 도구 - 문서 검색과 성적 계산 도구를 직접 설계."""

from typing import Literal

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# 필요한 문서는 이미 로드되었다고 가정한다.
DOCUMENTS = [
    {
        "id": "C1",
        "category": "성적",
        "content": "RAG 실습 평가는 프로젝트 50%, 실습 보고서 30%, 출석 20%로 구성한다.",
    },
    {
        "id": "C2",
        "category": "출석",
        "content": "지각 3회는 결석 1회로 처리하며 전체 수업의 25% 이상 결석하면 F이다.",
    },
    {
        "id": "C3",
        "category": "제출",
        "content": "프로젝트는 6월 14일 23시 59분까지 보고서와 저장소 URL을 제출한다.",
    },
]


class SearchInput(BaseModel):
    """도구 입력을 제한하여 Agent가 올바른 범주만 선택하게 한다."""

    category: Literal["성적", "출석", "제출"] = Field(
        description="검색할 학사 문서 범주"
    )
    keyword: str = Field(description="문서에서 찾을 핵심어")


@tool("search_course_documents", args_schema=SearchInput)
def search_course_documents(category: str, keyword: str) -> str:
    """강의 문서에서 범주와 핵심어에 관련된 규정을 검색한다."""
    # 실제 서비스라면 이 부분을 벡터 검색이나 데이터베이스 조회로 교체한다.
    candidates = [doc for doc in DOCUMENTS if doc["category"] == category]
    exact = [doc for doc in candidates if keyword.lower() in doc["content"].lower()]
    selected = exact or candidates
    if not selected:
        return "관련 문서를 찾지 못했습니다."
    return "\n".join(f"[{doc['id']}] {doc['content']}" for doc in selected)


@tool
def calculate_weighted_score(
    project: float, report: float, attendance: float
) -> float:
    """프로젝트·보고서·출석의 100점 만점 점수로 최종 가중 점수를 계산한다.

    Args:
        project: 프로젝트 점수
        report: 실습 보고서 점수
        attendance: 출석 점수
    """
    scores = (project, report, attendance)
    if any(score < 0 or score > 100 for score in scores):
        raise ValueError("각 점수는 0부터 100 사이여야 합니다.")
    return round(project * 0.5 + report * 0.3 + attendance * 0.2, 2)


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
agent = create_agent(
    model=model,
    tools=[search_course_documents, calculate_weighted_score],
    system_prompt=(
        "당신은 강의 운영 도우미입니다. 규정은 문서 검색 도구로 확인한 뒤 답하세요. "
        "최종 점수는 반드시 계산 도구를 사용하세요. 사용한 문서 ID를 답변에 표시하세요."
    ),
)

question = (
    "평가 비율을 문서에서 확인하고, 프로젝트 88점, 보고서 92점, "
    "출석 100점인 학생의 최종 점수를 계산해줘."
)
result = agent.invoke({"messages": [{"role": "user", "content": question}]})

for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("도구 호출:", message.tool_calls)
    elif message.type == "tool":
        print(f"도구 결과({message.name}):", message.content)

print("\n[최종 답변]")
print(result["messages"][-1].content)

# 실습 과제:
# 1. 110점처럼 잘못된 입력을 주어 입력 검증과 Agent의 오류 대응을 관찰한다.
# 2. DOCUMENTS에 재시험 규정을 추가하고 검색 범주 스키마도 함께 수정한다.
