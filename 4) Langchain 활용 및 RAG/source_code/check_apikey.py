import os
import sys

# Windows 콘솔에서 UTF-8 출력을 강제 설정
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    print("[WARN] python-dotenv 미설치: .env 파일을 로드하지 않습니다.")

# 환경 변수 확인
print("[OK] API 키 설정됨" if os.getenv("OPENAI_API_KEY") else "[ERROR] API 키 미설정")
