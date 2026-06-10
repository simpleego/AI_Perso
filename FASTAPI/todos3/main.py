from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# 할 일 저장
todos = [
    {"id": 1, "title": "FastAPI 공부하기", "is_done": False},
    {"id": 2, "title": "운동하기", "is_done": True},
    {"id": 3, "title": "책 읽기", "is_done": False},
]

# 전체 할 일 조회
@app.get(
    "/todos",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK
)
def get_todos_handler():
    return todos

# 단일 할 일 조회
@app.get(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def get_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# 할 일 생성
@app.post(
    "/todos",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(body: TodoCreateRequest):
    new_todo = {
        "id": len(todos) + 1,
        "title": body.title,
        "is_done": body.is_done,
    }
    todos.append(new_todo)
    return new_todo

# 할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos:
        if todo["id"] == todo_id:
            if body.title is not None:
                todo["title"] = body.title
            if body.is_done is not None:
                todo["is_done"] = body.is_done
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# 할 일 삭제
@app.delete(
    "/todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
