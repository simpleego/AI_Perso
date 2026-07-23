"""원칙 6: 제공된 컨텍스트만 사용하는 RAG 스타일 Q&A."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

context = """교육 과정명: 생성형 AI 입문
교육 기간: 4주
수업 시간: 매주 월요일과 수요일 오후 7시
대상: 파이썬 기초 문법을 학습한 성인
수료 조건: 출석률 80% 이상과 최종 프로젝트 제출
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 문서 기반 Q&A 어시스턴트입니다.
1. 제공된 컨텍스트 안의 정보만 사용하세요.
2. 컨텍스트에 없는 정보는 '문서에서 해당 정보를 찾을 수 없습니다'라고 답하세요.
3. 답변 뒤에 근거 문장을 짧게 인용하세요.""",
        ),
        (
            "human",
            """컨텍스트:
{context}

질문: {question}""",
        ),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
for question in ["수료 조건은 무엇인가요?", "수강료는 얼마인가요?"]:
    print(f"\n질문: {question}")
    print(chain.invoke({"context": context, "question": question}))
