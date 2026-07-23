"""Few-shot 예제 하나를 일정한 형식으로 만드는 포맷터."""

from langchain_core.prompts import PromptTemplate

example_prompt = PromptTemplate.from_template(
    "질문: {question}\n답변: {answer}"
)

formatted = example_prompt.format(
    question="광합성에 필요한 주요 요소는 무엇인가요?",
    answer="빛, 이산화탄소, 물입니다.",
)
print(formatted)
