"""updates와 messages를 동시에 수신하는 멀티 모드 스트리밍."""

from langchain.agents import create_agent
from langchain.tools import tool

from common import content_to_text, get_model


@tool
def get_weather(city: str) -> str:
    """도시의 날씨를 조회한다. 교육용 고정 데이터를 반환한다."""
    return f"{city}의 현재 날씨는 맑음이고 기온은 25도입니다."


agent = create_agent(
    model=get_model(),
    tools=[get_weather],
    system_prompt="날씨 질문에는 반드시 get_weather 도구를 사용하세요.",
)

for part in agent.stream(
    {"messages": [{"role": "user", "content": "부산 날씨를 알려 주세요."}]},
    stream_mode=["updates", "messages"],
    version="v2",
):
    mode = part["type"]
    data = part["data"]

    if mode == "updates":
        print(f"\n\n[상태 업데이트] {list(data.keys())}")

    elif mode == "messages":
        token, metadata = data
        text = content_to_text(token.content)
        if text:
            print(text, end="", flush=True)

print()
