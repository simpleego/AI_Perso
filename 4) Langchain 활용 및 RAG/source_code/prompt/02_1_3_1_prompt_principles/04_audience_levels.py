"""원칙 2: 대상 청중에 따라 응답 난이도를 변경."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 교육 콘텐츠 전문가입니다.
대상 청중: {audience}
- 초보자: 비유와 일상 예시를 사용하고 전문 용어를 최소화
- 중급자: 개념과 간단한 실습을 함께 제시
- 전문가: 내부 동작, 설계 선택, 최적화 관점 포함""",
        ),
        ("human", "{topic}에 대해 설명해주세요."),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
for audience in ["초보자", "전문가"]:
    print(f"\n=== {audience}용 설명 ===")
    print(chain.invoke({"audience": audience, "topic": "REST API"}))
