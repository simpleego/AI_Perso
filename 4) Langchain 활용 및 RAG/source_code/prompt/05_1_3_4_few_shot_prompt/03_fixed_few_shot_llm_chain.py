"""FewShotPromptTemplate을 Gemini와 연결."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

examples = [
    {"question": "지구의 자전 주기는?", "answer": "약 24시간입니다."},
    {"question": "원주율의 정의는?", "answer": "원의 둘레를 지름으로 나눈 비율입니다."},
    {"question": "DNA의 기본 구조는?", "answer": "두 가닥의 이중 나선 구조입니다."},
]

example_prompt = PromptTemplate.from_template(
    "질문: {question}\n답변: {answer}"
)
prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="과학 질문에 정확하고 간결하게 한두 문장으로 답하세요.",
    suffix="질문: {input}\n답변:",
    input_variables=["input"],
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"input": "태양계에서 가장 큰 행성은 무엇인가요?"}))
