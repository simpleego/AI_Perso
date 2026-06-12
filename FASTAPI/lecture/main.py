from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정 (클라이언트(HTML/JS)와 포트가 다를 때 발생할 수 있는 오류 방지)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],
)

# 요청 데이터 모델 정의
class MathRequest(BaseModel):
    num1: int
    num2: int

# 단일 메서드에서 모든 연산자 처리
@app.post("/calculate/{operator}")
def calculate(operator: str, data: MathRequest):
    num1 = data.num1
    num2 = data.num2
    
    result = 0
    
    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "x":  # 'x' 문자로 곱셈 처리
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            raise HTTPException(status_code=400, detail="0으로 나눌 수 없습니다.")
        result = num1 / num2
    else:
        raise HTTPException(status_code=400, detail="유효하지 않은 연산자입니다.")
        
    return {
        "num1": num1,
        "num2": num2,
        "operator": operator,
        "result": result
    }
