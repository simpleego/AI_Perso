"""
1-6-3. 다양한 메모리 저장 방식 - (3) SQLite 데이터베이스
로컬 파일 DB 사용. 별도 서버 없이 SQL 기반 영구 저장 가능 (단일 서버 프로덕션에 적합)
"""
from langchain_community.chat_message_histories import SQLChatMessageHistory
from _chain import build_chain_with_history, demo_conversation


def get_sql_session_history(session_id: str):
    return SQLChatMessageHistory(
        session_id=session_id,
        connection="sqlite:///chat_history.db",  # 로컬 SQLite 파일 (자동 생성)
    )


if __name__ == "__main__":
    chain = build_chain_with_history(get_sql_session_history)
    demo_conversation(chain, "user_123")
    print("\n→ chat_history.db 파일에 대화가 저장되었습니다. (재실행해도 기억 유지)")
