from datetime import datetime
from pydantic import BaseModel

# 할 일 응답 모델
class TodoResponse(BaseModel):
    id: int 
    title: str
    is_done: bool
    user_id: int | None

# 회원가입 응답 모델
class UserSignUpResponse(BaseModel):
    id: int
    email: str
    created_at: datetime