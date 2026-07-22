"""AIMessage의 content, usage_metadata, response_metadata를 확인하는 예제."""

from pprint import pprint

from langchain_core.messages import HumanMessage

from common import get_model, print_response


def main() -> None:
    model = get_model()
    response = model.invoke([HumanMessage(content="프롬프트 엔지니어링을 한 문장으로 설명해 주세요.")])

    print("[응답 내용]")
    print_response(response)

    print("\n[토큰 사용량: usage_metadata]")
    pprint(response.usage_metadata)

    print("\n[응답 메타데이터: response_metadata]")
    pprint(response.response_metadata)

    print("\n[추가 정보]")
    print("message id:", response.id)
    pprint(response.additional_kwargs)


if __name__ == "__main__":
    main()
