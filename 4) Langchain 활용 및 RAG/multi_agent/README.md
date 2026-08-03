# LangChain 1.x 멀티 에이전트 시스템 실습

위키독스 Part 5의 다섯 하위 단원을 각각 독립 실행형 Python 예제로 구성했습니다.
공통 시나리오는 대학 종합지원 시스템이며 필요한 문서는 이미 로드되었다고 가정합니다.

## 실습 구성

| 파일 | 대표 패턴 | 핵심 관찰 항목 |
|---|---|---|
| `01_multi_agent_overview.py` | 전문화 + 병렬 실행 | 컨텍스트 격리와 실행 시간 |
| `02_subagents_pattern.py` | Supervisor + Workers | Agent를 도구로 래핑 |
| `03_handoffs_pattern.py` | 상태 기반 전환 | 순차 흐름과 담당 Agent |
| `04_skills_pattern.py` | 점진적 공개 | 필요한 전문 지침만 로드 |
| `05_router_pattern.py` | Router + `Send` | 병렬 팬아웃과 결과 합성 |

## 환경 준비 및 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="본인의_OPENAI_API_KEY"

python 01_multi_agent_overview.py
python 02_subagents_pattern.py
python 03_handoffs_pattern.py
python 04_skills_pattern.py
python 05_router_pattern.py
```

## 패턴 선택 요약

- 중앙 감독과 여러 번의 동적 조정이 필요하면 Subagents
- 단계가 순차적이고 담당 Agent가 사용자와 직접 대화하면 Handoffs
- 별도 Agent보다 프롬프트 전문화만 필요하면 Skills
- 하나의 질문을 여러 독립 도메인에 병렬 전달하면 Router
- 도구가 적고 문제가 단순하다면 멀티 에이전트보다 단일 Agent를 우선 검토

## 결과 보고서 권장 항목

1. 호출된 Agent와 도구 목록
2. 모델 호출 횟수
3. 순차·병렬 실행 시간
4. 각 Agent에 전달된 컨텍스트
5. 최종 답변의 근거 문서
6. 선택한 패턴이 문제에 적합한 이유와 한계
