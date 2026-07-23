"""FewShotChatMessagePromptTemplate에 고정 예제를 사용."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

examples = [
    {
        "input": "지구 대기에서 가장 많은 기체는 무엇인가요?",
        "output": "질소입니다.",
    },
    {
        "input": "광합성에 필요한 주요 요소는 무엇인가요?",
        "output": "빛, 이산화탄소, 물입니다.",
    },
]

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "{input}"), ("ai", "{output}")]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "과학과 수학 질문에 한두 문장으로 정확히 답하세요."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | get_llm() | StrOutputParser()
print(chain.invoke({"input": "지구의 자전 주기는 얼마인가요?"}))
