# LangChain 프롬프트 실습 프로젝트

이 프로젝트는 다음 PDF의 **파일명 순서**를 그대로 따라 구성했습니다.

1. `1-3-0 프롬프트(Prompt)`
2. `1-3-1 프롬프트 작성 원칙`
3. `1-3-2 프롬프트 템플릿(PromptTemplate)`
4. `1-3-3 챗 프롬프트 템플릿(ChatPromptTemplate)`
5. `1-3-4 Few-shot Prompt`
6. `1-3-5 Partial Prompt`

PDF의 OpenAI 예제를 현재 LangChain과 Gemini API 방식으로 수정했으며, 각 코드 블록과 주요 개념을 **개별 실행 파일**로 분리했습니다.

## 1. 기본 모델

- 채팅 모델: `gemini-2.5-flash-lite`
- 임베딩 모델: `gemini-embedding-001`
- 연동 클래스: `ChatGoogleGenerativeAI`, `GoogleGenerativeAIEmbeddings`

Gemini API의 무료 등급은 호출량 제한이 있으며 지역, 계정, 시점에 따라 사용 가능량이 달라질 수 있습니다.

## 2. 설치

### Windows CMD

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

`.env` 파일을 열어 API 키를 입력합니다.

```env
GOOGLE_API_KEY=실제_API_KEY
GEMINI_MODEL=gemini-2.5-flash-lite
GEMINI_EMBEDDING_MODEL=gemini-embedding-001
```

## 3. 환경 점검

```bash
python 00_environment_check.py
```

## 4. 폴더별 학습 순서

### 01_1_3_0_prompt_overview

| 파일 | 학습 내용 | API 호출 |
|---|---|---|
| `01_prompt_template_basic.py` | 문자열 PromptTemplate | 없음 |
| `02_chat_prompt_chain.py` | ChatPromptTemplate + Gemini | 있음 |
| `03_prompt_structure_preview.py` | 역할·컨텍스트·지시·출력 구조 | 없음 |

### 02_1_3_1_prompt_principles

| 파일 | 학습 내용 |
|---|---|
| `01_vague_vs_specific.py` | 모호한 지시와 구체적 지시 비교 |
| `02_explicit_constraints.py` | 길이·문체·용어 제약 |
| `03_context_comparison.py` | 컨텍스트 유무 비교 |
| `04_audience_levels.py` | 초보자와 전문가용 응답 비교 |
| `05_role_definition.py` | 역할과 전문 분야 설정 |
| `06_step_by_step_code_review.py` | 단계별 작업 지시 |
| `07_output_markdown_table.py` | 표 형식 출력 |
| `08_output_json.py` | JSON 파서 활용 |
| `09_output_numbered_list.py` | 번호 목록 출력 |
| `10_structured_output_pydantic.py` | Gemini 네이티브 구조화 출력 |
| `11_few_shot_classification.py` | Few-shot 분류 |
| `12_translation_pattern_examples.py` | 패턴 예시 기반 번역 |
| `13_hallucination_guard.py` | 불확실성 표현과 환각 억제 |
| `14_context_only_qa.py` | 컨텍스트 제한 Q&A |
| `15_integrated_code_generation.py` | 종합 코드 생성 프롬프트 |
| `16_business_analysis_report.py` | 비즈니스 리포트 생성 |
| `17_prompt_checklist.py` | 작성 원칙 체크리스트 |

### 03_1_3_2_prompt_template

| 파일 | 학습 내용 |
|---|---|
| `01_components_product_review.py` | 지시·예시·맥락·질문 결합 |
| `02_string_template_format.py` | 변수 포맷팅 |
| `03_combine_templates.py` | 템플릿 덧셈 결합 |
| `04_combined_template_llm_chain.py` | 결합 템플릿 체인 실행 |

### 04_1_3_3_chat_prompt_template

| 파일 | 학습 내용 |
|---|---|
| `01_tuple_message_format.py` | 2-튜플 메시지 목록 |
| `02_tuple_message_chain.py` | 2-튜플 프롬프트 체인 |
| `03_message_prompt_templates.py` | 메시지별 템플릿 클래스 |
| `04_message_prompt_chain.py` | 메시지 템플릿 체인 |

### 05_1_3_4_few_shot_prompt

| 파일 | 학습 내용 | API 호출 |
|---|---|---|
| `01_example_formatter.py` | 예제 포맷터 | 없음 |
| `02_fixed_few_shot_prompt.py` | 고정 FewShotPromptTemplate | 없음 |
| `03_fixed_few_shot_llm_chain.py` | 고정 예제 + Gemini | 있음 |
| `04_semantic_example_selector.py` | 의미 유사도 예제 선택 | 임베딩 |
| `05_fixed_few_shot_chat.py` | 고정 채팅 Few-shot | 있음 |
| `06_dynamic_few_shot_chat.py` | 동적 채팅 Few-shot | 임베딩 + 채팅 |

### 06_1_3_5_partial_prompt

| 파일 | 학습 내용 |
|---|---|
| `01_string_partial.py` | 문자열 값 부분 바인딩 |
| `02_partial_variables_constructor.py` | 생성자에서 부분 변수 지정 |
| `03_function_partial_season.py` | 함수 기반 동적 부분 변수 |
| `04_dynamic_date_partial.py` | 현재 날짜 자동 삽입 |
| `05_partial_prompt_llm_chain.py` | Partial Prompt + Gemini |

## 5. 실행 예시

프로젝트 루트에서 실행합니다.

```bash
python 01_1_3_0_prompt_overview/01_prompt_template_basic.py
python 02_1_3_1_prompt_principles/01_vague_vs_specific.py
python 03_1_3_2_prompt_template/04_combined_template_llm_chain.py
python 04_1_3_3_chat_prompt_template/02_tuple_message_chain.py
python 05_1_3_4_few_shot_prompt/06_dynamic_few_shot_chat.py
python 06_1_3_5_partial_prompt/05_partial_prompt_llm_chain.py
```

## 6. PDF 원본 코드에서 보완한 부분

- `ChatOpenAI`와 `init_chat_model("gpt-4o-mini")`를 Gemini 연동으로 교체했습니다.
- 모델 응답을 문자열로 받을 때 `StrOutputParser`를 명시했습니다.
- JSON 출력은 단순한 “JSON으로 답하라” 지시뿐 아니라 `JsonOutputParser` 예제를 추가했습니다.
- 구조화 출력은 Gemini가 지원하는 `method="json_schema"`를 사용했습니다.
- Few-shot 동적 선택은 별도 Chroma 서버 없이 `InMemoryVectorStore`로 실행되도록 단순화했습니다.
- OpenAI 임베딩을 무료 등급이 있는 Gemini 임베딩으로 교체했습니다.
- PDF의 동적 Few-shot 호출에서 문자열을 직접 전달하던 부분을 입력 변수 딕셔너리로 수정했습니다.
- API 키 누락 시 이해하기 쉬운 오류가 나오도록 공통 검사 코드를 추가했습니다.

## 7. 주의사항

- `01_*`, `03_*` 등 API 호출이 없는 파일부터 실행하면 프롬프트 객체의 동작을 먼저 이해할 수 있습니다.
- API 호출 파일을 연속 실행하면 무료 할당량을 빠르게 사용할 수 있습니다.
- 모델이 생성한 코드나 사실 정보는 교육용 결과이므로 반드시 검토해야 합니다.
- `.env` 파일은 GitHub에 올리지 마세요.
