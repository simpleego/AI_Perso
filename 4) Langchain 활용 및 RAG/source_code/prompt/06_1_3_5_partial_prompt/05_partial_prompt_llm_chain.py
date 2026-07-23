"""Partial PromptTemplate을 Gemini 체인으로 실행."""

import sys
from datetime import datetime
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm


def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


base_prompt = PromptTemplate.from_template(
    """작성일: {date}
대상: {audience}
주제: {topic}

위 주제를 대상 수준에 맞춰 정의, 예시, 확인 문제 순서로 설명하세요."""
)
partial_prompt = base_prompt.partial(
    date=current_date,
    audience="파이썬 기초를 학습한 비전공자",
)

chain = partial_prompt | get_llm() | StrOutputParser()
print(chain.invoke({"topic": "PromptTemplate의 partial 기능"}))
