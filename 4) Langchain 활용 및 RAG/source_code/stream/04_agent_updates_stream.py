"""에이전트 단계별 진행 상황을 stream_mode='updates'로 확인한다."""

from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool

from common import content_to_text, get_model


@tool
def get_weather(city: str) -> str:
    """도시의 날씨를 조회한다. 교육용 예제이므로 고정된 가상 데이터를 반환한다."""
    return f"{city}의 현재 날씨는 맑음이고 기온은 25도입니다."


agent = create_agent(
    model=get_model(),
    tools=[get_weather],
    system_prompt="날씨 질문에는 반드시 get_weather 도구를 사용하세요.",
)

request: dict[str, Any] = {
    "messages": [{"role": "user", "content": "서울 날씨를 알려 주세요."}]
}

for part in agent.stream(
    request,
    stream_mode="updates",
    version="v2",
):
    if part["type"] != "updates":
        continue

    for step_name, state_update in part["data"].items():
        print(f"\n[단계: {step_name}]")
        messages = state_update.get("messages", [])
        if not messages:
            print(state_update)
            continue

        last_message = messages[-1]
        text = content_to_text(last_message.content)
        print("메시지 종류:", type(last_message).__name__)
        if getattr(last_message, "tool_calls", None):
            print("도구 호출:", last_message.tool_calls)
        if text:
            print("내용:", text)
