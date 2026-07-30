"""실습 5: Router - 질문을 분해해 여러 전문 노드로 병렬 팬아웃."""

import operator
from typing import Annotated

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

KNOWLEDGE = {
    "academic": "학사 문서: 평점 4.0 이상이면 최대 21학점까지 신청할 수 있다.",
    "scholarship": "장학 문서: 평점 3.5 이상이고 12학점 이상 이수하면 성적우수 장학금 대상이다.",
    "career": "진로 문서: AI 취업 프로그램은 3학년 이상이며 포트폴리오 제출이 필요하다.",
}


class Route(BaseModel):
    """라우터가 선택할 도메인과 하위 질문."""

    domain: str = Field(description="academic, scholarship, career 중 하나")
    query: str = Field(description="해당 도메인 Agent가 답할 하위 질문")


class RoutePlan(BaseModel):
    routes: list[Route]


class RouterState(TypedDict):
    question: str
    routes: list[dict]
    # 여러 병렬 노드 결과를 operator.add로 한 리스트에 합친다.
    answers: Annotated[list[str], operator.add]
    final_answer: str


class WorkerState(TypedDict):
    domain: str
    query: str


def plan_routes(state: RouterState) -> dict:
    """구조화 출력으로 필요한 전문 도메인과 하위 질문을 결정한다."""
    router_model = model.with_structured_output(RoutePlan)
    plan = router_model.invoke(
        "질문을 academic, scholarship, career 도메인으로 분해하세요. "
        "관련된 도메인만 선택하세요.\n질문: " + state["question"]
    )
    return {"routes": [route.model_dump() for route in plan.routes]}


def fan_out(state: RouterState) -> list[Send]:
    """Send(): route 수만큼 worker 노드를 동적으로 병렬 실행한다."""
    return [Send("worker", route) for route in state["routes"]]


def worker(state: WorkerState) -> dict:
    """각 전문 Agent는 자신의 도메인 문서만 받아 독립적으로 답한다."""
    domain = state["domain"]
    prompt = (
        f"당신은 {domain} 전문 상담원입니다.\n"
        f"참고 문서: {KNOWLEDGE[domain]}\n질문: {state['query']}"
    )
    answer = model.invoke(prompt).content
    return {"answers": [f"[{domain}] {answer}"]}


def synthesize(state: RouterState) -> dict:
    """병렬 결과를 중복 없이 하나의 사용자 답변으로 합성한다."""
    joined = "\n\n".join(state["answers"])
    answer = model.invoke(
        "아래 전문 Agent 결과를 근거로 통합 답변을 작성하세요. 도메인 표시는 유지하세요.\n" + joined
    )
    return {"final_answer": answer.content}


builder = StateGraph(RouterState)
builder.add_node("plan_routes", plan_routes)
builder.add_node("worker", worker)
builder.add_node("synthesize", synthesize)
builder.add_edge(START, "plan_routes")
builder.add_conditional_edges("plan_routes", fan_out, ["worker"])
builder.add_edge("worker", "synthesize")
builder.add_edge("synthesize", END)
graph = builder.compile()

result = graph.invoke(
    {
        "question": "평점 4.0 학생의 최대 신청 학점과 성적우수 장학금 가능 여부를 알려줘.",
        "routes": [],
        "answers": [],
        "final_answer": "",
    }
)
print("라우팅 계획:", result["routes"])
print("전문 Agent 결과:", result["answers"])
print("\n통합 답변:", result["final_answer"])

# 실습 과제:
# 1. 진로 질문을 추가하고 실제로 관련된 도메인만 선택되는지 확인한다.
# 2. 순차 실행 버전을 만들고 병렬 Router의 실행 시간과 비교한다.
