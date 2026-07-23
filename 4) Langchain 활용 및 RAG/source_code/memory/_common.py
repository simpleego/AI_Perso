"""공통 설정: .env에서 GOOGLE_API_KEY 로드 및 Gemini 모델 초기화"""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()  # .env 파일에서 GOOGLE_API_KEY 로드

# 무료 API 키로 사용 가능한 Gemini 모델 문자열 (create_agent에도 그대로 사용 가능)
GEMINI_MODEL = "google_genai:gemini-2.5-flash"


def check_api_key():
    """API 키 미설정 시 친절한 안내 후 종료"""
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit(
            "[오류] GOOGLE_API_KEY가 설정되지 않았습니다.\n"
            "1) https://aistudio.google.com/apikey 에서 무료 키 발급\n"
            "2) .env 파일에 GOOGLE_API_KEY=발급받은키 추가"
        )


def get_llm(temperature: float = 0):
    """무료 API 키로 사용 가능한 Gemini 채팅 모델 반환"""
    check_api_key()
    return init_chat_model(GEMINI_MODEL, temperature=temperature)
