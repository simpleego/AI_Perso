"""5-5. Router: 질문 분류 후 필요한 전문 에이전트를 병렬 실행."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Literal

from langchain.agents import create_agent
from pydantic import BaseModel, Field

from common import ask, get_model


Domain = Literal["python", "database", "ai"]


class RouteDecision(BaseModel):
    """라우터가 반환할 구조화된 분류 결과."""

    domains: list[Domain] = Field(
        description="질문을 해결하는 데 필요한 하나 이상의 전문 영역"
    )
    reason: str = Field(description="해당 영역을 선택한 짧은 이유")


def main() -> None:
    model = get_model()
    router = model.with_structured_output(RouteDecision)

    agents = {
        "python": create_agent(
            model=model,
            tools=[],
            system_prompt="당신은 Python 개발 전문가입니다. 실행 가능한 예를 중시하세요.",
        ),
        "database": create_agent(
            model=model,
            tools=[],
            system_prompt="당신은 데이터베이스·SQL 전문가입니다. 데이터 모델과 SQL을 중시하세요.",
        ),
        "ai": create_agent(
            model=model,
            tools=[],
            system_prompt="당신은 생성형 AI·LangChain 전문가입니다. AI 구성과 한계를 설명하세요.",
        ),
    }

    question = (
        input(
            "질문(기본값: Python과 SQLite로 LangChain 대화 기록을 저장하는 방법): "
        ).strip()
        or "Python과 SQLite로 LangChain 대화 기록을 저장하는 방법을 알려줘."
    )

    decision = router.invoke(
        (
            "질문을 python, database, ai 중 필요한 영역으로 분류하세요. "
            "복합 질문은 여러 영역을 선택하세요.\n\n"
            f"질문: {question}"
        )
    )
    domains = list(dict.fromkeys(decision.domains))
    if not domains:
        domains = ["ai"]

    # 선택된 전문 에이전트만 동시에 실행합니다.
    with ThreadPoolExecutor(max_workers=len(domains)) as executor:
        futures = {
            domain: executor.submit(ask, agents[domain], question)
            for domain in domains
        }
        results = {
            domain: future.result()
            for domain, future in futures.items()
        }

    evidence = "\n\n".join(
        f"[{domain} 전문가]\n{text}" for domain, text in results.items()
    )
    synthesizer = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "당신은 여러 전문가 답변을 중복 없이 통합합니다. "
            "상충되는 의견은 숨기지 말고, 최종 실행 순서를 제시하세요."
        ),
    )
    final_answer = ask(
        synthesizer,
        f"원래 질문: {question}\n\n{evidence}",
    )

    print("\n=== 라우팅 결과 ===")
    print("선택 영역:", ", ".join(domains))
    print("선택 이유:", decision.reason)
    print("\n=== 최종 통합 답변 ===")
    print(final_answer)


if __name__ == "__main__":
    main()

