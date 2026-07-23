"""실전 예제: 구조화된 비즈니스 분석 리포트 생성."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

sales_data = """월,매출,신규고객,재구매율
1월,1200,80,32%
2월,1350,95,35%
3월,1280,70,41%
4월,1620,110,44%
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 비즈니스 분석 전문가입니다.
작성 규칙:
1. 제공된 데이터에 근거
2. 명확한 인사이트 도출
3. 실행 가능한 권고안 제시

리포트 구조:
## 요약
## 주요 발견사항
## 상세 분석
## 권고사항
## 다음 단계""",
        ),
        (
            "human",
            """다음 데이터를 분석해주세요.
데이터:
{data}

분석 목적: {purpose}
대상 독자: {audience}""",
        ),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {
            "data": sales_data,
            "purpose": "매출 성장 원인과 다음 분기 실행 전략 도출",
            "audience": "소규모 전자상거래 기업 대표",
        }
    )
)
