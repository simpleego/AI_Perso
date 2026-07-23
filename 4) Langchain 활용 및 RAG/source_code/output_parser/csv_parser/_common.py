"""공통 설정: .env에서 GOOGLE_API_KEY 로드 및 Gemini 모델 초기화"""
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()  # .env 파일에서 환경 변수 로드


def check_api_key():
    """API 키가 설정되어 있는지 확인"""
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit(
            "[오류] GOOGLE_API_KEY가 설정되지 않았습니다.\n"
            "1) https://aistudio.google.com/apikey 에서 무료 키 발급\n"
            "2) .env 파일에 GOOGLE_API_KEY=발급받은키 추가"
        )


def get_llm(temperature: float = 0):
    """무료 API 키로 사용 가능한 Gemini 모델 반환"""
    check_api_key()
    return init_chat_model("google_genai:gemini-2.5-flash", temperature=temperature)
