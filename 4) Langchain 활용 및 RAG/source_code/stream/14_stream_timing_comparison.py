"""invoke와 stream의 체감 차이를 첫 출력 시간 기준으로 비교한다."""

from time import perf_counter

from langchain_core.messages import HumanMessage

from common import content_to_text, get_model

message = HumanMessage(
    content="RAG의 구성 요소와 동작 과정을 비교적 자세하게 설명해 주세요."
)

model = get_model()

start = perf_counter()
response = model.invoke([message])
invoke_elapsed = perf_counter() - start
print(f"invoke 완료 시간: {invoke_elapsed:.2f}초")
print(f"invoke 응답 길이: {len(content_to_text(response.content))}자\n")

start = perf_counter()
first_chunk_time = None
chunk_count = 0
for chunk in model.stream([message]):
    text = content_to_text(chunk.content)
    if text:
        if first_chunk_time is None:
            first_chunk_time = perf_counter() - start
            print(f"stream 첫 텍스트 수신 시간: {first_chunk_time:.2f}초")
        chunk_count += 1
        print(text, end="", flush=True)

stream_elapsed = perf_counter() - start
print(f"\n\nstream 전체 시간: {stream_elapsed:.2f}초")
print(f"텍스트 청크 수: {chunk_count}")
