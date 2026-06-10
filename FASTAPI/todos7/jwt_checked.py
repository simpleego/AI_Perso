import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "secret"
BAD_SECRET = "wrong-secret"

payload = {
    "user_id": 10,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=1),
}

# 정상적인 비밀키로 토큰 생성
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("token:", token)

# 정상적인 비밀키로 검증
decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
print("Ok:", decoded)

# 잘못된 비밀키로 검증(서명 불일치)
try:
    jwt.decode(token, BAD_SECRET, algorithms=["HS256"])
except jwt.InvalidSignatureError:
    print("Signature 검증 실패: 잘못된 secret")