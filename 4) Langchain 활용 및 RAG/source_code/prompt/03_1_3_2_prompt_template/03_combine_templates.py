"""PromptTemplate + PromptTemplate + 문자열 결합."""

from langchain_core.prompts import PromptTemplate

profile_prompt = PromptTemplate.from_template(
    "안녕하세요, 제 이름은 {name}이고 나이는 {age}살입니다."
)

combined_prompt = (
    profile_prompt
    + PromptTemplate.from_template("\n\n아버지를 아버지라 부를 수 없습니다.")
    + "\n\n위 전체 문장을 {language}로 자연스럽게 번역해주세요."
)

print("통합 입력 변수:", combined_prompt.input_variables)
print(
    combined_prompt.format(name="홍길동", age=30, language="영어")
)
