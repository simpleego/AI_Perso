"""여러 AIMessageChunk를 결합하여 최종 AIMessage를 만드는 실습."""

from langchain_core.messages import HumanMessage

from common import content_to_text, get_model

model = get_model()
chunks = []

print("[실시간 출력]")
for chunk in model.stream([HumanMessage(content="생성형 AI의 특징 3가지를 알려 주세요.")]):
    chunks.append(chunk)
    text = content_to_text(chunk.content)
    if text:
        print(text, end="", flush=True)

print(f"\n\n수신한 청크 수: {len(chunks)}")

if chunks:
    combined = chunks[0]
    for chunk in chunks[1:]:
        combined = combined + chunk

    print("\n[청크 결합 후 전체 내용]")
    print(content_to_text(combined.content))
    print("\n[응답 메타데이터]")
    print(combined.response_metadata)
