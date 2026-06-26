
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DB 접속한다.


# 접속할 DB 주소 설정
DATABASE_URL = "mysql+pymysql://simple:pjc0129@localhost:3306/fastapi_db"

# 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
# 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine,
)

