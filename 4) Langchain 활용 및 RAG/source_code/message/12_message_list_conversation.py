"""System/Human/AI 메시지 리스트로 이전 대화 맥락을 구성하는 예제."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()

    messages = [
        SystemMessage(content="당신은 한국 가정식 요리 전문가입니다."),
        HumanMessage(content="김치찌개 만드는 법을 알려 주세요."),
        AIMessage(
            content=(
                "김치와 돼지고기를 볶고 물과 양념을 넣어 끓인 뒤, "
                "두부와 대파를 넣으면 됩니다."
            )
        ),
        HumanMessage(content="앞에서 설명한 김치찌개를 고기 없이 만들 수 있나요?"),
    ]

    response = model.invoke(messages)
    print_response(response)


if __name__ == "__main__":
    main()
