"""
1-5-1. CSV Parser - 실전 예제: 키워드 추출
긴 텍스트에서 핵심 키워드를 리스트로 추출
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "텍스트에서 핵심 키워드를 추출합니다.\n{format_instructions}"),
        ("human", "다음 텍스트에서 핵심 키워드 5개를 추출하세요:\n\n{text}"),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    text = """
    LangChain은 대규모 언어 모델을 활용한 애플리케이션 개발을 위한 프레임워크입니다.
    프롬프트 관리, 체인 구성, 에이전트 생성 등 다양한 기능을 제공하며,
    RAG(검색 증강 생성) 시스템 구축에도 널리 사용됩니다.
    """

    keywords = chain.invoke({"text": text})
    print("추출된 키워드:", keywords)


if __name__ == "__main__":
    main()
