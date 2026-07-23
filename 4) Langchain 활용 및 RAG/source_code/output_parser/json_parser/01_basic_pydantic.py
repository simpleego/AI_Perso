"""
1-5-2. JSON Parser - 기본 사용법
Pydantic 모델로 스키마를 정의하고 포맷 지시사항 확인 (LLM 호출 없이 동작)
"""
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


# Pydantic 모델 정의
class CuisineRecipe(BaseModel):
    name: str = Field(description="요리 이름")
    ingredients: list[str] = Field(description="필요한 재료 목록")
    cooking_time: int = Field(description="조리 시간 (분)")
    difficulty: str = Field(description="난이도: 쉬움/보통/어려움")


def main():
    # JSON 파서 생성
    output_parser = JsonOutputParser(pydantic_object=CuisineRecipe)

    # 포맷 지시사항 확인 (JSON 스키마 기반 출력 안내)
    format_instructions = output_parser.get_format_instructions()
    print("=== 포맷 지시사항 ===")
    print(format_instructions)


if __name__ == "__main__":
    main()
