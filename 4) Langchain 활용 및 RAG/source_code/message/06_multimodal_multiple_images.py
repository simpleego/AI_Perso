"""두 개의 로컬 이미지를 한 메시지에 넣어 비교하는 예제."""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from langchain_core.messages import HumanMessage

from common import get_model, print_response

ASSET_DIR = Path(__file__).parent / "assets"
IMAGE_PATHS = [
    ASSET_DIR / "sample_diagram.png",
    ASSET_DIR / "sample_chart.png",
]


def image_part(image_path: Path) -> dict[str, str]:
    if not image_path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    mime_type = mimetypes.guess_type(image_path.name)[0] or "image/png"
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return {"type": "image", "base64": encoded, "mime_type": mime_type}


def main() -> None:
    model = get_model()

    content = [
        {
            "type": "text",
            "text": "첫 번째 이미지와 두 번째 이미지의 목적과 표현 방식 차이를 비교해 주세요.",
        }
    ]
    content.extend(image_part(path) for path in IMAGE_PATHS)

    response = model.invoke([HumanMessage(content=content)])
    print_response(response)


if __name__ == "__main__":
    main()
