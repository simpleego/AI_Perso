"""
1-5-2. JSON Parser - with_structured_output과 비교
LangChain 1.0 권장 방식: 프롬프트에 포맷 지시사항을 넣지 않아도
모델의 구조화 출력 기능을 사용해 Pydantic 객체를 직접 반환
(Gemini도 with_structured_output을 지원합니다)
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class MovieInfo(BaseModel):
    """영화 정보"""
    title: str = Field(description="영화 제목")
    year: int = Field(description="개봉 연도")
    genre: str = Field(description="장르")


def json_output_parser_way():
    """방식 1: JsonOutputParser (모든 LLM에서 동작, dict 반환)"""
    output_parser = JsonOutputParser(pydantic_object=MovieInfo)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "{format_instructions}"),
        ("human", "{movie}에 대해 알려주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm()
    chain = prompt | llm | output_parser

    result = chain.invoke({"movie": "인셉션"})
    print("[JsonOutputParser 방식]")
    print(result)          # dict 반환
    print(type(result))    # <class 'dict'>


def with_structured_output_way():
    """방식 2: with_structured_output (권장, Pydantic 객체 반환)"""
    llm = get_llm()
    structured_llm = llm.with_structured_output(MovieInfo)

    result = structured_llm.invoke("인셉션에 대해 알려주세요.")
    print("\n[with_structured_output 방식 (권장)]")
    print(result)          # Pydantic 객체 반환
    print(type(result))    # <class 'MovieInfo'>

    # 속성으로 접근 가능
    print(f"제목: {result.title}")
    print(f"연도: {result.year}")
    print(f"장르: {result.genre}")


if __name__ == "__main__":
    json_output_parser_way()
    with_structured_output_way()
