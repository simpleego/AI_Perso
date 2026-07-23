"""
1-5-1. CSV Parser - 실전 예제: 선택지 생성
퀴즈/객관식 문제의 보기 목록 생성
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "주어진 질문에 대한 가능한 답변 선택지를 생성합니다.\n{format_instructions}"),
        ("human", "다음 질문에 대한 4가지 선택지를 만들어주세요:\n{question}"),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    question = "파이썬에서 리스트를 정렬하는 메서드는?"
    choices = chain.invoke({"question": question})

    # 선택지 포맷팅
    print(f"[문제] {question}")
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")


if __name__ == "__main__":
    main()
