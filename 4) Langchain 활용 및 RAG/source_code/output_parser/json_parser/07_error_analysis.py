"""
1-5-2. JSON Parser - 실전 예제: 오류 분석 결과
에러 메시지를 분석하여 원인/해결책을 구조화된 형태로 제공
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class ErrorAnalysis(BaseModel):
    error_type: str = Field(description="에러 유형")
    root_cause: str = Field(description="근본 원인")
    affected_area: str = Field(description="영향 받는 영역")
    solutions: list[str] = Field(description="해결 방법 목록")
    prevention: str = Field(description="예방 방법")


def main():
    output_parser = JsonOutputParser(pydantic_object=ErrorAnalysis)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """소프트웨어 디버깅 전문가입니다.
에러 메시지를 분석하여 원인과 해결책을 제시합니다.
{format_instructions}"""),
        ("human", "다음 에러를 분석해주세요:\n{error_message}"),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    error = """
    TypeError: Cannot read properties of undefined (reading 'map')
        at UserList (UserList.js:15)
        at renderWithHooks (react-dom.development.js:14985)
    """

    result = chain.invoke({"error_message": error})
    print(f"에러 유형: {result['error_type']}")
    print(f"원인: {result['root_cause']}")
    print("해결 방법:")
    for i, solution in enumerate(result["solutions"], 1):
        print(f"  {i}. {solution}")
    print(f"예방: {result['prevention']}")


if __name__ == "__main__":
    main()
