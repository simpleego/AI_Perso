"""모델 호출 결과가 AIMessage 객체로 반환되는지 확인하는 예제."""

from langchain_core.messages import AIMessage, HumanMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()
    response = model.invoke([HumanMessage(content="안녕하세요! 한 문장으로 인사해 주세요.")])

    print(f"반환 클래스: {type(response).__name__}")
    print(f"AIMessage 여부: {isinstance(response, AIMessage)}")
    print("응답 내용:")
    print_response(response)


if __name__ == "__main__":
    main()
