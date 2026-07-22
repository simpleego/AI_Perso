"""Gemini 연동에서 현재 사용하는 타임아웃·재시도 옵션 예제."""

from langchain_core.messages import HumanMessage

from common import get_model, print_stream_chunk

# PDF의 OpenAI 예제와 달리 ChatGoogleGenerativeAI에서는
# request_timeout과 retries 매개변수를 사용한다.
model = get_model(request_timeout=30.0, retries=2)

try:
    for chunk in model.stream(
        [HumanMessage(content="스트리밍 타임아웃이 필요한 이유를 설명해 주세요.")]
    ):
        print_stream_chunk(chunk)
    print()
except TimeoutError:
    print("요청 시간이 초과되었습니다.")
except Exception as exc:
    print(f"API 요청 중 오류가 발생했습니다: {exc}")
