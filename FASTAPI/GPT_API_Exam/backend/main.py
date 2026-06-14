from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

app = FastAPI()

# 프론트엔드 주소 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션별 대화 기록 저장소
# 실제 서비스에서는 Redis, DB 사용 권장
session_store: Dict[str, List[dict]] = {}


class ChatRequest(BaseModel):
    message: str


def get_or_create_session_id(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax",
        )

    if session_id not in session_store:
        session_store[session_id] = []

    return session_id


def fake_ai_model(message: str, history: List[dict]) -> str:
    """
    실제 AI 모델 호출 위치
    예: Qwen, LLaMA, OpenAI API, Ollama 등으로 교체 가능
    """
    return f"AI 응답: '{message}'라고 말씀하셨습니다. 현재 대화 수는 {len(history) + 1}개입니다."

def call_gpt_model(history: List[dict]) -> str:
    """
    실제 GPT API 호출 함수
    OpenAI API 키는 .env의 OPENAI_API_KEY를 사용
    """

    messages = [
        {
            "role": "system",
            "content": "너는 친절한 한국어 AI assistant야. 답변은 간단하고 명확하게 해줘."
        }
    ]

    messages.extend(history)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )

    return response.choices[0].message.content

@app.post("/chat")
def chat(request: Request, response: Response, data: ChatRequest):
    session_id = get_or_create_session_id(request, response)

    history = session_store[session_id]

    user_message = {
        "role": "user",
        "content": data.message
    }
    history.append(user_message)

    # ai_answer = fake_ai_model(data.message, history)
    ai_answer = call_gpt_model(history)

    ai_message = {
        "role": "assistant",
        "content": ai_answer
    }
    history.append(ai_message)

    return {
        "session_id": session_id,
        "answer": ai_answer,
        "history": history
    }


@app.get("/history")
def get_history(request: Request, response: Response):
    session_id = get_or_create_session_id(request, response)

    return {
        "session_id": session_id,
        "history": session_store[session_id]
    }


@app.post("/reset")
def reset_session(request: Request, response: Response):
    session_id = get_or_create_session_id(request, response)
    session_store[session_id] = []

    return {
        "message": "세션 대화 기록이 초기화되었습니다.",
        "session_id": session_id
    }