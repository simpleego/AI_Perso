"""MessagePromptTemplate 기반 ChatPromptTemplate을 LLM과 연결."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "당신은 {domain} 전문 교육자입니다. 답변은 한국어로 작성하세요."
        ),
        HumanMessagePromptTemplate.from_template("{user_input}"),
    ]
)

chain = chat_prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {
            "domain": "천문학",
            "user_input": "목성과 지구의 크기를 간단히 비교해주세요.",
        }
    )
)
