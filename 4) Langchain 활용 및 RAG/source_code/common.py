"""모든 실습 파일에서 공통으로 사용하는 Gemini 모델 초기화 모듈."""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

DEFAULT_MODEL = "gemini-2.5-flash-lite"


def get_model(*, temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """환경 변수에서 API 키를 읽어 Gemini 채팅 모델을 반환한다."""
    load_dotenv()

    # langchain-google-genai는 GOOGLE_API_KEY를 우선 사용하고
    # GEMINI_API_KEY도 대체 환경 변수로 지원한다.
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Gemini API Key가 없습니다. .env 파일에 "
            "GOOGLE_API_KEY=발급받은_키 형식으로 저장하세요."
        )

    # 사용자가 GEMINI_API_KEY만 설정했을 때도 일관되게 동작하도록 복사한다.
    os.environ.setdefault("GOOGLE_API_KEY", api_key)

    model_name = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
    )


def print_response(response: Any) -> None:
    """Gemini 2.5/3.x 응답 형식 차이를 고려해 텍스트를 출력한다."""
    text = getattr(response, "text", None)
    if text:
        print(text)
    else:
        print(getattr(response, "content", response))
