"""공개 이미지 URL을 HumanMessage에 넣어 분석하는 멀티모달 예제."""

from langchain_core.messages import HumanMessage

from common import get_model, print_response

IMAGE_URL = "https://picsum.photos/seed/langchain-message/640/420"


def main() -> None:
    model = get_model()

    message = HumanMessage(
        content=[
            {"type": "text", "text": "이 이미지에서 보이는 내용을 한국어로 설명해 주세요."},
            {"type": "image", "url": IMAGE_URL},
        ]
    )

    response = model.invoke([message])
    print_response(response)


if __name__ == "__main__":
    main()
