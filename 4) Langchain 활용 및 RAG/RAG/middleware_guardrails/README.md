# LangChain 1.x Middleware & Guardrails 학생 실습

위키독스 Part 4의 여섯 하위 단원을 각각 독립 실행형 Python 코드로 구성했습니다.
대학 학사·학생지원 Agent를 공통 주제로 사용하며, 문서는 이미 로드되었다고 가정하고
각 파일에서 모의 데이터를 생성합니다.

## 실습 구성

| 파일 | 대표 기능 | 관찰 포인트 |
|---|---|---|
| `01_middleware_overview.py` | Node-style 전후 훅 | Agent 루프와 훅 실행 순서 |
| `02_builtin_middleware.py` | 호출 제한, Tool 재시도 | 비용 통제와 장애 복구 |
| `03_custom_middleware.py` | 로깅, 검증, 오류 변환 | 횡단 관심사 분리 |
| `04_guardrails_overview.py` | 결정적 입력 가드레일 | 인젝션 차단과 오탐 |
| `05_pii_detection.py` | PII redact/mask/block | 개인정보 처리 전략 |
| `06_human_in_the_loop.py` | approve/edit/reject | 고위험 도구의 사람 승인 |

## 환경 준비

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="본인의_OPENAI_API_KEY"
```

## 실행

```powershell
python 01_middleware_overview.py
python 02_builtin_middleware.py
python 03_custom_middleware.py
python 04_guardrails_overview.py
python 05_pii_detection.py
python 06_human_in_the_loop.py
```

## 안전한 수업 운영

- PII 실습에는 실제 개인정보를 사용하지 말고 제공된 가상 데이터만 사용합니다.
- HITL의 발송 도구는 실제 외부 시스템에 연결하지 않은 모의 함수입니다.
- 차단·마스킹·승인 여부와 함께 false positive/false negative를 기록합니다.
- 미들웨어 순서는 결과에 영향을 줄 수 있으므로 실험 시 순서를 함께 기록합니다.
- 프로덕션 HITL에서는 `InMemorySaver` 대신 영속 체크포인터를 사용해야 합니다.

## 결과 보고서 권장 항목

1. 미들웨어 적용 전후 실행 흐름
2. 모델 및 도구 호출 횟수
3. 실패 후 재시도 결과
4. PII 전략별 변환 결과
5. 가드레일 오탐·미탐 사례
6. HITL 승인·수정·거부 결과
