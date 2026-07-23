"""입력 질문과 유사한 예제만 동적으로 선택하는 채팅 Few-shot."""

import sys
from pathlib import Path

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_core.vectorstores import InMemoryVectorStore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_embeddings, get_llm

examples = [
    {
        "input": "지구 대기에서 가장 많은 기체는 무엇인가요?",
        "output": "질소이며 약 78%를 차지합니다.",
    },
    {
        "input": "광합성에 필요한 주요 요소는 무엇인가요?",
        "output": "빛, 이산화탄소, 물입니다.",
    },
    {
        "input": "피타고라스 정리를 설명해주세요.",
        "output": "직각삼각형에서 빗변 제곱은 다른 두 변 제곱의 합과 같습니다.",
    },
    {
        "input": "DNA의 기본 구조를 설명해주세요.",
        "output": "두 개의 핵산 사슬이 이중 나선 구조를 이룹니다.",
    },
    {
        "input": "원주율의 정의는 무엇인가요?",
        "output": "원의 둘레와 지름의 비율입니다.",
    },
]

selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,
    embeddings=get_embeddings(),
    vectorstore_cls=InMemoryVectorStore,
    k=2,
    input_keys=["input"],
)

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_selector=selector,
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    ),
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "과학과 수학 질문에 간결하고 정확한 한국어로 답하세요."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | get_llm() | StrOutputParser()
question = "태양계에서 가장 큰 행성은 무엇인가요?"
print(chain.invoke({"input": question}))
