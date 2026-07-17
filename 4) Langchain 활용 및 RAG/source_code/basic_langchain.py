import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_openai_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일 또는 시스템 환경 변수에 키를 추가하세요."
        )
    return api_key


def main() -> None:
    api_key = get_openai_api_key()
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=api_key,
    )

    try:
        response = llm.invoke("LangChain v1.0의 주요 장점 3가지를 알려주세요.")
        print("[OK] 설치 및 설정 완료")
        print(f"\n응답:\n{response.content}")
    except Exception as e:
        print(f"[ERROR] 오류 발생: {e}")


if __name__ == "__main__":
    main()
