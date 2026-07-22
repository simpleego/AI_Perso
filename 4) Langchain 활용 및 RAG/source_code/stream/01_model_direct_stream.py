"""PDF의 '모델 직접 스트리밍' 예제."""

from langchain_core.messages import HumanMessage

from common import get_model, print_stream_chunk

model = get_model()
message = HumanMessage(content="파이썬의 장점 5가지를 초보자도 이해하도록 설명해 주세요.")

print("[Gemini 스트리밍 시작]\n")
for chunk in model.stream([message]):
    print_stream_chunk(chunk)
print("\n\n[스트리밍 종료]")
