
# 기사 요약 체인 만들기 실습 코드

## 1. 이미지에서 추출한 원본 코드

```python
from langchain.chains import SequentialChain, LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)

# 첫 번째 체인: 기사 요약
summarize_template = """
다음 뉴스 기사를 3-4문장으로 요약해주세요:
{article}
요약:
"""

summarize_prompt = PromptTemplate(
    template=summarize_template,
    input_variables=["article"]
)

summarize_chain = LLMChain(
    llm=llm,
    prompt=summarize_prompt,
    output_key="summary"
)

# 두 번째 체인: 핵심 주제 추출
topics_template = """
다음 요약에서 핵심 주제 3가지를 추출해주세요:
{summary}
주제:
"""

topics_prompt = PromptTemplate(
    template=topics_template,
    input_variables=["summary"]
)

topics_chain = LLMChain(
    llm=llm,
    prompt=topics_prompt,
    output_key="topics"
)

# 체인 연결
sequential_chain = SequentialChain(
    chains=[summarize_chain, topics_chain],
    input_variables=["article"],
    output_variables=["summary", "topics"]
)

# 실행
result = sequential_chain(
    {"article": "여기에 긴 뉴스 기사 내용..."}
)

print("요약:", result["summary"])
print("주제:", result["topics"])
```

## 2. 확인 결과

원본 코드의 처리 구조는 올바릅니다.

```text
기사 입력
   ↓
기사 요약 체인
   ↓
요약 결과
   ↓
주제 추출 체인
   ↓
요약 + 핵심 주제 출력
```

다만 최신 LangChain 환경에서는 다음 부분을 수정해야 합니다.

* `langchain.llms.OpenAI` 대신 `langchain_openai.ChatOpenAI` 사용
* `LLMChain`, `SequentialChain` 대신 LCEL의 `|`와 Runnable 사용
* 체인 실행은 `chain(...)` 대신 `chain.invoke(...)` 사용
* API 키는 코드에 직접 입력하지 않고 환경변수로 관리

`LLMChain`은 현재 deprecated 상태이며, 공식 참조 문서도 Runnable 기반 구현을 안내합니다. OpenAI 연동 역시 별도 패키지인 `langchain-openai`를 설치하여 `ChatOpenAI`를 사용합니다. ([Docs by LangChain][1])

---

# 3. 실습용 최신 코드

## 라이브러리 설치

터미널 또는 명령 프롬프트에서 실행합니다.

```bash
pip install -U langchain langchain-openai python-dotenv
```

코랩에서는 다음과 같이 실행합니다.

```python
!pip install -qU langchain langchain-openai python-dotenv
```

## `.env` 파일

파이썬 파일과 같은 폴더에 `.env` 파일을 생성합니다.

```env
OPENAI_API_KEY=여기에_OpenAI_API_키_입력
OPENAI_MODEL=gpt-5.4-mini
```

공식 OpenAI 모델 문서에서 비용과 응답 속도를 고려한 소형 모델로 `gpt-5.4-mini`를 안내하고 있으므로 실습 기본값으로 사용했습니다. ([OpenAI 개발자][2])

## 전체 실행 코드

```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI


# ==================================================
# 1. 환경변수 불러오기
# ==================================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되지 않았습니다. "
        ".env 파일을 확인해주세요."
    )


# ==================================================
# 2. 모델 생성
# ==================================================
model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
    timeout=30,
    max_retries=2,
)

parser = StrOutputParser()


# ==================================================
# 3. 첫 번째 체인: 기사 요약
# ==================================================
summarize_prompt = ChatPromptTemplate.from_template(
    """
다음 기사를 3~4문장으로 요약해주세요.

조건:
- 기사에 없는 내용은 추가하지 마세요.
- 중요한 내용을 중심으로 작성하세요.
- 한국어로 답변하세요.

기사:
{article}

요약:
"""
)

summarize_chain = summarize_prompt | model | parser


# ==================================================
# 4. 두 번째 체인: 핵심 주제 추출
# ==================================================
topics_prompt = ChatPromptTemplate.from_template(
    """
다음 기사 요약에서 핵심 주제 3가지를 추출해주세요.

각 주제는 짧은 키워드 형태로 작성하세요.

요약:
{summary}

출력 형식:
1. 주제
2. 주제
3. 주제
"""
)

topics_chain = topics_prompt | model | parser


# ==================================================
# 5. 두 개의 체인을 순차적으로 연결
# ==================================================
article_chain = (
    # 원본 article을 유지하면서 summary 추가
    RunnablePassthrough.assign(
        summary=summarize_chain
    )

    # 생성된 summary를 사용하여 topics 추가
    | RunnablePassthrough.assign(
        topics=topics_chain
    )
)


# ==================================================
# 6. 실습용 기사
# ==================================================
article = """
대전시가 지역 청년과 재직자를 대상으로 인공지능 실무 교육을
확대한다고 발표했다. 이번 교육은 생성형 AI, 데이터 분석,
인공지능 서비스 개발 과정으로 구성된다.

교육생들은 이론 수업뿐만 아니라 실제 데이터를 활용한 프로젝트도
수행한다. 대전시는 지역 기업과 연계하여 우수 프로젝트의 사업화와
취업 지원도 추진할 계획이다.
"""


# ==================================================
# 7. 체인 실행
# ==================================================
try:
    result = article_chain.invoke(
        {
            "article": article
        }
    )

    print("=" * 60)
    print("기사 요약")
    print("=" * 60)
    print(result["summary"])

    print("\n" + "=" * 60)
    print("핵심 주제")
    print("=" * 60)
    print(result["topics"])

except Exception as error:
    print("모델 실행 중 오류가 발생했습니다.")
    print(f"오류 내용: {error}")
```

`RunnablePassthrough.assign()`은 기존 입력값을 그대로 유지하면서 새로운 키를 추가합니다. 첫 번째 단계에서 `summary`를 추가하고, 두 번째 단계에서 그 요약을 이용해 `topics`를 추가합니다. ([LangChain Reference][3])

## 최종 결과 구조

```python
{
    "article": "원본 기사",
    "summary": "생성된 기사 요약",
    "topics": "추출된 핵심 주제"
}
```

---

# 4. 더 간단한 초급자용 코드

`RunnablePassthrough`가 아직 어렵다면 두 체인을 직접 순서대로 호출해도 됩니다.

```python
# 1단계: 기사 요약
summary = summarize_chain.invoke(
    {
        "article": article
    }
)

# 2단계: 요약 결과로 주제 추출
topics = topics_chain.invoke(
    {
        "summary": summary
    }
)

print("=== 기사 요약 ===")
print(summary)

print("\n=== 핵심 주제 ===")
print(topics)
```

두 코드의 작업 순서는 같습니다.

```text
summarize_chain.invoke(article)
            ↓
         summary
            ↓
topics_chain.invoke(summary)
            ↓
          topics
```

수업에서는 먼저 **초급자용 직접 호출 방식**으로 데이터 전달 과정을 설명한 후, `RunnablePassthrough.assign()`을 이용한 통합 체인으로 확장하는 것이 이해하기 좋습니다.

[1]: https://docs.langchain.com/oss/python/integrations/chat/openai?utm_source=chatgpt.com "ChatOpenAI integration - Docs by LangChain"
[2]: https://developers.openai.com/api/docs/models?utm_source=chatgpt.com "Models | OpenAI API"
[3]: https://reference.langchain.com/python/langchain-core/runnables/passthrough/RunnablePassthrough?utm_source=chatgpt.com "RunnablePassthrough | langchain_core"
