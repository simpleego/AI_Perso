"""
1-5-1. CSV Parser - 결과 후처리 및 검증
파싱된 리스트를 조작/변환하고, 결과가 유효한지 검증하는 함수 예제
"""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from _common import get_llm


def validate_list_output(result: list, min_count: int = 1, max_count: int = 10) -> bool:
    """파싱 결과 검증"""
    if not isinstance(result, list):
        return False
    if len(result) < min_count or len(result) > max_count:
        return False
    if any(not item.strip() for item in result):
        return False
    return True


def main():
    output_parser = CommaSeparatedListOutputParser()

    prompt = PromptTemplate(
        template="5가지 {subject}을(를) 나열하세요.\n{format_instructions}",
        input_variables=["subject"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    keywords = chain.invoke({"subject": "머신러닝 핵심 개념"})

    # --- 리스트 활용 ---
    print(f"총 {len(keywords)}개 키워드")
    print(f"첫 번째: {keywords[0]}")
    print(f"정렬: {sorted(keywords)}")

    # 다른 데이터 구조로 변환
    keyword_set = set(keywords)                              # 중복 제거
    keyword_dict = {i: kw for i, kw in enumerate(keywords)}  # 인덱스 매핑
    print("집합:", keyword_set)
    print("딕셔너리:", keyword_dict)

    # --- 결과 검증 ---
    if validate_list_output(keywords, min_count=3, max_count=7):
        print("유효한 결과:", keywords)
    else:
        print("결과 검증 실패")


if __name__ == "__main__":
    main()
