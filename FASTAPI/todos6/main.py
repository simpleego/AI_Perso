from fastapi import FastAPI
from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(todo_router)
app.include_router(user_router)

app.add_middleware(
    SessionMiddleware,
    secret_key="your-secret-here"
)