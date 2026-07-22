"""AI의 도구 호출을 실행하고 ToolMessage로 결과를 되돌려주는 전체 흐름."""

from __future__ import annotations

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import BaseTool, tool

from common import get_model, print_response


@tool
def get_weather(city: str) -> str:
    """지정한 도시의 현재 날씨를 조회한다."""
    weather_data = {
        "서울": "맑음, 25도, 습도 60%",
        "부산": "흐림, 23도, 습도 72%",
        "대전": "구름 조금, 24도, 습도 58%",
    }
    return weather_data.get(city, f"{city}의 예제 날씨 데이터가 없습니다.")


def execute_tool_call(tool_call: dict, tools_by_name: dict[str, BaseTool]) -> ToolMessage:
    tool_name = tool_call["name"]
    if tool_name not in tools_by_name:
        return ToolMessage(
            content=f"등록되지 않은 도구입니다: {tool_name}",
            tool_call_id=tool_call["id"],
        )

    result = tools_by_name[tool_name].invoke(tool_call["args"])
    return ToolMessage(
        content=str(result),
        tool_call_id=tool_call["id"],
        name=tool_name,
    )


def main() -> None:
    tools = [get_weather]
    tools_by_name = {tool.name: tool for tool in tools}

    model = get_model()
    model_with_tools = model.bind_tools(tools)

    messages = [
        HumanMessage(
            content="서울 날씨를 도구로 확인한 뒤, 외출 복장을 한 문장으로 추천해 주세요."
        )
    ]

    # 1단계: 모델이 도구 호출을 결정한다.
    ai_message = model_with_tools.invoke(messages)
    messages.append(ai_message)  # 도구 호출 정보가 든 AIMessage 전체를 보존한다.

    if not ai_message.tool_calls:
        print("모델이 도구를 호출하지 않았습니다.")
        print_response(ai_message)
        return

    # 2단계: 애플리케이션이 실제 파이썬 함수를 실행한다.
    for tool_call in ai_message.tool_calls:
        tool_message = execute_tool_call(tool_call, tools_by_name)
        print(f"도구 실행 결과: {tool_message.content}")
        messages.append(tool_message)

    # 3단계: 도구 결과를 받은 모델이 최종 자연어 답변을 생성한다.
    final_response = model_with_tools.invoke(messages)
    print("\n최종 답변:")
    print_response(final_response)


if __name__ == "__main__":
    main()
