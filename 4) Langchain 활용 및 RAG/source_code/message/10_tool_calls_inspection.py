"""Gemini가 생성한 AIMessage의 tool_calls 정보를 확인하는 예제."""

from pprint import pprint

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from common import get_model


@tool
def get_weather(city: str) -> str:
    """지정한 도시의 현재 날씨를 조회한다."""
    weather_data = {
        "서울": "맑음, 25도",
        "부산": "흐림, 23도",
        "대전": "구름 조금, 24도",
    }
    return weather_data.get(city, f"{city}의 예제 날씨 데이터가 없습니다.")


def main() -> None:
    model = get_model()
    model_with_tools = model.bind_tools([get_weather])

    response = model_with_tools.invoke(
        [HumanMessage(content="서울 날씨를 확인해 주세요. 반드시 get_weather 도구를 사용하세요.")]
    )

    print("[AIMessage content]")
    print(response.content)

    print("\n[AIMessage tool_calls]")
    if not response.tool_calls:
        print("도구 호출이 생성되지 않았습니다. 프롬프트를 다시 실행해 보세요.")
        return

    for tool_call in response.tool_calls:
        pprint(tool_call)
        print(f"도구 이름: {tool_call['name']}")
        print(f"도구 인자: {tool_call['args']}")
        print(f"호출 ID: {tool_call['id']}\n")


if __name__ == "__main__":
    main()
