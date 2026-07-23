"""원칙 2: 컨텍스트 유무에 따른 추천 결과 비교."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

llm = get_llm()
parser = StrOutputParser()

without_context = ChatPromptTemplate.from_template(
    "파이썬 웹 프레임워크를 추천해주세요."
)

with_context = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 시니어 백엔드 개발자입니다."),
        (
            "human",
            """다음 프로젝트 요구사항에 맞는 파이썬 웹 프레임워크를 추천해주세요.

프로젝트 정보:
- 팀 규모: 3명(주니어 2명, 시니어 1명)
- 예상 트래픽: 하루 10만 요청
- 주요 기능: REST API, 실시간 알림
- 개발 기한: 3개월

후보별 장단점과 이 프로젝트에 적합한 이유를 설명해주세요.""",
        ),
    ]
)

print("=== 컨텍스트 없음 ===")
print((without_context | llm | parser).invoke({}))
print("\n=== 컨텍스트 있음 ===")
print((with_context | llm | parser).invoke({}))
