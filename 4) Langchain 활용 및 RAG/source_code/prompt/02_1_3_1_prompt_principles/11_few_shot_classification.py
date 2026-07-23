"""원칙 5: Few-shot 예시를 사용한 사용자 요청 분류."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

examples = [
    {"input": "오늘 날씨 어때?", "output": "일상 대화"},
    {"input": "파이썬으로 웹서버 만드는 법", "output": "기술 질문"},
    {"input": "내일 회의 일정 잡아줘", "output": "업무 요청"},
]

example_prompt = ChatPromptTemplate.from_messages(
    [("human", "{input}"), ("ai", "{output}")]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "사용자 입력을 다음 중 하나로만 분류하세요: 일상 대화, 기술 질문, 업무 요청",
        ),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)

chain = final_prompt | get_llm() | StrOutputParser()
print(chain.invoke({"input": "React 컴포넌트 만드는 방법을 알려줘"}))
