"""
1-5-2. JSON Parser - 중첩 객체 처리
복잡한 스키마 정의(모델 안에 모델)와 중첩 데이터 접근
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


# 중첩 모델 정의
class Author(BaseModel):
    name: str = Field(description="저자 이름")
    nationality: str = Field(description="국적")
    birth_year: int = Field(description="출생 연도")


class BookInfo(BaseModel):
    title: str = Field(description="책 제목")
    author: Author = Field(description="저자 정보")
    year: int = Field(description="출판 연도")
    genres: list[str] = Field(description="장르 목록")
    rating: float = Field(description="평점 (1.0-5.0)")


def main():
    output_parser = JsonOutputParser(pydantic_object=BookInfo)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "책 정보를 분석하여 구조화된 데이터로 제공합니다.\n{format_instructions}"),
        ("human", "{book_name}에 대한 정보를 알려주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    result = chain.invoke({"book_name": "해리포터와 마법사의 돌"})
    print(result)

    # 중첩 객체 접근
    print(f"\n책 제목: {result['title']}")
    print(f"저자: {result['author']['name']}")
    print(f"국적: {result['author']['nationality']}")
    print(f"장르: {', '.join(result['genres'])}")


if __name__ == "__main__":
    main()
