"""5-1. 멀티 에이전트 개요: 두 전문가의 독립 분석과 결과 통합."""

from concurrent.futures import ThreadPoolExecutor

from langchain.agents import create_agent

from common import ask, get_model


def main() -> None:
    model = get_model()

    technical_agent = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "당신은 소프트웨어 기술 전문가입니다. 기술 난이도, "
            "개발 구조, 유지보수 관점에서 한국어로 분석하세요."
        ),
    )
    education_agent = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "당신은 비전공자 AI 교육 전문가입니다. 학습 난이도, "
            "실습 구성, 교육 효과 관점에서 한국어로 분석하세요."
        ),
    )

    topic = (
        input("분석할 주제(기본값: 음성 AI 비서 프로젝트): ").strip()
        or "음성 AI 비서 프로젝트"
    )

    # 서로 독립적인 두 작업을 동시에 실행합니다.
    with ThreadPoolExecutor(max_workers=2) as executor:
        tech_future = executor.submit(
            ask, technical_agent, f"'{topic}'를 기술 관점에서 분석해줘."
        )
        edu_future = executor.submit(
            ask, education_agent, f"'{topic}'를 교육 관점에서 분석해줘."
        )
        technical_result = tech_future.result()
        education_result = edu_future.result()

    synthesizer = create_agent(
        model=model,
        tools=[],
        system_prompt=(
            "당신은 두 전문가의 의견을 통합하는 책임자입니다. "
            "공통점, 차이점, 최종 권장안을 명확히 정리하세요."
        ),
    )
    combined = ask(
        synthesizer,
        f"""
주제: {topic}

[기술 전문가 분석]
{technical_result}

[교육 전문가 분석]
{education_result}

두 분석을 통합하여 실행 가능한 최종 권장안을 작성해줘.
""",
    )

    print("\n=== 기술 전문가 ===\n", technical_result)
    print("\n=== 교육 전문가 ===\n", education_result)
    print("\n=== 통합 결과 ===\n", combined)


if __name__ == "__main__":
    main()

