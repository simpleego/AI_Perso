"""로컬 이미지를 Base64로 인코딩해 Gemini에 전달하는 예제."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from langchain_core.messages import HumanMessage

from common import get_model, print_response

IMAGE_PATH = Path(__file__).parent / "assets" / "sample_diagram.png"


def encode_image(image_path: Path) -> tuple[str, str]:
    if not image_path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    image_base64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return image_base64, mime_type


def main() -> None:
    model = get_model()
    image_base64, mime_type = encode_image(IMAGE_PATH)

    message = HumanMessage(
        content=[
            {"type": "text", "text": "이 다이어그램의 처리 순서를 단계별로 설명해 주세요."},
            {
                "type": "image",
                "base64": image_base64,
                "mime_type": mime_type,
            },
        ]
    )

    response = model.invoke([message])
    print_response(response)


if __name__ == "__main__":
    main()
