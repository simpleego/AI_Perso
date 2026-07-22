"""LangChain의 네 가지 기본 메시지 객체를 생성해 확인하는 예제."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage


def main() -> None:
    messages = [
        SystemMessage(content="당신은 친절한 한국어 AI 어시스턴트입니다."),
        HumanMessage(content="파이썬 리스트를 간단히 설명해 주세요."),
        AIMessage(content="파이썬 리스트는 여러 값을 순서대로 저장하는 자료형입니다."),
        ToolMessage(
            content="서울의 현재 온도는 25도입니다.",
            tool_call_id="call_example_001",
            name="get_weather",
        ),
    ]

    for index, message in enumerate(messages, start=1):
        print(f"[{index}] 클래스: {type(message).__name__}")
        print(f"    내용: {message.content}")
        print(f"    이름: {message.name}\n")


if __name__ == "__main__":
    main()
