"""
모든 실습 파일에서 공통으로 사용하는
Gemini 및 OpenAI 모델 초기화 모듈.
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


# 기본 모델
DEFAULT_GEMINI_MODEL = "gemini-2.5"
DEFAULT_OPENAI_MODEL = "gpt-4.1-mini"


def get_model(
    *,
    temperature: float = 0.0,
) -> ChatGoogleGenerativeAI:
    """
    Gemini 채팅 모델을 반환한다.

    기존 실습 파일과의 호환성을 위해
    get_model()은 Gemini 모델을 반환한다.
    """
    return get_gemini_model(temperature=temperature)


def get_gemini_model(
    *,
    temperature: float = 0.0,
) -> ChatGoogleGenerativeAI:
    """환경 변수에서 API 키를 읽어 Gemini 채팅 모델을 반환한다."""

    load_dotenv()

    # GOOGLE_API_KEY를 우선 사용하고,
    # 없으면 GEMINI_API_KEY를 사용한다.
    api_key = (
        os.getenv("GOOGLE_API_KEY")
        or os.getenv("GEMINI_API_KEY")
    )

    if not api_key:
        raise RuntimeError(
            "Gemini API Key가 없습니다.\n"
            ".env 파일에 다음과 같이 저장하세요.\n"
            "GOOGLE_API_KEY=발급받은_키"
        )

    # GEMINI_API_KEY만 설정한 경우에도
    # langchain-google-genai가 인식하도록 복사한다.
    os.environ.setdefault("GOOGLE_API_KEY", api_key)

    model_name = os.getenv(
        "GEMINI_MODEL",
        DEFAULT_GEMINI_MODEL,
    )

    return ChatGoogleGenerativeAI(
        model=model_name,
        temperature=temperature,
        max_retries=2,
    )


def get_openai_model(
    *,
    temperature: float = 0.0,
) -> ChatOpenAI:
    """환경 변수에서 API 키를 읽어 OpenAI GPT 모델을 반환한다."""

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OpenAI API Key가 없습니다.\n"
            ".env 파일에 다음과 같이 저장하세요.\n"
            "OPENAI_API_KEY=발급받은_키"
        )

    model_name = os.getenv(
        "OPENAI_MODEL",
        DEFAULT_OPENAI_MODEL,
    )

    return ChatOpenAI(
        model=model_name,
        api_key=api_key,
        temperature=temperature,
        max_retries=2,
    )


def get_chat_model(
    provider: str = "gemini",
    *,
    temperature: float = 0.0,
) -> ChatGoogleGenerativeAI | ChatOpenAI:
    """
    provider 값에 따라 Gemini 또는 OpenAI 모델을 반환한다.

    사용 가능한 provider:
    - gemini
    - google
    - openai
    - gpt
    """

    provider = provider.strip().lower()

    if provider in {"gemini", "google"}:
        return get_gemini_model(
            temperature=temperature,
        )

    if provider in {"openai", "gpt", "gpt4"}:
        return get_openai_model(
            temperature=temperature,
        )

    raise ValueError(
        f"지원하지 않는 모델 제공자입니다: {provider}\n"
        "사용 가능한 값: gemini, google, openai, gpt"
    )


def print_response(response: Any) -> None:
    """
    Gemini 및 OpenAI 응답에서 텍스트를 추출해 출력한다.
    """

    # 일부 모델 응답은 text 속성을 제공한다.
    text = getattr(response, "text", None)

    if isinstance(text, str) and text:
        print(text)
        return

    # 일반적인 LangChain AIMessage는 content를 사용한다.
    content = getattr(response, "content", None)

    if isinstance(content, str):
        print(content)
        return

    if isinstance(content, list):
        for item in content:
            if isinstance(item, str):
                print(item)
            elif isinstance(item, dict):
                item_text = item.get("text")
                if item_text:
                    print(item_text)
        return

    print(response)