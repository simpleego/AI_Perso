"""모든 예제에서 공통으로 사용하는 Gemini 설정 모듈."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR / ".env")

DEFAULT_CHAT_MODEL = "gemini-2.5-flash-lite"
DEFAULT_EMBEDDING_MODEL = "gemini-embedding-001"


def require_api_key() -> str:
    """GOOGLE_API_KEY를 검사하고 반환합니다."""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY가 설정되지 않았습니다. "
            ".env.example을 .env로 복사한 뒤 API 키를 입력하세요."
        )
    return api_key


def get_llm(*, temperature: float = 0.0) -> ChatGoogleGenerativeAI:
    """Gemini 채팅 모델을 생성합니다."""
    require_api_key()
    model_name = os.getenv("GEMINI_MODEL", DEFAULT_CHAT_MODEL).strip()
    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_retries=2,
    )


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Few-shot 예제 선택에 사용할 Gemini 임베딩 모델을 생성합니다."""
    require_api_key()
    model_name = os.getenv(
        "GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL
    ).strip()
    return GoogleGenerativeAIEmbeddings(
        model=model_name,
        task_type="SEMANTIC_SIMILARITY",
    )


def content_to_text(content: Any) -> str:
    """Gemini 응답 content가 문자열 또는 블록 목록인 경우 모두 문자열로 변환합니다."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(str(text))
        return "".join(parts)
    return str(content)


def print_response(response: Any) -> None:
    """AIMessage 또는 문자열 결과를 보기 좋게 출력합니다."""
    content = getattr(response, "content", response)
    print(content_to_text(content))
