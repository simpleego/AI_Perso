"""
1-5-2. JSON Parser - 실전 예제: 비교 분석 결과 구조화
두 기술의 비교 결과를 중첩 리스트 구조로 받아 처리
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class ComparisonItem(BaseModel):
    aspect: str = Field(description="비교 항목")
    option_a: str = Field(description="첫 번째 옵션 평가")
    option_b: str = Field(description="두 번째 옵션 평가")
    winner: str = Field(description="우위 옵션 (A/B/동등)")


class ComparisonResult(BaseModel):
    item_a: str = Field(description="비교 대상 A")
    item_b: str = Field(description="비교 대상 B")
    comparisons: list[ComparisonItem] = Field(description="세부 비교 항목들")
    conclusion: str = Field(description="종합 결론")
    recommended: str = Field(description="추천 옵션")


def main():
    output_parser = JsonOutputParser(pydantic_object=ComparisonResult)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """기술 비교 분석 전문가입니다.
두 가지 옵션을 객관적으로 비교 분석합니다.
{format_instructions}"""),
        ("human", "{option_a}와(과) {option_b}를 비교해주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    result = chain.invoke({"option_a": "React", "option_b": "Vue"})

    print(f"비교: {result['item_a']} vs {result['item_b']}")
    print("\n세부 비교:")
    for comp in result["comparisons"]:
        print(f"  - {comp['aspect']}: {comp['winner']} 우위")
    print(f"\n결론: {result['conclusion']}")
    print(f"추천: {result['recommended']}")


if __name__ == "__main__":
    main()
