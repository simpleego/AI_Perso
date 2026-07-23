"""
1-5-1. CSV Parser - ChatPromptTemplate과 함께 사용
system/human 메시지 구조로 프롬프트 구성
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 유용한 정보를 제공하는 AI입니다. {format_instructions}"),
        ("human", "{category}에 관련된 {count}가지 항목을 나열해주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    # 다양한 요청
    programming_langs = chain.invoke({"category": "프로그래밍 언어", "count": "5"})
    frameworks = chain.invoke({"category": "파이썬 웹 프레임워크", "count": "3"})

    print("프로그래밍 언어:", programming_langs)
    print("웹 프레임워크:", frameworks)


if __name__ == "__main__":
    main()
