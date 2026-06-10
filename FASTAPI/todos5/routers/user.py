from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select
from schema.request import UserSignUpRequest
from database.db_connection import SessionFactory
from models import User
from auth.password import hash_password
from schema.response import UserSignUpResponse
router = APIRouter(tags=["User"])

# 회원가입
@router.post(
    "/users/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSignUpResponse
)
def signup_user_handler(body: UserSignUpRequest): # 요청 데이터 검증
    # 이메일 중복 검사
    with SessionFactory() as session:
        stmt = select(User).where(User.email == body.email)
        existing_user = session.scalar(stmt)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다."
            )
        # 비밀번호 해시 생성
        hashed_password = hash_password(body.password)
        # User 모델 생성 후 DB 저장
        user = User(
            email=str(body.email),
            hashed_password=hashed_password,
        )
        session.add(user)
        session.commit()
        # 응답 반환
        session.refresh(user)
        return user