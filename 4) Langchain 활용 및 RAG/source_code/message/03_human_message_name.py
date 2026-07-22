"""HumanMessage의 선택 속성인 name을 지정하는 예제."""

from langchain_core.messages import HumanMessage, SystemMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()

    user_message = HumanMessage(
        content="오늘 학습할 파이썬 주제 하나를 추천해 주세요.",
        name="student_park",
    )

    print(f"메시지 이름: {user_message.name}")
    response = model.invoke(
        [
            SystemMessage(content="당신은 초보자용 파이썬 학습 코치입니다."),
            user_message,
        ]
    )
    print_response(response)


if __name__ == "__main__":
    main()
