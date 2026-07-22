"""도구 내부의 진행 상황을 get_stream_writer()로 전달한다."""

import time

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.config import get_stream_writer

from common import get_model


@tool
def process_documents(count: int) -> str:
    """지정한 개수의 문서를 순차 처리하고 진행 상황을 스트리밍한다."""
    if count < 1 or count > 20:
        return "count는 1 이상 20 이하로 입력해야 합니다."

    writer = get_stream_writer()
    for index in range(count):
        time.sleep(0.3)  # 실제 처리 시간을 흉내 낸다.
        completed = index + 1
        writer(
            {
                "progress": f"문서 {completed}/{count} 처리 중",
                "percent": round(completed / count * 100),
            }
        )
    return f"총 {count}개 문서 처리를 완료했습니다."


agent = create_agent(
    model=get_model(),
    tools=[process_documents],
    system_prompt="문서 처리 요청에는 반드시 process_documents 도구를 사용하세요.",
)

for part in agent.stream(
    {"messages": [{"role": "user", "content": "5개 문서를 처리해 주세요."}]},
    stream_mode="custom",
    version="v2",
):
    if part["type"] == "custom":
        event = part["data"]
        print(f"진행률 {event['percent']:>3}% - {event['progress']}")
