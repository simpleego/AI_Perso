"""
1-5-2. JSON Parser - 체인 구성 및 실행
레시피 정보를 구조화된 딕셔너리(dict)로 받아오기
"""
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class CuisineRecipe(BaseModel):
    name: str = Field(description="요리 이름")
    ingredients: list[str] = Field(description="필요한 재료 목록")
    cooking_time: int = Field(description="조리 시간 (분)")
    difficulty: str = Field(description="난이도: 쉬움/보통/어려움")


def main():
    output_parser = JsonOutputParser(pydantic_object=CuisineRecipe)

    # 프롬프트 구성
    prompt = PromptTemplate(
        template="{query}에 대한 레시피 정보를 제공해주세요.\n{format_instructions}",
        input_variables=["query"],
        partial_variables={
            "format_instructions": output_parser.get_format_instructions()
        },
    )

    # 모델 초기화 및 체인 구성 (무료 API 키 사용 가능한 Gemini)
    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    # 실행
    result = chain.invoke({"query": "비빔밥"})
    print(result)
    print(type(result))  # <class 'dict'>


if __name__ == "__main__":
    main()
