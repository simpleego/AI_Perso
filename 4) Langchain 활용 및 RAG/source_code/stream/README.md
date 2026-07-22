# LangChain Streaming + Gemini 실습

첨부 PDF의 스트리밍 주제를 현재 LangChain 1.x와 `ChatGoogleGenerativeAI`에 맞게 수정한 프로젝트입니다. 각 주제는 서로 독립된 파일로 분리되어 있습니다.

## 1. 실습 모델

기본 모델은 `gemini-2.5-flash-lite`입니다. Google AI Studio에서 발급한 Gemini API 키를 사용합니다.

## 2. 설치

### Windows PowerShell

```powershell
cd langchain_streaming_gemini_practice
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

### Windows CMD

```cmd
cd langchain_streaming_gemini_practice
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

### macOS / Linux

```bash
cd langchain_streaming_gemini_practice
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

`.env` 파일을 열어 다음 값을 수정합니다.

```env
GOOGLE_API_KEY=실제_Gemini_API_KEY
GEMINI_MODEL=gemini-2.5-flash-lite
```

## 3. 개별 실습 파일

| 파일 | 실습 내용 |
|---|---|
| `00_environment_check.py` | 패키지·API 키·모델 환경 점검 |
| `01_model_direct_stream.py` | 모델 직접 스트리밍 |
| `02_chain_lcel_stream.py` | LCEL 체인 스트리밍 |
| `03_async_model_stream.py` | 비동기 모델 스트리밍 |
| `04_agent_updates_stream.py` | 에이전트 단계별 `updates` |
| `05_agent_messages_stream.py` | 에이전트 토큰 `messages` |
| `06_agent_multi_mode_stream.py` | `updates`와 `messages` 동시 사용 |
| `07_custom_stream_writer.py` | 도구 내부 커스텀 진행률 이벤트 |
| `08_async_chain_stream.py` | LCEL 비동기 스트리밍 |
| `09_fastapi_sse_server.py` | FastAPI SSE 서버 |
| `10_sse_client.html` | 브라우저용 SSE 클라이언트 |
| `11_disable_streaming.py` | 스트리밍 비활성화 |
| `12_timeout_and_retry.py` | 타임아웃과 재시도 |
| `13_chunk_aggregation.py` | AIMessageChunk 결합 |
| `14_stream_timing_comparison.py` | invoke와 stream 체감 비교 |

## 4. 실행 예시

```bash
python 00_environment_check.py
python 01_model_direct_stream.py
python 02_chain_lcel_stream.py
python 04_agent_updates_stream.py
python 07_custom_stream_writer.py
```

각 파일은 다른 실습 파일을 먼저 실행하지 않아도 됩니다. 단, 공통 설정을 위해 같은 폴더의 `common.py`를 사용합니다.

## 5. FastAPI 웹 스트리밍

서버를 실행합니다.

```bash
uvicorn 09_fastapi_sse_server:app --reload
```

그다음 `10_sse_client.html`을 브라우저에서 엽니다. 서버 주소는 기본적으로 `http://127.0.0.1:8000`입니다.

> 파일명을 숫자로 시작해도 `uvicorn 09_fastapi_sse_server:app` 형식의 CLI import는 동작합니다. 환경에서 문제가 발생하면 파일명을 `fastapi_sse_server.py`로 바꾸어 실행하세요.

## 6. PDF 코드에서 보완한 점

- OpenAI 모델 대신 Gemini Developer API를 사용했습니다.
- `init_chat_model()` 대신 공급자별 설정이 명확한 `ChatGoogleGenerativeAI`를 사용했습니다.
- LangGraph의 통합 스트림 형식인 `version="v2"`를 에이전트 예제에 적용했습니다.
- Gemini 연동에 맞게 타임아웃 옵션을 `request_timeout`, 재시도를 `retries`로 수정했습니다.
- 문자열뿐 아니라 콘텐츠 블록으로 반환되는 경우도 출력할 수 있게 처리했습니다.
- FastAPI 예제에서 JSON 기반 SSE 이벤트, 오류 이벤트, 버퍼링 방지 헤더를 추가했습니다.
- 날씨와 문서 처리 도구는 외부 유료 API가 필요 없는 가상 데이터로 구성했습니다.

## 7. 주의 사항

- Gemini 무료 등급에도 호출량 제한이 있습니다.
- 무료 등급에 입력한 데이터는 Google 제품 개선에 사용될 수 있으므로 민감한 개인정보나 회사 기밀을 입력하지 않는 것이 좋습니다.
- 에이전트 예제는 LLM이 도구를 호출하므로 단순 모델 예제보다 API 호출 횟수가 많을 수 있습니다.
