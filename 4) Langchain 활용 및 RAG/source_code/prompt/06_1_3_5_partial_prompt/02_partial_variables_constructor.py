"""PromptTemplate 생성 시 partial_variables 지정."""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    template="지구의 {layer}에서 대표적으로 풍부한 원소는 {element}입니다.",
    input_variables=["element"],
    partial_variables={"layer": "맨틀"},
)

print("사용자 입력 변수:", prompt.input_variables)
print("미리 지정된 변수:", prompt.partial_variables)
print(prompt.format(element="규소"))
