"""5-3. Handoffs: Command로 전문가 노드 간 제어권 전환."""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain.agents import create_agent
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command

from common import ask, get_model


class SupportState(TypedDict, total=False):
    request: str
    warranty_status: Literal["보증기간 내", "보증기간 만료"]
    issue_type: Literal["하드웨어", "소프트웨어"]
    history: list[str]
    final_answer: str


model = get_model()

warranty_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "당신은 보증 판정 담당자입니다. 사용자가 제공한 정보만 사용하세요. "
        "'구매 1년 이내'이면 보증기간 내, 그 외에는 보증기간 만료로 판정하고 "
        "판정값 하나만 출력하세요."
    ),
)
classifier_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "당신은 장애 분류 담당자입니다. 물리적 파손·전원·부품 문제는 "
        "하드웨어, 프로그램·설정·업데이트 문제는 소프트웨어로 판정하세요. "
        "판정값 하나만 출력하세요."
    ),
)
resolution_agent = create_agent(
    model=model,
    tools=[],
    system_prompt=(
        "당신은 해결 담당자입니다. 전달받은 보증 상태와 장애 유형에 맞춰 "
        "안전하고 구체적인 해결 절차를 한국어로 제시하세요."
    ),
)


def warranty_node(state: SupportState) -> Command:
    raw = ask(warranty_agent, state["request"])
    status: Literal["보증기간 내", "보증기간 만료"]
    status = "보증기간 내" if "내" in raw and "만료" not in raw else "보증기간 만료"
    history = [*state.get("history", []), f"보증 담당자 → {status}"]
    return Command(
        update={"warranty_status": status, "history": history},
        goto="classifier",
    )


def classifier_node(state: SupportState) -> Command:
    raw = ask(classifier_agent, state["request"])
    issue: Literal["하드웨어", "소프트웨어"]
    issue = "소프트웨어" if "소프트웨어" in raw else "하드웨어"
    history = [*state.get("history", []), f"분류 담당자 → {issue}"]
    return Command(
        update={"issue_type": issue, "history": history},
        goto="resolution",
    )


def resolution_node(state: SupportState) -> Command:
    answer = ask(
        resolution_agent,
        (
            f"고객 요청: {state['request']}\n"
            f"보증 상태: {state['warranty_status']}\n"
            f"장애 유형: {state['issue_type']}"
        ),
    )
    history = [*state.get("history", []), "해결 담당자 → 해결안 작성"]
    return Command(
        update={"final_answer": answer, "history": history},
        goto=END,
    )


def build_workflow():
    builder = StateGraph(SupportState)
    builder.add_node("warranty", warranty_node)
    builder.add_node("classifier", classifier_node)
    builder.add_node("resolution", resolution_node)
    builder.add_edge(START, "warranty")
    return builder.compile()


def main() -> None:
    workflow = build_workflow()
    request = (
        input(
            "문제 설명(기본값: 6개월 전 구매한 노트북 화면이 깨졌어요): "
        ).strip()
        or "6개월 전 구매한 노트북 화면이 깨졌어요."
    )
    result = workflow.invoke({"request": request, "history": []})

    print("\n=== 핸드오프 기록 ===")
    for item in result["history"]:
        print("-", item)
    print("\n=== 최종 해결안 ===")
    print(result["final_answer"])


if __name__ == "__main__":
    main()

