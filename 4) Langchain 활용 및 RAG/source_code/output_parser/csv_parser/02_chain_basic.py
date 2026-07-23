"""
1-5-1. CSV Parser - 체인과 통합 (기본 체인 구성)
PromptTemplate + Gemini + CSV Parser를 LCEL로 연결
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def main():
    # 파서 생성
    output_parser = CommaSeparatedListOutputParser()

    # 프롬프트 템플릿 (포맷 지시사항 포함)
    prompt = PromptTemplate(
        template="5가지 {subject}을(를) 나열하세요.\n{format_instructions}",
        input_variables=["subject"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    # 모델 초기화 (무료 API 키 사용 가능한 Gemini)
    llm = get_llm(temperature=0)

    # 체인 구성 (LCEL)
    chain = prompt | llm | output_parser

    # 실행
    result = chain.invoke({"subject": "인기 있는 한국 음식"})
    print("결과:", result)
    print("타입:", type(result))


if __name__ == "__main__":
    main()
