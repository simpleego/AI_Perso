"""멀티 에이전트 실습 공통 함수."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


def get_model():
    """환경변수를 읽어 Gemini 채팅 모델을 초기화합니다."""
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(
            "GOOGLE_API_KEY가 없습니다. "
            ".env.example을 .env로 복사하고 실제 키를 입력하세요."
        )

    model_name = os.getenv(
        "MODEL_NAME", "google_genai:gemini-2.5-flash-lite"
    )
    return init_chat_model(model_name, temperature=0)


def final_text(result: dict) -> str:
    """create_agent 실행 결과에서 마지막 답변을 꺼냅니다."""
    return str(result["messages"][-1].content)


def ask(agent, question: str) -> str:
    """에이전트에 한 번 질문하고 텍스트 답변을 반환합니다."""
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    return final_text(result)

