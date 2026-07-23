"""원칙 6: 불확실한 정보에 대해 추측하지 않도록 지시."""

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
            """당신은 정확한 정보만 제공하는 AI입니다.
규칙:
1. 확인할 수 없는 정보는 '확실하지 않습니다'라고 명시하세요.
2. 추론이 필요한 경우 '추론입니다'라고 표시하세요.
3. 최신 정보가 필요한 질문은 별도 검증이 필요하다고 안내하세요.
4. 존재하지 않는 사실이나 출처를 만들지 마세요.""",
        ),
        ("human", "{question}"),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"question": "LangChain 9.0의 공식 출시일과 핵심 기능을 알려주세요."}))
