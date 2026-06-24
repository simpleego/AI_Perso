# jwt 토큰 비밀키 생성
> `SECRET_KEY`는 JWT(JSON Web Token)의 **무결성을 검증하고 서명(Signature)을 생성할 때 사용하는 가장 중요한 열쇠**입니다.
> 개발 단계나 연습용으로는 코드처럼 `"secret"` 같은 단순한 문자열을 사용하기도 하지만, **실제 서비스(운영 환경)에서는 해커가 무차별 대입 공격(Brute-force)으로 알아낼 수 없도록 절대 유추할 수 없는 강력한 무작위 문자열**을 사용해야 합니다.

실제 운영 환경에서 안전한 `SECRET_KEY`를 생성하고 관리하는 구체적인 방법을 정리해 드릴게요.

---

## 1. 안전한 실제 값(문자열)을 생성하는 방법

보안 표준을 만족하는 무작위 문자열은 파이썬 내장 라이브러리인 `secrets`나 `uuid` 등을 이용해 터미널(콘솔)에서 쉽게 한 줄로 생성할 수 있습니다.

가장 추천하는 방법은 **암호학적으로 안전한 무작위 바이트를 생성한 뒤 16진수(Hex)나 Base64 문자열로 변환**하는 것입니다.

### 방법 A: `secrets` 모듈 사용 (가장 권장)

파이썬 3.6부터 지원하는 `secrets` 모듈은 암호학적으로 안전한 비밀값을 생성해 줍니다. 터미널을 열고 아래 명령어를 입력해 보세요.

```bash
python -c "import secrets; print(secrets.token_hex(32))"

```

* **결과 예시:** `4f9e1a3b8c7d6e5f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f`
* 32바이트의 무작위 데이터를 16진수로 표현하여 **64글자의 강력한 문자열**이 생성됩니다. (JWT의 HS256 알고리즘은 최소 256비트/32바이트 이상의 키를 권장합니다.)

### 방법 B: `openssl` 명령어 사용 (터미널 전용)

파이썬을 켜지 않고 맥(Mac)이나 리눅스 터미널에서 바로 생성할 수도 있습니다.

```bash
openssl rand -hex 32

```

---

## 2. 생성한 비밀키를 실제 코드에 적용하는 올바른 방법

코드에 `SECRET_KEY = "4f9e1a3b8c7d..."` 처럼 실제 값을 직접 적어두는 것(하드코딩)은 대단히 위험합니다. 코드가 GitHub 같은 곳에 실수로 공개되면 보안이 완전히 무너지기 때문입니다.

따라서 실제 서비스에서는 환경 변수(Environment Variable)에 저장해 두고 소스코드에서 불러오는 방식을 사용합니다.

### Step 1: `.env` 파일 만들기

프로젝트 루트 디렉토리에 `.env` 파일을 만들고, 생성한 비밀키를 저장합니다.

```env
# .env 파일 예시
JWT_SECRET_KEY=4f9e1a3b8c7d6e5f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f

```

*(주의: 이 `.env` 파일은 절대 Git에 업로드하지 않도록 `.gitignore`에 등록해야 합니다.)*

### Step 2: 파이썬 코드에서 불러오기

`python-dotenv` 라이브러리를 사용하면 `.env` 파일을 읽어올 수 있습니다. (설치: `pip install python-dotenv`)

```python
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

# .env 파일의 환경 변수 로드
load_dotenv()

# 환경 변수에서 비밀키 읽어오기 (없으면 기본값 사용하거나 에러 처리)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY가 환경 변수 설정에 없습니다!")

# 토큰 데이터 구성
payload = {
    "user_id": 10,
    "exp": datetime.now(timezone.utc) + timedelta(minutes=10)
}

# 안전하게 불러온 비밀키로 토큰 생성
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(token)

```

---

## 요약

* **실제값은 어떻게 만드나요?** 터미널에서 `python -c "import secrets; print(secrets.token_hex(32))"` 코드를 실행해 유추 불가능한 64글자 무작위 문자열을 생성합니다.
* **어떻게 관리하나요?** 코드에 직접 적지 말고 `.env` 파일이나 운영체제 환경 변수에 숨겨두고 `os.getenv()`로 불러와 사용합니다.
