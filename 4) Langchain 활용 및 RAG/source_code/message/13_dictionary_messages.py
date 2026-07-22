"""메시지 객체 대신 role/content 딕셔너리 목록을 사용하는 예제."""

from common import get_model, print_response


def main() -> None:
    model = get_model()

    messages = [
        {"role": "system", "content": "당신은 유용한 AI 프로그래밍 강사입니다."},
        {"role": "user", "content": "파이썬이란 무엇인가요?"},
        {
            "role": "assistant",
            "content": "파이썬은 읽기 쉬운 문법을 가진 범용 프로그래밍 언어입니다.",
        },
        {"role": "user", "content": "방금 설명한 파이썬의 주요 특징을 세 가지만 알려 주세요."},
    ]

    response = model.invoke(messages)
    print_response(response)


if __name__ == "__main__":
    main()
