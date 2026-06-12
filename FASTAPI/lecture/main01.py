from fastapi import FastAPI

app = FastAPI()


@app.get("/") # url 매핑 : 어떤 요청("/")이 들어오면 해당 함수를 수행한다.
async def root():
    return [{"메시지1": "안녕 친구야1"},
            {"메시지2": "안녕 친구야2"}]

@app.get("/hi") # url 매핑 : 어떤 요청("/hi")이 들어오면 해당 함수를 수행한다.
async def hi():
    # 해당 기능을 수행
    return {"메시지1": "안녕 잘지냈어?"}

# @app.get("/100") # url 매핑 : 어떤 요청("/hi")이 들어오면 해당 함수를 수행한다.
# async def hi100():
#     # 100번 인사하기

#     return ["안녕 하세요"]*100

@app.get("/100")
async def hi100():
    # 100번 인사하기
    message_list=[]

    for _ in range(100):
        message_list.append("안녕 하세요~~")

    return message_list

@app.get("/login")
def login():
    # 로그인 화면을 호출

    return "로그인 화면을 호출"

@app.post("/login")
def login():
    # 로그인 기능
    # 아이디와 비번을 확인한다.
    # DB에 저장된 id와 비번을 조회해서 가져오기    

    return "쇼핑몰에 오신 걸 환영합니다."

@app.get("/users/{user_id}")
def read_user_handler(user_id: str):
    # 로그인 기능
    # 아이디와 비번을 확인한다.
    # DB에 저장된 id와 비번을 조회해서 가져오기    

    return {"user_id" : user_id, "message": f"사용자 {user_id} 정보 조회"}