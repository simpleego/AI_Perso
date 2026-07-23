"""Gemini 임베딩과 InMemoryVectorStore로 유사한 예제를 선택."""

import sys
from pathlib import Path

from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.vectorstores import InMemoryVectorStore

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_embeddings

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
    {
        "question": "원주율의 정의는 무엇인가요?",
        "answer": "원의 둘레와 지름의 비율입니다.",
    },
]

selector = SemanticSimilarityExampleSelector.from_examples(
    examples=examples,
    embeddings=get_embeddings(),
    vectorstore_cls=InMemoryVectorStore,
    k=2,
    input_keys=["question"],
)

question = "화성 표면이 붉게 보이는 이유는 무엇인가요?"
selected = selector.select_examples({"question": question})

print("질문:", question)
print("\n선택된 예제:")
for index, example in enumerate(selected, start=1):
    print(f"{index}. {example}")
