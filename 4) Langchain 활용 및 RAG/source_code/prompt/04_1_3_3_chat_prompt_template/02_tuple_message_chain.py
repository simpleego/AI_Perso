"""2-튜플 ChatPromptTemplate을 Gemini 체인으로 실행."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 천문학 교육자입니다. 초보자가 이해하도록 3문장 이내로 답하세요.",
        ),
        ("human", "{user_input}"),
    ]
)

chain = chat_prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {"user_input": "태양계에서 가장 큰 행성은 무엇인가요?"}
    )
)
