"""원칙 1: 모호한 프롬프트와 구체적인 프롬프트의 결과 비교."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

llm = get_llm()
parser = StrOutputParser()

vague_prompt = ChatPromptTemplate.from_template("{topic}에 대해 알려줘.")
specific_prompt = ChatPromptTemplate.from_template(
    """{topic}에 대해 다음 형식으로 설명해주세요.
1. 정의: 1~2문장
2. 핵심 특징: 정확히 3가지
3. 실제 활용 사례: 정확히 2가지
전문 용어는 피하고 초보자도 이해할 수 있게 작성해주세요."""
)

inputs = {"topic": "머신러닝"}

print("=== 모호한 프롬프트 결과 ===")
print((vague_prompt | llm | parser).invoke(inputs))

print("\n=== 구체적인 프롬프트 결과 ===")
print((specific_prompt | llm | parser).invoke(inputs))
