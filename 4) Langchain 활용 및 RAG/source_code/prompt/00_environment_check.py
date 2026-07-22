"""설치 패키지와 환경 변수를 점검합니다."""

import os
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

PACKAGES = [
    "langchain",
    "langchain-core",
    "langchain-google-genai",
    "python-dotenv",
    "pydantic",
]

print(f"Python: {sys.version.split()[0]}")
for package in PACKAGES:
    try:
        print(f"{package}: {version(package)}")
    except PackageNotFoundError:
        print(f"{package}: 설치되지 않음")

api_key = os.getenv("GOOGLE_API_KEY", "")
print("GOOGLE_API_KEY:", "설정됨" if api_key else "설정되지 않음")
print("GEMINI_MODEL:", os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"))
print(
    "GEMINI_EMBEDDING_MODEL:",
    os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"),
)
