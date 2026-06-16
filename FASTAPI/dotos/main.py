from schema.response import TodoResponse
from schema.request import TodoRequest, TodoUpdateRequest
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS 설정 (클라이언트(HTML/JS)와 포트가 다를 때 발생할 수 있는 오류 방지)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],
)

"""
 파이썬 설명문
 
"""


# 할 일 저장
# DB서버 또는 AI API를 이용한 결과로 받는 값들
todos = [
    {"id":1, "title":"FastAPI 공부하기", "is_done": False},
    {"id":2, "title":"운동하기", "is_done": True},
    {"id":3, "title":"책읽기 ", "is_done": False},
    {"id":4, "title":"영상녹화 하기 ", "is_done": False},
    {"id":5, "title":"AI모델 생성 ", "is_done": False},
]

# 전체 할 일 조회
@app.get("/todos",
         response_model=list[TodoResponse],
         status_code=status.HTTP_200_OK)
def root():
    # 서버 root 요청 처리
    return todos

# 할 일 조회(한개의 할 일)
@app.get("/todos/{todo_id}",
         response_model=TodoResponse,
         status_code=status.HTTP_200_OK)
def get_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    # print("not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

# 할 일 생성(Create)
@app.post(
    "/todos",
    response_model=TodoResponse,    
    status_code=status.HTTP_201_CREATED)

def create_todo_handler(body: TodoRequest):
    new_todo = {
        "id": len(todos)+1, # 아이디 자동증가로 생성
        "title": body.title,
        "is_done": body.is_done,
    }

    todos.append(new_todo)
    return new_todo

# 할 일 수정(PUT(전체수정)/PATCH(부분수정): 데이터 수정)
@app.patch(
    "/todos/{todo_id}",
    response_model = TodoResponse,    
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos:
        if todo["id"] == todo_id:
            if body.title is not None:
                todo["id"] = body.title
            
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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found for delete")