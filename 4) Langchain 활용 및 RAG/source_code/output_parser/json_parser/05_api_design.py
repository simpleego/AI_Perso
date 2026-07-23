"""
1-5-2. JSON Parser - 실전 예제: API 응답 구조화
요청 기능에 맞는 REST API 엔드포인트 설계 결과를 구조화
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class APIEndpoint(BaseModel):
    method: str = Field(description="HTTP 메서드 (GET, POST, PUT, DELETE)")
    path: str = Field(description="엔드포인트 경로")
    description: str = Field(description="기능 설명")
    parameters: list[str] = Field(description="필수 파라미터 목록")
    response_type: str = Field(description="응답 데이터 타입")


def main():
    output_parser = JsonOutputParser(pydantic_object=APIEndpoint)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """REST API 설계 전문가입니다.
요청된 기능에 맞는 API 엔드포인트를 설계합니다.
{format_instructions}"""),
        ("human", "다음 기능을 위한 API를 설계해주세요: {feature}"),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    result = chain.invoke({"feature": "사용자 프로필 조회"})
    print(f"Method: {result['method']}")
    print(f"Path: {result['path']}")
    print(f"Description: {result['description']}")
    print(f"Parameters: {result['parameters']}")


if __name__ == "__main__":
    main()
