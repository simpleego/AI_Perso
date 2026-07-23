# LangChain 메모리와 대화 관리 실습 (1-6장)

wikidocs 1-6-1 ~ 1-6-5 내용을 기반으로, **무료 API 키로 사용 가능한
Google Gemini(gemini-2.5-flash)** 모델을 사용하도록 수정·보완한 실행 가능한 실습 코드입니다.
각 장(章)의 메시지(섹션) 단위로 소스 코드를 분리했고, 핵심 코드에 한국어 주석을 추가했습니다.

## 1. 사전 준비

### (1) 패키지 설치
```bash
pip install -r requirements.txt
```

### (2) 무료 API 키 발급 (Google AI Studio)
1. https://aistudio.google.com/apikey 접속 (구글 계정 로그인)
2. "Create API key" 클릭 → 키 복사 (무료 티어 제공)
3. `.env.example`을 `.env`로 복사 후 키 입력
```bash
cp .env.example .env
```
> 무료 티어는 분당/일일 요청 제한이 있습니다. 에이전트 예제는 내부적으로
> 여러 번 모델을 호출하므로, 연속 실행 시 잠시 대기가 필요할 수 있습니다.

## 2. 실행 방법
각 파일은 독립적으로 실행 가능합니다. (프로젝트 루트에서 실행 권장)
```bash
python 01_memory_concept/01_no_memory_problem.py
python 04_short_term_patterns/01_checkpointer_basic.py
```

## 3. 파일 구성

### 01_memory_concept/ (1-6-1. 메모리의 필요성과 개념)
| 파일 | 내용 |
|---|---|
| 01_no_memory_problem.py | 메모리가 없는 대화의 문제점 (상태 없는 LLM) |
| 02_runnable_with_message_history.py | RunnableWithMessageHistory (간단한 챗봇용) |
| 03_langgraph_memory.py | LangGraph 기반 메모리 (LangChain 1.0 권장) |
| 04_token_optimization.py | 토큰 비용 최적화 3가지 (윈도우/토큰 트리밍/요약) |

### 02_message_history/ (1-6-2. RunnableWithMessageHistory)
| 파일 | 내용 |
|---|---|
| 01_astronomy_chat.py | 구현 단계별 분석 + "그 행성" 참조 이해 실험 |
| 02_session_isolation.py | 세션 기반 격리 (session_id별 독립 대화) |
| 03_trim_history.py | 프로덕션 고려사항: 토큰 제한 관리 (trim_messages) |

### 03_memory_stores/ (1-6-3. 다양한 메모리 저장 방식)
| 파일 | 내용 |
|---|---|
| _chain.py | 공통 체인 빌더 (저장소 함수만 교체하는 구조) |
| 01_inmemory_store.py | 인메모리 저장소 (개발용, 재시작 시 소멸) |
| 02_file_store.py | 파일 기반 저장소 (JSON, 재실행해도 기억 유지) |
| 03_sqlite_store.py | SQLite (단일 서버 프로덕션, DB 파일 자동 생성) |
| 04_redis_store.py | Redis (분산 환경, TTL 지원) ※ Redis 서버 필요 |
| 05_postgres_store.py | PostgreSQL (안정적 영구 저장) ※ PG 서버 필요 |

### 04_short_term_patterns/ (1-6-4. 단기 메모리 패턴)
| 파일 | 내용 |
|---|---|
| 01_checkpointer_basic.py | 단기 메모리 활성화 (create_agent + checkpointer) |
| 02_trimming_middleware.py | 메시지 트리밍 (@before_model, 일시적 제한) |
| 03_deletion.py | 메시지 삭제 (RemoveMessage, 민감 정보 영구 제거) |
| 04_summarization.py | 메시지 요약 (SummarizationMiddleware) |
| 05_customer_support_bot.py | 실전: 도구 + 요약 + 트리밍 조합 고객 지원 챗봇 |

### 05_long_term_memory/ (1-6-5. 장기 메모리)
| 파일 | 내용 |
|---|---|
| 01_store_basics.py | Store 구조와 CRUD (put/get/search/delete/TTL) ※ API 키 불필요 |
| 02_read_memory_tool.py | 도구에서 메모리 읽기 (runtime.store) |
| 03_write_memory_tool.py | 도구에서 메모리 쓰기 (스레드 간 정보 유지 확인) |
| 04_shopping_assistant.py | 실전: 개인화된 쇼핑 도우미 (구매 이력 기반 추천) |
| 05_namespace_and_manage.py | 네임스페이스 검색 / 사용자 데이터 삭제 ※ API 키 불필요 |

## 4. 원본 대비 주요 변경 사항
- 모델: `gpt-4o-mini`/`gpt-4o`/`claude-haiku` → **`google_genai:gemini-2.5-flash`** (무료 API 키)
- `.env` + `python-dotenv` 기반 키 관리 (`_common.py` 공통 모듈)
- 각 섹션을 독립 실행 파일로 분리, `main()` 함수 구조 적용
- LangChain 1.0 기준으로 세부 API 보정
  - `SQLChatMessageHistory`: `connection_string` → `connection` 인자 사용
  - `@before_model` 미들웨어 함수는 `(state, runtime)` 시그니처 사용
  - `SummarizationMiddleware(model=..., max_tokens_before_summary=..., messages_to_keep=...)`
  - Store 네임스페이스는 튜플 `("users", "user-123")` 형태, 조회 결과는 `.value`로 접근
- Redis/PostgreSQL 예제는 서버 미설치 시 안내 메시지를 출력하도록 예외 처리 추가

## 5. 수업 진행 팁
- API 키 없이 바로 실행 가능한 파일: `05_long_term_memory/01_store_basics.py`, `05_namespace_and_manage.py`
  → 개념(네임스페이스/키 구조) 설명용 워밍업으로 활용
- 단기 vs 장기 메모리 비교: 04장 `01_checkpointer_basic.py`(thread_id 기준)와
  05장 `03_write_memory_tool.py`(thread가 바뀌어도 기억)를 나란히 시연하면 효과적입니다.
- 라이브러리 버전에 따라 미들웨어/Store API 세부 인자가 다를 수 있으니,
  오류 발생 시 `pip show langchain langgraph`로 버전 확인 후 공식 문서를 참조하세요.
