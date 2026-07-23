"""문자열 값을 partial()로 미리 바인딩."""

from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "지구의 {layer}에서 가장 흔한 원소는 {element}입니다."
)
partial_prompt = prompt.partial(layer="지각")

print("남은 입력 변수:", partial_prompt.input_variables)
print(partial_prompt.format(element="산소"))
