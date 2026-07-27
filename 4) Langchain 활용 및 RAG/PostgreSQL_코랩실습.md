Google Colab에서 `PostgresStore`를 사용하려면 다음 세 가지가 필요합니다.

1. Colab 런타임에 PostgreSQL 서버 설치 및 실행
2. LangGraph PostgreSQL 패키지와 `psycopg` 드라이버 설치
3. 데이터베이스와 사용자를 만든 후 `PostgresStore.setup()` 실행

`PostgresStore`는 LangGraph의 **장기 메모리 Store**입니다. 그래프 실행 상태를 저장하는 `PostgresSaver`와는 용도가 다릅니다. `PostgresStore`는 사용자 설정, 선호도, 장기 기억 같은 데이터를 키-값 형태로 저장합니다. ([LangChain Reference][1])

---

# 1. 필수 패키지 설치

Colab 첫 번째 셀에서 실행합니다.

```python
!apt-get update -qq
!apt-get install -y postgresql postgresql-contrib

!pip install -qU \
    langgraph \
    langgraph-checkpoint-postgres \
    "psycopg[binary]" \
    psycopg-pool
```

`langgraph-checkpoint-postgres`는 기본적으로 Psycopg 3을 사용합니다. Colab에서는 컴파일 문제를 피하기 위해 `"psycopg[binary]"`를 함께 설치하는 것이 편리합니다. ([PyPI][2])

설치 후 버전을 확인합니다.

```python
import langgraph
import psycopg

print("psycopg version:", psycopg.__version__)
```

패키지 설치 후 import 오류가 발생하면 Colab 메뉴에서 다음을 실행합니다.

```text
런타임 → 세션 다시 시작
```

---

# 2. PostgreSQL 서버 실행

```python
!service postgresql start
!service postgresql status
```

정상적으로 실행되면 다음과 비슷한 메시지가 표시됩니다.

```text
PostgreSQL is running
```

프로세스로 확인할 수도 있습니다.

```python
!pg_isready
```

정상 출력 예시:

```text
/var/run/postgresql:5432 - accepting connections
```

---

# 3. PostgreSQL 사용자와 데이터베이스 생성

예제에서는 다음 정보를 사용하겠습니다.

| 항목     | 설정값              |
| ------ | ---------------- |
| 사용자    | `langgraph_user` |
| 비밀번호   | `langgraph_pass` |
| 데이터베이스 | `langgraph_db`   |
| 호스트    | `localhost`      |
| 포트     | `5432`           |

다음 셀을 실행합니다.

```python
!sudo -u postgres psql -c "CREATE USER langgraph_user WITH PASSWORD 'langgraph_pass';"
!sudo -u postgres psql -c "CREATE DATABASE langgraph_db OWNER langgraph_user;"
!sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE langgraph_db TO langgraph_user;"
```

이미 실행해서 사용자나 데이터베이스가 존재하면 다음과 같은 오류가 발생할 수 있습니다.

```text
role "langgraph_user" already exists
database "langgraph_db" already exists
```

이 경우 다시 생성할 필요는 없습니다.

## 반복 실행 가능한 생성 코드

Colab 셀을 여러 번 실행할 가능성이 있다면 다음 방식을 권장합니다.

```python
import subprocess

def run_sql_as_postgres(sql: str) -> None:
    result = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-tAc", sql],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

# 사용자 존재 여부 확인
result = subprocess.run(
    [
        "sudo", "-u", "postgres", "psql",
        "-tAc",
        "SELECT 1 FROM pg_roles WHERE rolname='langgraph_user';",
    ],
    capture_output=True,
    text=True,
    check=True,
)

if result.stdout.strip() != "1":
    run_sql_as_postgres(
        "CREATE USER langgraph_user WITH PASSWORD 'langgraph_pass';"
    )
    print("사용자를 생성했습니다.")
else:
    print("사용자가 이미 존재합니다.")

# 데이터베이스 존재 여부 확인
result = subprocess.run(
    [
        "sudo", "-u", "postgres", "psql",
        "-tAc",
        "SELECT 1 FROM pg_database WHERE datname='langgraph_db';",
    ],
    capture_output=True,
    text=True,
    check=True,
)

if result.stdout.strip() != "1":
    run_sql_as_postgres(
        "CREATE DATABASE langgraph_db OWNER langgraph_user;"
    )
    print("데이터베이스를 생성했습니다.")
else:
    print("데이터베이스가 이미 존재합니다.")
```

---

# 4. 연결 테스트

먼저 LangGraph를 연결하기 전에 `psycopg`만으로 연결을 테스트합니다.

```python
import psycopg

DB_URI = (
    "postgresql://langgraph_user:"
    "langgraph_pass@localhost:5432/langgraph_db"
)

try:
    with psycopg.connect(DB_URI) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]

    print("PostgreSQL 연결 성공")
    print(version)

except Exception as e:
    print("PostgreSQL 연결 실패")
    print(type(e).__name__, e)
```

연결이 성공해야 `PostgresStore`도 사용할 수 있습니다.

---

# 5. PostgresStore 생성 및 초기화

사용자가 제시한 코드는 다음과 같습니다.

```python
store = PostgresStore.from_conn_string(
    "postgresql://user:pass@localhost/dbname"
)
```

현재 사용 환경에서는 다음처럼 수정하는 것이 안전합니다.

```python
from langgraph.store.postgres import PostgresStore

DB_URI = (
    "postgresql://langgraph_user:"
    "langgraph_pass@localhost:5432/langgraph_db"
)

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    print("PostgresStore 초기화 완료")
```

`setup()`은 LangGraph Store가 사용할 테이블과 마이그레이션 정보를 생성합니다. 최초 사용 전에 반드시 한 번 실행해야 합니다. 공식 API와 예제에서도 `from_conn_string()` 컨텍스트 매니저와 `setup()` 사용 방식을 제공합니다. ([LangChain Reference][1])

---

# 6. 데이터 저장과 조회

`PostgresStore`는 다음 세 가지 구조를 사용합니다.

```text
namespace + key + value
```

예를 들어 사용자 `user_001`의 환경설정을 저장해 보겠습니다.

```python
from langgraph.store.postgres import PostgresStore

DB_URI = (
    "postgresql://langgraph_user:"
    "langgraph_pass@localhost:5432/langgraph_db"
)

with PostgresStore.from_conn_string(DB_URI) as store:
    # setup()은 최초 한 번만 필요하지만,
    # 실습에서는 반복 실행해도 안전하게 구성할 수 있습니다.
    store.setup()

    namespace = ("users", "user_001")

    store.put(
        namespace,
        "preferences",
        {
            "language": "ko",
            "theme": "dark",
            "difficulty": "beginner",
        },
    )

    item = store.get(namespace, "preferences")

    if item:
        print("저장된 값:", item.value)
    else:
        print("데이터가 없습니다.")
```

실행 결과:

```python
저장된 값: {
    'language': 'ko',
    'theme': 'dark',
    'difficulty': 'beginner'
}
```

공식적인 기본 사용 패턴도 `put(namespace, key, value)`와 `get(namespace, key)` 형식입니다. ([GitHub][3])

---

# 7. 전체 실행 코드

다음은 Colab에서 한 번에 실습할 수 있도록 정리한 코드입니다.

## 셀 1: 패키지 설치

```python
!apt-get update -qq
!apt-get install -y postgresql postgresql-contrib

!pip install -qU \
    langgraph \
    langgraph-checkpoint-postgres \
    "psycopg[binary]" \
    psycopg-pool
```

## 셀 2: PostgreSQL 시작

```python
!service postgresql start
!pg_isready
```

## 셀 3: 사용자와 데이터베이스 생성

```python
import subprocess

POSTGRES_USER = "langgraph_user"
POSTGRES_PASSWORD = "langgraph_pass"
POSTGRES_DB = "langgraph_db"


def execute_postgres_sql(sql: str) -> str:
    result = subprocess.run(
        ["sudo", "-u", "postgres", "psql", "-tAc", sql],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


user_exists = execute_postgres_sql(
    f"SELECT 1 FROM pg_roles WHERE rolname='{POSTGRES_USER}';"
)

if user_exists != "1":
    execute_postgres_sql(
        f"CREATE USER {POSTGRES_USER} "
        f"WITH PASSWORD '{POSTGRES_PASSWORD}';"
    )
    print("PostgreSQL 사용자를 생성했습니다.")
else:
    print("PostgreSQL 사용자가 이미 존재합니다.")


db_exists = execute_postgres_sql(
    f"SELECT 1 FROM pg_database WHERE datname='{POSTGRES_DB}';"
)

if db_exists != "1":
    execute_postgres_sql(
        f"CREATE DATABASE {POSTGRES_DB} OWNER {POSTGRES_USER};"
    )
    print("PostgreSQL 데이터베이스를 생성했습니다.")
else:
    print("PostgreSQL 데이터베이스가 이미 존재합니다.")
```

## 셀 4: PostgresStore 사용

```python
from langgraph.store.postgres import PostgresStore

POSTGRES_USER = "langgraph_user"
POSTGRES_PASSWORD = "langgraph_pass"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_DB = "langgraph_db"

DB_URI = (
    f"postgresql://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/"
    f"{POSTGRES_DB}"
)

namespace = ("users", "user_001")

with PostgresStore.from_conn_string(DB_URI) as store:
    # 최초 실행 시 필요한 테이블 생성
    store.setup()

    # 데이터 저장
    store.put(
        namespace,
        "profile",
        {
            "name": "심플",
            "language": "ko",
            "learning_level": "beginner",
        },
    )

    # 데이터 조회
    item = store.get(namespace, "profile")

    if item is None:
        print("저장된 데이터가 없습니다.")
    else:
        print("조회 결과")
        print(item.value)
```

---

# 8. 여러 데이터 저장 및 검색

```python
from langgraph.store.postgres import PostgresStore

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    namespace = ("users", "user_001", "memories")

    store.put(
        namespace,
        "memory_001",
        {
            "content": "사용자는 초보자 수준의 설명을 선호한다.",
            "category": "preference",
        },
    )

    store.put(
        namespace,
        "memory_002",
        {
            "content": "사용자는 Google Colab을 주로 사용한다.",
            "category": "environment",
        },
    )

    store.put(
        namespace,
        "memory_003",
        {
            "content": "사용자는 LangChain 강의를 준비하고 있다.",
            "category": "work",
        },
    )

    results = store.search(namespace)

    for result in results:
        print("key:", result.key)
        print("value:", result.value)
        print("-" * 50)
```

---

# 9. 데이터 수정과 삭제

## 수정

같은 namespace와 key로 다시 `put()`하면 값이 갱신됩니다.

```python
with PostgresStore.from_conn_string(DB_URI) as store:
    namespace = ("users", "user_001")

    store.put(
        namespace,
        "profile",
        {
            "name": "심플",
            "language": "ko",
            "learning_level": "intermediate",
        },
    )

    updated_item = store.get(namespace, "profile")
    print(updated_item.value)
```

## 삭제

```python
with PostgresStore.from_conn_string(DB_URI) as store:
    namespace = ("users", "user_001")

    store.delete(namespace, "profile")

    deleted_item = store.get(namespace, "profile")
    print(deleted_item)
```

결과:

```text
None
```

---

# 10. LangGraph 그래프에 Store 연결

`PostgresStore`는 그래프를 컴파일할 때 `store` 인수로 전달합니다.

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.store.base import BaseStore
from langgraph.store.postgres import PostgresStore
from langchain_core.runnables import RunnableConfig


class State(TypedDict):
    message: str
    result: str


def memory_node(
    state: State,
    config: RunnableConfig,
    *,
    store: BaseStore,
) -> State:
    user_id = config["configurable"]["user_id"]
    namespace = ("users", user_id)

    profile = store.get(namespace, "profile")

    if profile:
        user_name = profile.value.get("name", "사용자")
    else:
        user_name = "사용자"

    return {
        "message": state["message"],
        "result": f"{user_name}님, 입력 내용은 '{state['message']}'입니다.",
    }


builder = StateGraph(State)

builder.add_node("memory_node", memory_node)
builder.add_edge(START, "memory_node")
builder.add_edge("memory_node", END)


with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    store.put(
        ("users", "user_001"),
        "profile",
        {"name": "심플"},
    )

    graph = builder.compile(store=store)

    config = {
        "configurable": {
            "user_id": "user_001"
        }
    }

    result = graph.invoke(
        {"message": "PostgreSQL Store를 학습하고 있습니다."},
        config=config,
    )

    print(result["result"])
```

예상 결과:

```text
심플님, 입력 내용은 'PostgreSQL Store를 학습하고 있습니다.'입니다.
```

---

# 11. PostgresStore와 PostgresSaver 차이

두 클래스는 이름이 비슷하지만 역할이 다릅니다.

| 구분     | `PostgresStore`                  | `PostgresSaver`                      |
| ------ | -------------------------------- | ------------------------------------ |
| 주요 목적  | 장기 기억 저장                         | 그래프 실행 상태 저장                         |
| 저장 내용  | 사용자 정보, 선호도, 기억                  | 노드 실행 상태, 메시지 상태                     |
| 범위     | 여러 대화·스레드에서 공유 가능                | 일반적으로 특정 `thread_id` 중심              |
| 주요 메서드 | `put`, `get`, `search`, `delete` | `get`, `put`, `list`                 |
| 그래프 연결 | `compile(store=store)`           | `compile(checkpointer=checkpointer)` |

`PostgresSaver`도 최초 사용 전에 `setup()`을 실행해야 합니다. 공식 구현에서도 체크포인트 테이블과 마이그레이션 생성을 위해 초기 설정 호출이 필요합니다. ([LangChain Reference][4])

두 가지를 함께 사용할 수도 있습니다.

```python
from langgraph.store.postgres import PostgresStore
from langgraph.checkpoint.postgres import PostgresSaver

with (
    PostgresStore.from_conn_string(DB_URI) as store,
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
):
    store.setup()
    checkpointer.setup()

    graph = builder.compile(
        store=store,
        checkpointer=checkpointer,
    )
```

실행할 때는 `thread_id`와 `user_id`를 함께 지정합니다.

```python
config = {
    "configurable": {
        "thread_id": "conversation_001",
        "user_id": "user_001",
    }
}
```

* `thread_id`: 현재 대화나 그래프 실행을 구분
* `user_id`: 장기 기억을 저장할 사용자를 구분

---

# 12. Colab 사용 시 중요한 제한

Colab에 직접 설치한 PostgreSQL 데이터는 **런타임이 초기화되면 삭제됩니다**.

즉, 다음 상황에서는 데이터가 사라질 수 있습니다.

* 런타임 연결 해제
* 세션 초기화
* 런타임 유형 변경
* 장시간 미사용으로 인한 종료

따라서 Colab 내부 PostgreSQL은 다음 용도에 적합합니다.

```text
수업 실습
PostgresStore 동작 테스트
간단한 프로토타입
```

실제 프로젝트에서 데이터를 계속 보존하려면 외부 PostgreSQL을 권장합니다.

```text
Supabase
Neon
Google Cloud SQL
AWS RDS
Azure Database for PostgreSQL
직접 운영하는 PostgreSQL 서버
```

외부 PostgreSQL을 사용하는 경우 Colab에 PostgreSQL 서버를 설치할 필요가 없습니다. Python 패키지만 설치하고 제공받은 연결 문자열을 사용하면 됩니다.

```python
!pip install -qU \
    langgraph \
    langgraph-checkpoint-postgres \
    "psycopg[binary]" \
    psycopg-pool
```

```python
from langgraph.store.postgres import PostgresStore

DB_URI = "postgresql://사용자:비밀번호@외부호스트:5432/데이터베이스?sslmode=require"

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()
```

외부 서비스는 대부분 SSL 연결을 요구하므로 다음 옵션이 필요할 수 있습니다.

```text
?sslmode=require
```

---

# 13. 비밀번호를 코드에 직접 작성하지 않는 방법

Colab 보안 비밀 기능을 사용하는 것이 좋습니다.

Colab 왼쪽 메뉴에서 다음과 같이 등록합니다.

```text
보안 비밀 → 새 보안 비밀 추가
이름: POSTGRES_URI
값: postgresql://...
```

코드에서는 다음처럼 가져옵니다.

```python
from google.colab import userdata
from langgraph.store.postgres import PostgresStore

DB_URI = userdata.get("POSTGRES_URI")

if not DB_URI:
    raise RuntimeError(
        "Colab 보안 비밀에 POSTGRES_URI를 등록하세요."
    )

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    store.put(
        ("users", "user_001"),
        "profile",
        {"name": "심플"},
    )

    item = store.get(
        ("users", "user_001"),
        "profile",
    )

    print(item.value)
```

---

## 핵심 수정 사항

사용자의 원래 코드:

```python
store = PostgresStore.from_conn_string(
    "postgresql://user:pass@localhost/dbname"
)
```

Colab 실습용 권장 형태:

```python
from langgraph.store.postgres import PostgresStore

DB_URI = (
    "postgresql://langgraph_user:"
    "langgraph_pass@localhost:5432/langgraph_db"
)

with PostgresStore.from_conn_string(DB_URI) as store:
    store.setup()

    store.put(
        ("users", "user_001"),
        "profile",
        {"name": "심플"},
    )

    item = store.get(
        ("users", "user_001"),
        "profile",
    )

    print(item.value)
```

가장 중요한 차이는 `from_conn_string()`을 `with` 문으로 관리하고, 최초 연결 시 `store.setup()`을 실행하는 것입니다. Colab 내부 PostgreSQL은 세션 종료 시 데이터가 사라지므로 장기 보존이 필요하면 외부 관리형 PostgreSQL 연결 문자열로 교체해야 합니다.

[1]: https://reference.langchain.com/python/langgraph.store.postgres?utm_source=chatgpt.com "langgraph.store.postgres"
[2]: https://pypi.org/project/langgraph-checkpoint-postgres/?utm_source=chatgpt.com "langgraph-checkpoint-postgres"
[3]: https://github.com/langchain-ai/langgraph/issues/2887?utm_source=chatgpt.com "CREATE INDEX CONCURRENTLY cannot run inside a ..."
[4]: https://reference.langchain.com/javascript/langchain-langgraph-checkpoint-postgres/index/PostgresSaver?utm_source=chatgpt.com "PostgresSaver | @langchain/langgraph-checkpoint-postgres"
