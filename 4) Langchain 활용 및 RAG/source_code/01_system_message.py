"""SystemMessage로 모델의 역할과 답변 규칙을 설정하는 예제."""

from langchain_core.messages import HumanMessage, SystemMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()

    messages = [
        SystemMessage(
            content=(
                "당신은 파이썬 프로그래밍 강사입니다.\n"
                "- 비전공자도 이해할 수 있게 설명하세요.\n"
                "- 짧은 코드 예제를 포함하세요.\n"
                "- 모든 답변은 한국어로 작성하세요."
            )
        ),
        HumanMessage(content="파이썬의 리스트와 튜플 차이를 설명해 주세요."),
    ]

    response = model.invoke(messages)
    print_response(response)


if __name__ == "__main__":
    main()
