"""모든 실습에서 공통으로 사용하는 모델 초기화 코드."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


def get_model():
    """`.env`를 읽고 LangChain 채팅 모델을 반환합니다."""
    load_dotenv()

    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY가 없습니다. "
            ".env.example을 .env로 복사한 뒤 API 키를 입력하세요."
        )

    model_name = os.getenv(
        "MODEL_NAME", "google_genai:gemini-2.5-flash-lite"
    )
    return init_chat_model(model_name, temperature=0)


def print_final_answer(result: dict) -> None:
    """에이전트 실행 결과의 마지막 메시지만 보기 좋게 출력합니다."""
    print("\n=== 최종 답변 ===")
    print(result["messages"][-1].content)

