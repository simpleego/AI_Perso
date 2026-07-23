"""
1-5-2. JSON Parser - ChatPromptTemplate과 함께 사용
제품 분석 결과를 구조화하고 dict 키로 접근
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class ProductInfo(BaseModel):
    name: str = Field(description="제품명")
    category: str = Field(description="카테고리")
    price_range: str = Field(description="가격대: 저가/중가/고가")
    features: list[str] = Field(description="주요 특징 3가지")


def main():
    output_parser = JsonOutputParser(pydantic_object=ProductInfo)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 제품 분석 전문가입니다.\n{format_instructions}"),
        ("human", "{product}에 대해 분석해주세요."),
    ]).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    result = chain.invoke({"product": "아이폰 15"})
    print(f"제품명: {result['name']}")
    print(f"카테고리: {result['category']}")
    print(f"가격대: {result['price_range']}")
    print(f"특징: {result['features']}")


if __name__ == "__main__":
    main()
