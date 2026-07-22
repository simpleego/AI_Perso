"""disable_streaming 옵션을 적용했을 때의 동작을 확인한다."""

from langchain_core.messages import HumanMessage

from common import content_to_text, get_model

model = get_model(disable_streaming=True)
message = HumanMessage(content="LangChain 스트리밍을 두 문장으로 설명해 주세요.")

print("[invoke(): 전체 응답을 한 번에 수신]")
response = model.invoke([message])
print(content_to_text(response.content))

print("\n[stream(): 스트리밍이 비활성화되어 일반적으로 전체 결과가 한 청크로 반환됨]")
chunk_count = 0
for chunk in model.stream([message]):
    chunk_count += 1
    print(content_to_text(chunk.content), end="", flush=True)
print(f"\n수신 청크 수: {chunk_count}")
