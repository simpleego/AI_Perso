from pydantic import BaseModel

# 할 일 응답 모델
class TodoRequest(BaseModel):
    id: int
    title: str
    is_done: bool


# 할 일 수정 요청 모델
class TodoUpdateRequest(BaseModel):
    title: str | None = None
    is_done: bool | None = None
