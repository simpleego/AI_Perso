"""
1-6-3. 다양한 메모리 저장 방식 - (5) PostgreSQL 저장소
프로덕션 환경에서 안정적인 영구 저장이 필요할 때 사용.
[사전 준비] pip install psycopg2-binary + PostgreSQL 서버 및 chatdb 데이터베이스
"""
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from _chain import build_chain_with_history, demo_conversation


def get_postgres_session_history(session_id: str):
    return PostgresChatMessageHistory(
        session_id=session_id,
        connection_string="postgresql://user:password@localhost:5432/chatdb",  # 환경에 맞게 수정
    )


if __name__ == "__main__":
    try:
        chain = build_chain_with_history(get_postgres_session_history)
        demo_conversation(chain, "user_123")
    except Exception as e:
        print("[안내] PostgreSQL에 연결할 수 없습니다. 접속 정보를 확인 후 다시 시도하세요.")
        print("에러:", e)
