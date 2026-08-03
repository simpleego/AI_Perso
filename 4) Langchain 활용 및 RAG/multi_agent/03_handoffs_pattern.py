"""실습 3: Handoffs - 상태에 따라 상담 담당 Agent를 순차 전환."""

from typing import Annotated, Literal

from langchain_core.messages import AnyMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.types import Command
from typing_extensions import TypedDict


class SupportState(TypedDict):
    """대화 턴을 넘어 유지되는 공유 상태."""

    messages: Annotated[list[AnyMessage], add_messages]
    active_agent: Literal["triage", "academic", "scholarship"]


model = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def triage_node(state: SupportState) -> Command:
    """초기 상담 Agent가 질문을 분류하고 전문 Agent로 handoff한다."""
    text = str(state["messages"][-1].content)
    if any(word in text for word in ["장학", "지원금", "등록금"]):
        target = "scholarship"
    else:
        target = "academic"
    print(f"[Handoff] triage → {target}")
    return Command(update={"active_agent": target}, goto=target)


def academic_node(state: SupportState) -> Command:
    """학사팀 Agent가 사용자에게 직접 답한다."""
    prompt = (
        "당신은 학사팀 상담원입니다. 일반휴학은 포털 신청과 지도교수 승인이 필요합니다. "
        f"사용자 질문: {state['messages'][-1].content}"
    )
    response = model.invoke(prompt)
    return Command(update={"messages": [response]}, goto=END)


def scholarship_node(state: SupportState) -> Command:
    """장학팀 Agent가 사용자에게 직접 답한다."""
    prompt = (
        "당신은 장학팀 상담원입니다. 성적우수 장학금은 직전 학기 12학점과 평점 3.5 이상이 필요합니다. "
        f"사용자 질문: {state['messages'][-1].content}"
    )
    response = model.invoke(prompt)
    return Command(update={"messages": [response]}, goto=END)


# StateGraph: 상태와 노드 전환을 명시하여 순차 제약을 표현한다.
builder = StateGraph(SupportState)
builder.add_node("triage", triage_node)
builder.add_node("academic", academic_node)
builder.add_node("scholarship", scholarship_node)
builder.add_edge(START, "triage")
graph = builder.compile()

result = graph.invoke(
    {
        "messages": [{"role": "user", "content": "성적우수 장학금 조건을 알려줘."}],
        "active_agent": "triage",
    }
)
print("최종 담당:", result["active_agent"])
print("최종 답변:", result["messages"][-1].content)

# 실습 과제:
# 1. 복합 질문이 들어오면 한 부서만 선택되는 한계를 관찰한다.
# 2. 정보 수집 → 본인 확인 → 전문 상담처럼 순차 상태를 추가한다.
