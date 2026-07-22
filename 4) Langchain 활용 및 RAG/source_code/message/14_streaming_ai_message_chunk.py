"""model.stream()이 반환하는 AIMessageChunk를 실시간 출력하는 예제."""

from langchain_core.messages import AIMessageChunk, HumanMessage

from common import get_model


def chunk_text(chunk: AIMessageChunk) -> str:
    # Gemini 2.5는 일반적으로 문자열 content를 반환한다.
    if isinstance(chunk.content, str):
        return chunk.content

    # 향후 모델에서 content block 목록이 반환되는 경우도 처리한다.
    texts: list[str] = []
    for block in chunk.content:
        if isinstance(block, dict) and block.get("type") == "text":
            texts.append(str(block.get("text", "")))
    return "".join(texts)


def main() -> None:
    model = get_model(temperature=0.7)
    message = HumanMessage(content="인공지능 학습을 주제로 네 줄짜리 짧은 시를 써 주세요.")

    print("[스트리밍 시작]\n")
    for chunk in model.stream([message]):
        print(chunk_text(chunk), end="", flush=True)
    print("\n\n[스트리밍 종료]")


if __name__ == "__main__":
    main()
