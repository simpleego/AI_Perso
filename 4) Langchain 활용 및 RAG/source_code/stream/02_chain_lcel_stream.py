"""PDF의 'LCEL 체인 스트리밍' 예제."""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common import get_model

model = get_model()
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 비전공자를 가르치는 친절한 AI 강사입니다."),
        ("human", "{topic}에 대해 핵심 개념과 간단한 예시를 들어 설명해 주세요."),
    ]
)
chain = prompt | model | StrOutputParser()

for text_chunk in chain.stream({"topic": "머신러닝"}):
    if text_chunk:
        print(text_chunk, end="", flush=True)
print()
