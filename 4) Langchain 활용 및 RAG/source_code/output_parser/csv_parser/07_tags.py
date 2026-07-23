"""
1-5-1. CSV Parser - 실전 예제: 태그 생성
블로그 글에 어울리는 태그를 생성하고 해시태그 형식으로 포맷팅
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """글의 내용을 분석하여 관련 태그를 생성합니다.
태그는 소문자로, 공백 없이 작성하세요.
{format_instructions}"""),
        ("human", "다음 글에 적합한 태그 5개를 생성하세요:\n\n{content}"),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    content = """
    React와 TypeScript를 사용하여 현대적인 웹 애플리케이션을 구축하는 방법을 알아봅니다.
    컴포넌트 설계, 상태 관리, API 연동 등 핵심 개념을 다룹니다.
    """

    tags = chain.invoke({"content": content})
    print("생성된 태그:", tags)

    # 태그 포맷팅 (해시태그 형식)
    print("해시태그:", " ".join(f"#{tag}" for tag in tags))


if __name__ == "__main__":
    main()
