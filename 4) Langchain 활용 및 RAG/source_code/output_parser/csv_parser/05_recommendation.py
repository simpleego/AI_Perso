"""
1-5-1. CSV Parser - 실전 예제: 추천 목록 생성
조건에 맞는 추천 항목을 리스트로 생성 (temperature=0.7로 다양성 부여)
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", """사용자의 조건에 맞는 추천 목록을 제공합니다.
각 항목은 간결하게 작성하세요.
{format_instructions}"""),
        ("human", "조건: {condition}\n{count}가지를 추천해주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    # 추천 작업은 약간의 창의성이 필요하므로 temperature를 높임
    llm = get_llm(temperature=0.7)
    chain = prompt | llm | output_parser

    books = chain.invoke({
        "condition": "파이썬 초보자를 위한 프로그래밍 책",
        "count": "3",
    })
    movies = chain.invoke({
        "condition": "가족과 함께 볼 수 있는 애니메이션 영화",
        "count": "5",
    })

    print("추천 도서:", books)
    print("추천 영화:", movies)


if __name__ == "__main__":
    main()
