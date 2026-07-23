"""원칙 3: 단계별 분석 순서를 명시한 코드 리뷰 프롬프트."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

sample_code = """def average(values):
    total = 0
    for value in values:
        total += value
    return total / len(values)
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 Python 코드 리뷰 전문가입니다."),
        (
            "human",
            """다음 코드를 리뷰해주세요.

<code>
{code}
</code>

다음 순서로 분석해주세요.
1. 기능 요약
2. 잘 작성된 부분 2가지
3. 개선이 필요한 부분 2~3가지
4. 예외 처리를 포함한 리팩토링 코드
각 섹션을 마크다운 제목으로 구분하세요.""",
        ),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"code": sample_code}))
