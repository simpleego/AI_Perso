import base64
import json

# 토큰 문자열 입력
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMCwiZXhwIjoxNzY5MzIwMjkxfQ.EeuzgLlDQW3Sm7WTvmwEXT2ZVfKiqPgE_K7ZKZIweWY"

# 토큰 문자열 분리
header_b64, payload_b64, _ = token.split(".")

# Base64 디코딩 함수 정의
def decode(b64: str):
    padded = b64 + "=" * (-len(b64) % 4)
    decoded = base64.urlsafe_b64decode(padded)
    return json.loads(decoded)

# 헤더와 페이로드 디코딩
header = decode(header_b64)
payload = decode(payload_b64)

print("Header:", header)
print("Payload:", payload)