"""원칙 1: 길이, 문체, 용어 사용 규칙을 명시."""

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
            """당신은 기술 문서 작성 전문가입니다.
응답 규칙:
- 각 문장은 20단어 이내
- 능동태 사용
- 전문 용어 사용 시 괄호 안에 쉬운 설명 추가
- 전체 응답은 200자 이내
- 한국어 사용""",
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"question": "REST API가 무엇인지 설명해주세요."}))
