"""원칙 4: 번호 목록 형식 지정."""

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
            "응답은 정확히 5개의 번호 목록으로 작성하고 각 항목은 한 줄로 제한하세요.",
        ),
        ("human", "{topic}의 장점 5가지를 알려주세요."),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"topic": "LangChain"}))
