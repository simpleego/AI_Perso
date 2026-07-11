# PromptTemplate
> PromptTemplate은 이전 방식이므로, 현재 코드에서는 `langchain_core.prompts`에서 가져오는 형태로 수정하는 것이 적절합니다.
> `PromptTemplate`은 문자열 안의 `{변수}`를 실제 입력값으로 교체해 재사용 가능한 프롬프트를 만드는 클래스입니다. ([LangChain Reference Docs][1])

## 1. 라이브러리 설치

```bash
pip install -U langchain langchain-openai python-dotenv
```

## 2. `.env` 파일 작성

파이썬 파일과 같은 폴더에 `.env` 파일을 생성합니다.

```env
OPENAI_API_KEY=여기에_API_키_입력
OPENAI_MODEL=gpt-5.6-luna
```

예제에서는 비용 민감형 작업용으로 제공되는 `gpt-5.6-luna`를 사용했으며, 계정에서 사용 가능한 다른 모델로 변경할 수 있습니다. ([OpenAI 플랫폼][2])

---

# 실습 1. PromptTemplate의 변수 치환 확인

먼저 OpenAI API를 호출하지 않고, 프롬프트가 어떤 형태로 완성되는지 확인합니다.

```python
from langchain_core.prompts import PromptTemplate


# 1. 프롬프트 템플릿 정의
template = """
당신은 전문 {profession}입니다.

다음 주제를 {tone} 말투로 비전공자도 이해할 수 있게 설명해주세요.

주제: {topic}

답변 형식:
1. 핵심 개념
2. 쉬운 비유
3. 활용 사례
"""


# 2. PromptTemplate 객체 생성
prompt = PromptTemplate(
    template=template,
    input_variables=[
        "profession",
        "topic",
        "tone",
    ],
)


# 3. 템플릿에 전달할 입력값
input_data = {
    "profession": "AI 연구원",
    "topic": "트랜스포머 모델",
    "tone": "친근한",
}


# 4. 입력값을 템플릿에 적용
formatted_prompt = prompt.format(**input_data)


# 5. 완성된 프롬프트 출력
print("=== 완성된 프롬프트 ===")
print(formatted_prompt)
```

### 예상 출력

```text
=== 완성된 프롬프트 ===

당신은 전문 AI 연구원입니다.

다음 주제를 친근한 말투로 비전공자도 이해할 수 있게 설명해주세요.

주제: 트랜스포머 모델

답변 형식:
1. 핵심 개념
2. 쉬운 비유
3. 활용 사례
```

이 단계에서는 LLM을 호출하지 않으므로 API 비용이 발생하지 않습니다.

---

# 실습 2. PromptTemplate을 GPT 모델과 연결

앞에서 만든 `prompt`를 OpenAI 모델과 연결합니다. OpenAI 연동은 별도 통합 패키지인 `langchain-openai`의 `ChatOpenAI`를 사용합니다. ([Docs by LangChain][3])

```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# 1. 환경변수 불러오기
# --------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되지 않았습니다. "
        ".env 파일을 확인해주세요."
    )


# --------------------------------------------------
# 2. 프롬프트 템플릿 정의
# --------------------------------------------------
template = """
당신은 전문 {profession}입니다.

다음 주제를 {tone} 말투로 비전공자도 이해할 수 있게 설명해주세요.

주제: {topic}

답변 형식:
1. 핵심 개념
2. 쉬운 비유
3. 활용 사례

답변은 한국어로 작성해주세요.
"""


prompt = PromptTemplate(
    template=template,
    input_variables=[
        "profession",
        "topic",
        "tone",
    ],
)


# --------------------------------------------------
# 3. OpenAI 모델 생성
# --------------------------------------------------
model = ChatOpenAI(
    model=model_name,
    timeout=30,
    max_retries=2,
)


# --------------------------------------------------
# 4. LCEL 방식으로 체인 구성
# PromptTemplate → GPT 모델 → 문자열 변환
# --------------------------------------------------
chain = prompt | model | StrOutputParser()


# --------------------------------------------------
# 5. 입력값 준비
# --------------------------------------------------
input_data = {
    "profession": "AI 연구원",
    "topic": "트랜스포머 모델",
    "tone": "친근한",
}


# --------------------------------------------------
# 6. 체인 실행
# --------------------------------------------------
try:
    response = chain.invoke(input_data)

    print("=== GPT 응답 ===")
    print(response)

except Exception as error:
    print("모델 호출 중 오류가 발생했습니다.")
    print(f"오류 내용: {error}")
```

`prompt | model | StrOutputParser()`는 프롬프트 생성, 모델 호출, 문자열 변환을 순서대로 연결합니다. `invoke()`에는 템플릿 변수명과 동일한 키를 가진 딕셔너리를 전달합니다. ([Docs by LangChain][4])

---

# 실습 3. 입력값을 바꾸어 프롬프트 재사용

`PromptTemplate`의 핵심은 동일한 템플릿을 여러 입력에 반복해서 사용할 수 있다는 점입니다.

```python
examples = [
    {
        "profession": "AI 연구원",
        "topic": "트랜스포머 모델",
        "tone": "친근한",
    },
    {
        "profession": "데이터 분석가",
        "topic": "머신러닝과 딥러닝의 차이",
        "tone": "쉽고 간결한",
    },
    {
        "profession": "소프트웨어 강사",
        "topic": "LangChain의 역할",
        "tone": "학생에게 설명하는",
    },
]


for index, data in enumerate(examples, start=1):
    print(f"\n{'=' * 50}")
    print(f"{index}번째 질문")
    print(f"{'=' * 50}")

    response = chain.invoke(data)
    print(response)
```

---

# 실습 4. `batch()`로 여러 질문 한 번에 처리

```python
examples = [
    {
        "profession": "AI 연구원",
        "topic": "트랜스포머 모델",
        "tone": "친근한",
    },
    {
        "profession": "데이터 분석가",
        "topic": "벡터 데이터베이스",
        "tone": "비전공자를 위한",
    },
    {
        "profession": "소프트웨어 강사",
        "topic": "RAG 시스템",
        "tone": "예시를 포함한",
    },
]


responses = chain.batch(examples)


for index, response in enumerate(responses, start=1):
    print(f"\n=== {index}번째 응답 ===")
    print(response)
```

## 핵심 실행 구조

```text
입력 데이터
{
    profession: "AI 연구원",
    topic: "트랜스포머 모델",
    tone: "친근한"
}
        ↓
PromptTemplate
        ↓
완성된 프롬프트
        ↓
ChatOpenAI
        ↓
AIMessage 객체
        ↓
StrOutputParser
        ↓
일반 문자열 응답
```

수업에서는 **실습 1로 변수 치환 원리를 확인한 다음, 실습 2에서 실제 LLM을 연결하는 순서**로 진행하는 것이 이해하기 좋습니다.

[1]: https://reference.langchain.com/python/langchain-core/prompts/prompt/PromptTemplate?utm_source=chatgpt.com "PromptTemplate | langchain_core"
[2]: https://platform.openai.com/docs/models "
  Models | OpenAI API
"
[3]: https://docs.langchain.com/oss/python/integrations/chat/openai?utm_source=chatgpt.com "ChatOpenAI integration - Docs by LangChain"
[4]: https://docs.langchain.com/langsmith/trace-with-langchain?utm_source=chatgpt.com "Trace LangChain applications (Python and JS/TS)"
