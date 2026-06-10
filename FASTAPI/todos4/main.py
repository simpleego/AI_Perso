from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import select
from database.db_connection import engine, SessionFactory
from database.orm import Base
from models import Todo

Base.metadata.create_all(bind=engine)
app = FastAPI()

# # 할 일 저장
# todos = [
#     {"id": 1, "title": "FastAPI 공부하기", "is_done": False},
#     {"id": 2, "title": "운동하기", "is_done": True},
#     {"id": 3, "title": "책 읽기", "is_done": False},
# ]

# 전체 할 일 조회
@app.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK
)
def get_todos_handler():
    session = SessionFactory()
    try:
        stmt = select(Todo)
        todos = session.execute(stmt).scalars().all()
        return todos
    finally:
        session.close()

# 단일 할 일 조회
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def get_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    finally:
        session.close()

# 할 일 생성
@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(body: TodoCreateRequest):
    session = SessionFactory()
    try:
        todo = Todo(
            title=body.title,
            is_done=body.is_done,
        )
        session.add(todo)
        session.commit()
        return todo
    finally:
        session.close()

# 할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            if body.title is not None:
                todo.title = body.title
            if body.is_done is not None:
                todo.is_done = body.is_done
            session.commit()
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    finally:
        session.close()

# 할 일 삭제
@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            session.delete(todo)
            session.commit()
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    finally:
        session.close()
