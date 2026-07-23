"""1-3-0: PromptTemplate 기본 문자열 생성."""

from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "{topic}에 대해 {length}자 이내로 설명해주세요."
)

completed_prompt = prompt_template.format(topic="인공지능", length=100)
print(completed_prompt)
