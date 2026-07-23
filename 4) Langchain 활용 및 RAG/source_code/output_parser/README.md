# LangChain 출력 파서 실습 (CSV Parser / JSON Parser)

wikidocs 1-5-1(CSV Parser), 1-5-2(JSON Parser) 내용을 기반으로,
**무료 API KEY로 사용 가능한 Google Gemini(gemini-2.5-flash)** 모델을 사용하도록
수정·보완한 실행 가능한 실습 코드입니다.

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
# .env 파일 안의 GOOGLE_API_KEY 값 수정
```

> 참고: 무료 티어는 분당/일일 요청 수 제한(RPM/RPD)이 있습니다.
> 수업 실습용으로는 충분하지만, 연속 호출 시 잠시 대기가 필요할 수 있습니다.

## 2. 실행 방법
각 파일은 독립적으로 실행 가능합니다.
```bash
python csv_parser/01_basic_usage.py
python json_parser/04_nested_object.py
```

## 3. 파일 구성

### csv_parser/ (1-5-1. CSV Parser)
| 파일 | 내용 |
|---|---|
| 01_basic_usage.py | 파서 생성, 포맷 지시사항, 직접 파싱 |
| 02_chain_basic.py | PromptTemplate + LCEL 체인 |
| 03_chat_prompt.py | ChatPromptTemplate과 함께 사용 |
| 04_keyword_extraction.py | 실전: 키워드 추출 |
| 05_recommendation.py | 실전: 추천 목록 생성 |
| 06_choices.py | 실전: 선택지 생성 |
| 07_tags.py | 실전: 태그 생성 (해시태그 포맷팅) |
| 08_postprocess_validate.py | 결과 후처리 및 검증 |

### json_parser/ (1-5-2. JSON Parser)
| 파일 | 내용 |
|---|---|
| 01_basic_pydantic.py | Pydantic 모델 정의, 포맷 지시사항 |
| 02_chain_basic.py | 체인 구성 및 실행 (레시피) |
| 03_chat_prompt.py | ChatPromptTemplate (제품 분석) |
| 04_nested_object.py | 중첩 객체 처리 (책 정보) |
| 05_api_design.py | 실전: API 응답 구조화 |
| 06_comparison.py | 실전: 비교 분석 결과 구조화 |
| 07_error_analysis.py | 실전: 오류 분석 결과 |
| 08_with_structured_output.py | with_structured_output 비교 (권장 방식) |
| 09_safe_parse.py | 오류 처리 (파싱 실패 대응) |

## 4. 원본 대비 변경 사항
- 모델: `gpt-4o-mini` → **`gemini-2.5-flash`** (무료 API 키 사용 가능)
  - `init_chat_model("google_genai:gemini-2.5-flash")` 형태로 초기화
- `.env` + `python-dotenv`로 API 키 관리 코드 추가
- 각 예제를 독립 실행 가능한 파일로 분리, `main()` 함수 구조 적용
- API 키 미설정 시 안내 메시지 출력 코드 추가
