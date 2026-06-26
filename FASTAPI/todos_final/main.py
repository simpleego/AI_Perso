from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)  # 테이블 생성 지시

app = FastAPI()

# CORS 설정 (클라이언트(HTML/JS)와 포트가 다를 때 발생할 수 있는 오류 방지)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], # 프론트엔드 주소 (실제 도메인/포트)
    allow_credentials=True,                 # 쿠키/세션 사용 시 필수
    allow_methods=["*"],                    # 모든 HTTP 메서드 허용
    allow_headers=["*"],
)

app.include_router(todo_router)
app.include_router(user_router)

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-here"
)