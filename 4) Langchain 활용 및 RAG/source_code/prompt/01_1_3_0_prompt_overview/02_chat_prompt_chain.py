"""1-3-0: ChatPromptTemplate과 Gemini를 LCEL 체인으로 연결."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 {role} 전문가입니다. 한국어로 답변하세요."),
        ("human", "{question}"),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
response = chain.invoke(
    {
        "role": "Python",
        "question": "리스트와 튜플의 차이점을 초보자 수준으로 설명해주세요.",
    }
)
print(response)
