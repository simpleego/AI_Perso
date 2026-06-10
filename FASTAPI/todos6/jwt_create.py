import jwt
from datetime import datetime, timedelta, timezone

# 서명에 사용할 비밀키 설정
SECRET_KEY = "secret"

# 토큰에 담을 데이터 구성
payload = {
    "user_id": 10,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=10),
}

# 토큰 생성(헤더 + 페이로드 + 서명)
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
# 생성된 토큰 출력
print(token)