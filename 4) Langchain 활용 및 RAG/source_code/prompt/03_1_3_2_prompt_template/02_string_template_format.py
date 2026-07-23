"""PromptTemplate.from_template과 format 사용."""

from langchain_core.prompts import PromptTemplate

template_text = "안녕하세요, 제 이름은 {name}이고 나이는 {age}살입니다."
prompt_template = PromptTemplate.from_template(template_text)

print("입력 변수:", prompt_template.input_variables)
print(prompt_template.format(name="홍길동", age=30))
