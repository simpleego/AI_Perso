"""원칙 3: 시스템 메시지에서 역할과 응답 스타일 정의."""

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
            """당신은 10년 경력의 데이터 사이언티스트입니다.
전문 분야:
- 머신러닝 모델 개발
- 데이터 분석과 시각화
- Python, SQL, TensorFlow

응답 스타일:
- 데이터에 근거하여 설명
- 필요한 경우 간단한 코드 포함
- 실무 적용 시 주의점 포함""",
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {"question": "분류 문제에서 정확도만 평가 지표로 사용하면 안 되는 이유는?"}
    )
)
