from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 설정)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# ChatOpenAI 모델 초기화 (v1.0 API)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)

# 간단한 테스트
try:
    response = llm.invoke("LangChain v1.0의 주요 장점 3가지를 알려주세요.")
    print("[OK] 설치 및 설정 완료")
    print(f"\n응답:\n{response.content}")
except Exception as e:
    print(f"[ERROR] 오류 발생: {e}")