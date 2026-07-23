"""원칙 5: 시스템 메시지 안에 번역 패턴 예시 제공."""

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
            """당신은 자연스러운 한영 번역가입니다.
예시:
입력: 오늘 하루도 화이팅!
출력: Have a great day today!

입력: 맛있게 드세요.
출력: Enjoy your meal!

입력: 수고하셨습니다.
출력: Thank you for your hard work!

직역보다 실제 영어권에서 자연스러운 표현을 우선하세요.""",
        ),
        ("human", "다음을 영어로 번역해주세요: {text}"),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(chain.invoke({"text": "조심히 들어가세요."}))
