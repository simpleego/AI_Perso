"""
1-5-2. JSON Parser - 오류 처리 (파싱 실패 대응)
LLM 출력이 올바른 JSON이 아닐 때를 대비한 안전한 파싱 함수
"""
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from _common import get_llm


class SimpleData(BaseModel):
    name: str = Field(description="이름")
    value: int = Field(description="숫자 값")


def safe_parse(chain, input_data):
    """안전한 파싱 함수"""
    try:
        result = chain.invoke(input_data)
        return {"success": True, "data": result}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON 파싱 오류: {e}"}
    except Exception as e:
        return {"success": False, "error": f"처리 오류: {e}"}


def main():
    output_parser = JsonOutputParser(pydantic_object=SimpleData)

    prompt = ChatPromptTemplate.from_template(
        "{query}\n{format_instructions}"
    ).partial(format_instructions=output_parser.get_format_instructions())

    llm = get_llm(temperature=0)
    chain = prompt | llm | output_parser

    result = safe_parse(chain, {"query": "테스트 데이터를 생성해주세요"})
    if result["success"]:
        print(f"성공: {result['data']}")
    else:
        print(f"실패: {result['error']}")


if __name__ == "__main__":
    main()
