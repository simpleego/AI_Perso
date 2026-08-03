# LangChain 1.x Agents & Tools 학생 실습

위키독스 Part 3의 네 하위 단원을 각각 하나의 독립 실행형 Python 코드로 구성했습니다.
모든 예제는 대학 학사도우미 시나리오를 사용하며, 외부 문서는 이미 로드되었다고
가정하고 코드 안에 모의 데이터를 생성합니다.

## 실습 구성

| 파일 | 핵심 내용 | 관찰할 항목 |
|---|---|---|
| `01_agent_overview.py` | `create_agent`, ReAct, 다중 도구 호출 | 전체 메시지와 도구 선택 |
| `02_builtin_tools.py` | Tavily 내장 검색 통합 | 검색 도구 스키마와 결과 |
| `03_custom_tools.py` | `@tool`, Pydantic 입력 스키마 | 도구 설명·검증·계산 |
| `04_toolruntime_context.py` | `ToolRuntime`, `context_schema` | 숨겨진 컨텍스트와 개인화 |

## 환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="본인의_OPENAI_API_KEY"

# 실습 2에서만 필요
$env:TAVILY_API_KEY="본인의_TAVILY_API_KEY"
```

## 권장 실행 순서

```powershell
python 01_agent_overview.py
python 02_builtin_tools.py
python 03_custom_tools.py
python 04_toolruntime_context.py
```

## 수업 진행 제안

1. 실행 전 어떤 도구가 호출될지 학생이 먼저 예측한다.
2. `result["messages"]`에서 AI 메시지, Tool 메시지, 최종 답변을 구분한다.
3. 각 파일 끝의 실습 과제를 수행한다.
4. 도구 설명, 타입 힌트, 시스템 프롬프트를 바꿔 도구 선택률을 비교한다.
5. 도구가 실패하거나 권한이 없을 때 안전한 답변이 나오는지 확인한다.

실제 서비스에서는 개인정보나 API 키를 사용자 메시지에 넣지 말고, 실습 4처럼
런타임 컨텍스트 또는 별도의 보안 저장소로 전달해야 합니다.
