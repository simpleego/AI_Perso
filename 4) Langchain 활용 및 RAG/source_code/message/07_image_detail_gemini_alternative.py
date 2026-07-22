"""
OpenAI의 detail=low/high 옵션 대신 이미지 해상도를 조정하는 Gemini 실습 예제.

Gemini용 LangChain 메시지에는 OpenAI 전용 detail 값을 사용하지 않는다.
작은 글자나 복잡한 도표를 읽힐 때는 원본 또는 고해상도 이미지를 전달한다.
"""

from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image
from langchain_core.messages import HumanMessage

from common import get_model, print_response

IMAGE_PATH = Path(__file__).parent / "assets" / "sample_diagram.png"


def resized_base64(image_path: Path, max_width: int) -> str:
    if not image_path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    with Image.open(image_path) as image:
        image = image.convert("RGB")
        if image.width > max_width:
            ratio = max_width / image.width
            image = image.resize((max_width, int(image.height * ratio)))

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=92)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def main() -> None:
    model = get_model()

    # 더 자세한 분석이 필요하면 max_width를 충분히 크게 유지한다.
    image_base64 = resized_base64(IMAGE_PATH, max_width=1600)
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "이미지 속 작은 글자와 화살표 관계까지 자세히 읽어 설명해 주세요.",
            },
            {
                "type": "image",
                "base64": image_base64,
                "mime_type": "image/jpeg",
            },
        ]
    )

    response = model.invoke([message])
    print_response(response)


if __name__ == "__main__":
    main()
