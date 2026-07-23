"""
1-6-3. 다양한 메모리 저장 방식 - (2) 파일 기반 저장소
대화 히스토리를 세션별 JSON 파일로 저장. 재실행해도 기억이 유지됨.
[주의] 단일 서버 환경 권장, 동시 접근 시 파일 잠금 문제 가능
"""
import os
from langchain_community.chat_message_histories import FileChatMessageHistory
from _chain import build_chain_with_history, demo_conversation

# chat_histories/ 디렉토리가 미리 존재해야 함 (핵심 주의사항)
os.makedirs("chat_histories", exist_ok=True)


def get_file_session_history(session_id: str):
    # 세션ID별로 별도의 JSON 파일 생성
    return FileChatMessageHistory(f"chat_histories/{session_id}.json")


if __name__ == "__main__":
    chain = build_chain_with_history(get_file_session_history)
    demo_conversation(chain, "user_123")
    print("\n→ chat_histories/user_123.json 파일을 열어 저장 내용을 확인해보세요.")
    print("→ 스크립트를 다시 실행해도 이전 대화를 기억합니다. (영구 저장)")
