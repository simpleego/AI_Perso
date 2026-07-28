"""3-2. 내장 도구: 웹 검색과 위키백과 도구를 에이전트에 연결."""

from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from common import get_model, print_final_answer


def main() -> None:
    # 별도 검색 API 키가 필요 없는 커뮤니티 통합 도구입니다.
    web_search = DuckDuckGoSearchRun(
        name="web_search",
        description="최신 웹 정보를 검색할 때 사용합니다.",
    )
    wikipedia = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            lang="ko",
            top_k_results=2,
            doc_content_chars_max=2000,
        )
    )

    agent = create_agent(
        model=get_model(),
        tools=[web_search, wikipedia],
        system_prompt=(
            "당신은 조사 도우미입니다. 일반적인 배경지식은 위키백과를, "
            "최근 정보는 웹 검색을 사용하세요. 도구 결과에서 확인되지 않은 "
            "내용을 추측하지 말고, 사용한 자료의 제목이나 URL을 답변에 포함하세요."
        ),
    )

    question = input(
        "질문을 입력하세요\n"
        "(예: 랭체인이 무엇인지 설명하고 최근 버전의 특징도 알려줘): "
    ).strip()
    if not question:
        question = "랭체인이 무엇인지 설명하고 최근 버전의 특징도 알려줘."

    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    print_final_answer(result)


if __name__ == "__main__":
    main()

