"""원칙 4: JsonOutputParser로 JSON 객체를 파싱."""

import sys
from pathlib import Path

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

parser = JsonOutputParser()
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "다른 설명 없이 유효한 JSON만 반환하세요.\n{format_instructions}",
        ),
        (
            "human",
            """다음 문장에서 name, email, phone을 추출하세요.
텍스트: {text}""",
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())

chain = prompt | get_llm() | parser
result = chain.invoke(
    {
        "text": "홍길동의 이메일은 gildong@example.com이며 전화번호는 010-1234-5678입니다."
    }
)
print(result)
print(type(result))
