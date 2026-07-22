"""LCEL 체인을 비동기로 스트리밍하는 추가 실습."""

import asyncio

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from common import get_model


async def main() -> None:
    prompt = ChatPromptTemplate.from_template(
        "{subject}의 핵심 개념을 세 문단으로 설명해 주세요."
    )
    chain = prompt | get_model() | StrOutputParser()

    async for text_chunk in chain.astream({"subject": "RAG"}):
        if text_chunk:
            print(text_chunk, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
