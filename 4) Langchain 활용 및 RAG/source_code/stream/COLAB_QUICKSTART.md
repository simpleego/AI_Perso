# Google Colab 빠른 실행

## 1. ZIP 업로드 및 압축 해제

```python
from google.colab import files
uploaded = files.upload()
```

업로드한 ZIP 파일명이 `langchain_streaming_gemini_practice.zip`일 때:

```python
!unzip -q langchain_streaming_gemini_practice.zip
%cd langchain_streaming_gemini_practice
```

## 2. 패키지 설치

```python
!pip install -q -r requirements.txt
```

패키지 설치 후 런타임 재시작 안내가 나오면 런타임을 재시작한 뒤 다시 프로젝트 폴더로 이동합니다.

## 3. API 키 설정

Colab의 왼쪽 열쇠 아이콘에서 보안 비밀을 만들 수 있습니다.

- 이름: `GOOGLE_API_KEY`
- 값: Google AI Studio에서 발급한 API 키

```python
from google.colab import userdata
import os

os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL"] = "gemini-2.5-flash-lite"
```

## 4. 개별 파일 실행

```python
!python 00_environment_check.py
!python 01_model_direct_stream.py
!python 02_chain_lcel_stream.py
!python 03_async_model_stream.py
```

에이전트 스트리밍:

```python
!python 04_agent_updates_stream.py
!python 05_agent_messages_stream.py
!python 06_agent_multi_mode_stream.py
!python 07_custom_stream_writer.py
```

## 5. Colab에서 FastAPI 실행 시 주의

Colab은 로컬 PC의 `127.0.0.1:8000`을 브라우저에 직접 노출하지 않습니다. 따라서 `09_fastapi_sse_server.py`와 `10_sse_client.html` 실습은 로컬 Windows 환경에서 실행하는 편이 간단합니다.
