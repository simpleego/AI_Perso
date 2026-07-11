# 랭체인에서 체인의 개념과 종류

<img width="800" alt="image" src="https://github.com/user-attachments/assets/9fa599a2-d906-45ac-ab96-4b148f719369" />

---  

<img width="800" alt="image" src="https://github.com/user-attachments/assets/5348bd4b-ab6a-45dc-9fa5-de67635476ba" />

>  `LLMChain`, `SequentialChain`, `RouterChain`은 개념 학습에는 유용하지만, 현재 LangChain에서는 **Runnable과 LCEL의 `|` 연산자**를 이용하는 방식이 권장됩니다.
>  `LLMChain`과 `LLMRouterChain`은 공식 참조 문서에서 deprecated로 표시되어 있으며, `|`로 연결한 구성은 `RunnableSequence`로 실행됩니다. ([LangChain Reference Docs][1])

## 0. 공통 환경 설정

### 라이브러리 설치

```bash
pip install -U langchain langchain-openai python-dotenv
```

### `.env`

```env
OPENAI_API_KEY=여기에_API_키_입력
OPENAI_MODEL=gpt-5.4
```

### 공통 코드

아래 코드를 먼저 실행한 후 각 실습을 실행합니다.

```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI


load_dotenv()

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.4")
)

parser = StrOutputParser()
```

---

# 1. LLMChain: 기본 체인

프롬프트와 LLM을 연결하는 가장 기본적인 체인입니다.

```python
# 프롬프트 생성
prompt = ChatPromptTemplate.from_template(
    "{topic}을 비전공자가 이해할 수 있도록 3문장으로 설명해주세요."
)

# 프롬프트 → 모델 → 문자열 출력
llm_chain = prompt | model | parser

# 실행
result = llm_chain.invoke(
    {"topic": "LangChain"}
)

print(result)
```

### 처리 과정

```text
입력
  ↓
PromptTemplate
  ↓
LLM 호출
  ↓
문자열 응답
```

### 예상 응답 형태

```text
LangChain은 대규모 언어 모델을 다양한 데이터와 프로그램에
연결할 수 있도록 도와주는 프레임워크입니다.

프롬프트, AI 모델, 데이터베이스 등을 하나의 작업 흐름으로
구성할 수 있습니다.
```

---

# 2. SequentialChain: 순차 체인

첫 번째 체인의 출력을 두 번째 체인의 입력으로 전달합니다.

예제에서는 다음 순서로 실행합니다.

```text
주제 입력
  ↓
강의 제목 생성
  ↓
생성된 제목으로 강의 소개 작성
```

```python
# 1단계: 제목 생성
title_chain = (
    ChatPromptTemplate.from_template(
        "{topic}에 대한 강의 제목을 하나만 작성해주세요."
    )
    | model
    | parser
)

# 2단계: 제목을 사용해 소개 작성
intro_chain = (
    ChatPromptTemplate.from_template(
        """
다음 제목의 강의 소개를 3문장으로 작성해주세요.

제목: {title}
"""
    )
    | model
    | parser
)

# 1단계 출력 문자열을 2단계의 title 입력으로 변환
sequential_chain = (
    title_chain
    | RunnableLambda(lambda title: {"title": title})
    | intro_chain
)

# 실행
result = sequential_chain.invoke(
    {"topic": "RAG"}
)

print(result)
```

`RunnableLambda`는 일반 파이썬 함수를 LangChain 실행 흐름에 넣을 때 사용합니다. 여기서는 첫 번째 결과를 `{"title": 결과}` 형태로 변환합니다.

---

# 3. RouterChain: 라우터 체인

사용자의 질문을 분석하여 적합한 체인을 선택합니다.

```text
사용자 질문
     ↓
라우터
   ↙     ↘
수학 체인  일반 지식 체인
```

```python
# 수학 질문용 체인
math_chain = (
    ChatPromptTemplate.from_template(
        """
당신은 수학 강사입니다.
계산 과정과 답을 간단히 설명해주세요.

질문: {question}
"""
    )
    | model
    | parser
)

# 일반 질문용 체인
general_chain = (
    ChatPromptTemplate.from_template(
        """
당신은 친절한 AI 강사입니다.
다음 질문에 쉽게 답변해주세요.

질문: {question}
"""
    )
    | model
    | parser
)


# 질문에 따라 체인 선택
def route(input_data):
    question = input_data["question"]

    math_keywords = [
        "계산",
        "더하기",
        "빼기",
        "곱하기",
        "나누기",
        "+",
        "-",
        "*",
        "/",
    ]

    if any(keyword in question for keyword in math_keywords):
        return math_chain

    return general_chain


# 라우터 체인 생성
router_chain = RunnableLambda(route)


# 수학 질문
result1 = router_chain.invoke(
    {"question": "25 곱하기 4를 계산해주세요."}
)

print("수학 질문 결과")
print(result1)


# 일반 질문
result2 = router_chain.invoke(
    {"question": "RAG란 무엇인가요?"}
)

print("\n일반 질문 결과")
print(result2)
```

`RunnableLambda`가 다른 Runnable을 반환하면, LangChain은 선택된 Runnable을 이어서 실행합니다. 이를 이용하면 간단한 조건 기반 라우터를 만들 수 있습니다. ([LangChain Reference Docs][2])

---

# 세 체인의 비교

| 체인 종류     | 처리 방식                   | 장점                                    | 단점                                               | 주요 응용 분야                                |
| --------- | ----------------------- | ------------------------------------- | ------------------------------------------------ | --------------------------------------- |
| 기본 LLM 체인 | 프롬프트와 모델을 한 번 연결        | 코드가 단순하고 이해하기 쉬움, 호출 비용과 시간이 비교적 적음   | 복잡한 다단계 작업 처리에 한계                                | 문서 요약, 질문 답변, 번역, 분류, 문장 생성             |
| 순차 체인     | 앞 단계의 출력을 다음 단계 입력으로 전달 | 복잡한 작업을 작은 단계로 분리 가능, 단계별 프롬프트 최적화 가능 | LLM 호출 횟수가 증가하여 비용과 시간이 늘어남, 앞 단계 오류가 다음 단계에 전달됨 | 제목→목차→본문, 질문→SQL→결과 설명, 문서 추출→요약        |
| 라우터 체인    | 입력에 따라 서로 다른 체인을 선택     | 질문 유형별 전문 처리 가능, 불필요한 체인 실행을 줄일 수 있음  | 라우팅 기준이 부정확하면 잘못된 체인이 선택됨, 체인 수가 많아질수록 관리 복잡     | FAQ 분류, 수학·일반 질문 분리, 언어별 번역, 분야별 RAG 검색 |

## 핵심 구분

```text
기본 LLM 체인
입력 → 하나의 작업 → 출력

순차 체인
입력 → 작업 1 → 작업 2 → 최종 출력

라우터 체인
입력 → 조건 판단 → 적절한 작업 선택 → 출력
```

실제 애플리케이션에서는 세 방식을 함께 사용할 수 있습니다. 예를 들어 라우터가 질문 분야를 선택한 뒤, 선택된 분야 내부에서 여러 순차 체인을 실행하도록 구성할 수 있습니다. 분야별 지식이나 도구가 분리된 시스템에서는 이러한 라우터 패턴이 특히 유용합니다. ([docs.langchain.com][3])

[1]: https://reference.langchain.com/python/langchain-classic/chains/llm/LLMChain?utm_source=chatgpt.com "LLMChain | langchain_classic"
[2]: https://reference.langchain.com/python/langchain-core/runnables/base/RunnableLambda?utm_source=chatgpt.com "RunnableLambda | langchain_core"
[3]: https://docs.langchain.com/oss/python/langchain/multi-agent/router-knowledge-base?utm_source=chatgpt.com "Build a multi-source knowledge base with routing"

