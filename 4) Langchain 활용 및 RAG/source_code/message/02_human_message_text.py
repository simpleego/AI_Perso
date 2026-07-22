"""일반 텍스트를 HumanMessage로 전달하는 가장 기본적인 예제."""

from langchain_core.messages import HumanMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()
    message = HumanMessage(content="파이썬 리스트 컴프리헨션을 예제와 함께 설명해 주세요.")

    response = model.invoke([message])
    print_response(response)


if __name__ == "__main__":
    main()
