from fastapi import HTTPException, APIRouter, Request, Depends
from sqlalchemy import select
from starlette import status

from database.db_connection import SessionFactory
from models import Todo
from schema.request import TodoCreateRequest, TodoUpdateRequest
from schema.response import TodoResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt import decode_access_token
router = APIRouter(tags=["Todo"])
bearer = HTTPBearer(auto_error=False)

# # 전체 할 일 조회(세션 방식)
# @router.get(
#     "/todos",
#     response_model=list[TodoResponse],
#     status_code=status.HTTP_200_OK
# )
# def get_todos_handler(request: Request):
#     user_id = request.session.get("user_id")
#     session = SessionFactory()
#     try:
#         stmt = select(Todo).where(Todo.user_id == user_id)
#         todos = session.execute(stmt).scalars().all()
#         return todos
#     finally:
#         session.close()
#
# # 단일 할 일 조회(세션 방식)
# @router.get(
#     "/todos/{todo_id}",
#     response_model=TodoResponse,
#     status_code=status.HTTP_200_OK
# )
# def get_todo_handler(request: Request, todo_id: int):
#     user_id = request.session.get("user_id")
#     session = SessionFactory()
#     try:
#         stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
#         todo = session.execute(stmt).scalars().first()
#         if todo:
#             return todo
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Todo not found"
#         )
#     finally:
#         session.close()
#
# # 할 일 생성(세션 방식)
# @router.post(
#     "/todos",
#     response_model=TodoResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_todo_handler(request: Request, body: TodoCreateRequest):
#     user_id = request.session.get("user_id")
#     session = SessionFactory()
#     try:
#         todo = Todo(
#             title=body.title,
#             is_done=body.is_done,
#             user_id=user_id,
#         )
#         session.add(todo)
#         session.commit()
#         return todo
#     finally:
#         session.close()
#
# # 할 일 수정(세션 방식)
# @router.patch(
#     "/todos/{todo_id}",
#     response_model=TodoResponse,
#     status_code=status.HTTP_200_OK
# )
# def update_todo_handler(request: Request, todo_id: int, body: TodoUpdateRequest):
#     user_id = request.session.get("user_id")
#     session = SessionFactory()
#     try:
#         stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
#         todo = session.execute(stmt).scalars().first()
#         if todo:
#             if body.title is not None:
#                 todo.title = body.title
#             if body.is_done is not None:
#                 todo.is_done = body.is_done
#             session.commit()
#             return todo
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Todo not found"
#         )
#     finally:
#         session.close()
#
# # 할 일 삭제(세션 방식)
# @router.delete(
#     "/todos/{todo_id}",
#     status_code=status.HTTP_204_NO_CONTENT
# )
# def delete_todo_handler(request: Request, todo_id: int):
#     user_id = request.session.get("user_id")
#     session = SessionFactory()
#     try:
#         stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
#         todo = session.execute(stmt).scalars().first()
#         if todo:
#             session.delete(todo)
#             session.commit()
#             return
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Todo not found"
#         )
#     finally:
#         session.close()

# 전체 할 일 조회(JWT 방식)
@router.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK
)
def get_todos_handler(
    authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        token = authorization.credentials
        user_id = decode_access_token(token)
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.user_id == user_id)
        todos = session.execute(stmt).scalars().all()
        return todos
    finally:
        session.close()

# 단일 할 일 조회(JWT 방식)
@router.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def get_todo_handler(
    todo_id: int,
    authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    finally:
        session.close()

# 할 일 생성(JWT 방식)
@router.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(
    body: TodoCreateRequest,
    authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    session = SessionFactory()
    try:
        todo = Todo(
            title=body.title,
            is_done=body.is_done,
            user_id=user_id,
        )
        session.add(todo)
        session.commit()
        return todo
    finally:
        session.close()

# 할 일 수정(JWT 방식)
@router.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def update_todo_handler(
    todo_id: int,
    body: TodoUpdateRequest,
    authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
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

# 할 일 삭제(JWT 방식)
@router.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(
    todo_id: int,
    authorization: HTTPAuthorizationCredentials | None = Depends(bearer)
):
    user_id = None
    if authorization:
        access_token = authorization.credentials
        user_id = decode_access_token(access_token)
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
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
