"""설치 상태, API 키, 선택 모델을 점검하는 예제."""

from importlib.metadata import version
import os

from dotenv import load_dotenv

load_dotenv()

packages = ["langchain", "langchain-google-genai", "langgraph"]

print("[패키지 버전]")
for package in packages:
    try:
        print(f"- {package}: {version(package)}")
    except Exception as exc:
        print(f"- {package}: 확인 실패 ({exc})")

api_key = os.getenv("GOOGLE_API_KEY", "").strip()
print("\n[환경 변수]")
print("- GOOGLE_API_KEY:", "설정됨" if api_key and api_key != "여기에_API_KEY_입력" else "설정 필요")
print("- GEMINI_MODEL:", os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
