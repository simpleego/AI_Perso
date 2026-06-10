from fastapi import FastAPI
from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(todo_router)
app.include_router(user_router)
