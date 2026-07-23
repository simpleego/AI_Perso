"""원칙 4: 마크다운 표 형식으로 출력 제한."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "응답은 유효한 마크다운 표 하나로만 작성하세요."),
        (
            "human",
            """다음 프로그래밍 언어를 비교해주세요: {languages}
열 순서: 언어 | 주요 용도 | 장점 | 단점 | 학습 난이도""",
        ),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"languages": "Python, Java, JavaScript"}))
