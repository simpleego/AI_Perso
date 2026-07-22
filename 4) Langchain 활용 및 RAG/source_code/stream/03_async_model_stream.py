"""PDF의 '비동기 스트리밍' 예제."""

import asyncio

from langchain_core.messages import HumanMessage

from common import get_model, print_stream_chunk


async def main() -> None:
    model = get_model()
    message = HumanMessage(content="인공지능을 주제로 짧은 시를 써 주세요.")

    async for chunk in model.astream([message]):
        print_stream_chunk(chunk)
    print()


if __name__ == "__main__":
    asyncio.run(main())
