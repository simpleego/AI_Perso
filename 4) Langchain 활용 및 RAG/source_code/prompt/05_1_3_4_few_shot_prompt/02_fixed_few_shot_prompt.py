"""고정 예제 목록을 사용하는 FewShotPromptTemplate."""

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

examples = [
    {
        "question": "지구 대기에서 가장 많은 기체는 무엇인가요?",
        "answer": "질소이며 약 78%를 차지합니다.",
    },
    {
        "question": "광합성에 필요한 주요 요소는 무엇인가요?",
        "answer": "빛, 이산화탄소, 물입니다.",
    },
    {
        "question": "피타고라스 정리를 설명해주세요.",
        "answer": "직각삼각형에서 빗변 제곱은 다른 두 변 제곱의 합과 같습니다.",
    },
    {
        "question": "DNA의 기본 구조는 무엇인가요?",
        "answer": "두 개의 사슬이 이중 나선 구조를 이룹니다.",
    },
]

example_prompt = PromptTemplate.from_template(
    "질문: {question}\n답변: {answer}"
)

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="다음 예시와 같은 길이와 문체로 답변하세요.",
    suffix="질문: {input}\n답변:",
    input_variables=["input"],
)

print(prompt.invoke({"input": "화성 표면이 붉은 이유는 무엇인가요?"}).to_string())
