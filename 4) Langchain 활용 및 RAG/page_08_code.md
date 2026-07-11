.env 파일

파이썬 파일과 같은 폴더에 .env 파일을 생성합니다.

```
OPENAI_API_KEY=sk-여기에-실제-API-키-입력
OPENAI_MODEL=gpt-5.4-mini
```
.env 파일은 GitHub에 올리지 않도록 .gitignore에 추가합니다.

```
.gitignore 파일 내용
.env
```


```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# --------------------------------------------------
# 1. 환경변수 불러오기
# --------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되지 않았습니다. "
        ".env 파일에 API 키를 입력해주세요."
    )


# --------------------------------------------------
# 2. OpenAI 채팅 모델 생성
# --------------------------------------------------
model = ChatOpenAI(
    model=model_name,
    timeout=30,
    max_retries=2
)


# --------------------------------------------------
# 3. 프롬프트 템플릿 생성
# --------------------------------------------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 비전공자에게 프로그래밍 기술을 "
            "쉽고 친절하게 설명하는 AI 강사입니다."
        ),
        (
            "human",
            """
안녕하세요. 저는 {name}입니다.

다음 주제에 대해 설명해주세요.

주제: {topic}

다음 형식으로 답변해주세요.

1. 핵심 개념
2. 쉬운 비유
3. 간단한 활용 사례
"""
        ),
    ]
)


# --------------------------------------------------
# 4. 체인 구성
# 프롬프트 → 모델 → 문자열 변환
# --------------------------------------------------
chain = prompt | model | StrOutputParser()


# --------------------------------------------------
# 5. 체인 실행
# --------------------------------------------------
try:
    response = chain.invoke(
        {
            "name": "한국 개발자",
            "topic": "LangChain",
        }
    )

    print("=== AI 응답 ===")
    print(response)

except Exception as error:
    print("OpenAI 모델 호출 중 오류가 발생했습니다.")
    print(f"오류 내용: {error}")

```

=== AI 응답 ===  
물론입니다.  
**LangChain**을 비전공자도 이해하기 쉽게, 그리고 개발자 관점에서 핵심만 정리해 설명드리겠습니다.

---

## 1. 핵심 개념

**LangChain**은  
**대규모 언어 모델(LLM)** 을 활용한 애플리케이션을 쉽게 만들 수 있게 도와주는 **프레임워크(도구 모음)** 입니다.

쉽게 말해, ChatGPT 같은 AI 모델을 단순히 “질문-답변” 용도로 쓰는 것을 넘어서서:

- 외부 데이터와 연결하고
- 여러 단계를 거치는 작업을 만들고
- 다른 도구(API, DB, 검색 등)와 연동하고
- 기억 기능을 넣어 대화형 서비스를 만들 수 있게 해줍니다.

### LangChain이 잘하는 것
- **프롬프트 관리**: LLM에게 어떤 식으로 물어볼지 구조화
- **체인(Chain)**: 여러 LLM 작업을 단계별로 연결
- **에이전트(Agent)**: 상황에 따라 LLM이 어떤 도구를 쓸지 판단
- **메모리(Memory)**: 이전 대화 내용을 기억
- **RAG(검색 결합 생성)**: 문서/DB에서 정보를 찾아 LLM 답변에 반영
- **도구 연결**: 검색, 계산기, API 호출 등 외부 기능과 연결

즉, LangChain은 **“LLM을 실제 서비스처럼 쓸 수 있게 만드는 연결 도구”**라고 이해하시면 됩니다.

---

## 2. 쉬운 비유

LangChain은 **요리사 + 조리도구 + 레시피북**에 비유할 수 있습니다.

- **LLM(ChatGPT 같은 모델)** = 뛰어난 요리사
- **LangChain** = 요리사가 일을 잘할 수 있게 도와주는 주방 시스템
- **체인(Chain)** = 요리 순서표
- **에이전트(Agent)** = 상황 보고 필요한 도구를 알아서 쓰는 셰프
- **메모리(Memory)** = “손님이 매운 걸 싫어한다” 같은 기록장
- **외부 데이터/도구** = 냉장고 재료, 계산기, 배달 앱

요리사가 아무리 뛰어나도  
재료를 가져오고, 순서를 정하고, 손님 취향을 기억하고, 필요한 도구를 쓰는 시스템이 있어야  
**실제로 좋은 음식**을 빠르게 만들 수 있죠.

LangChain도 마찬가지로,  
LLM을 **실용적인 서비스**로 만들도록 도와주는 프레임워크입니다.

---

## 3. 간단한 활용 사례

### 사례 1: 사내 문서 검색 챗봇
회사 규정, 매뉴얼, 기술 문서 PDF를 넣어두고  
직원이 질문하면 AI가 문서를 찾아 답해주는 챗봇을 만들 수 있습니다.

예:
- “연차 신청 절차가 뭐야?”
- “배포 전에 체크할 항목은?”
- “이 시스템 장애 대응 매뉴얼 보여줘”

이때 LangChain이 문서를 읽고 검색(RAG)해서 답변을 생성합니다.

---

### 사례 2: 고객 상담 자동화
쇼핑몰이나 SaaS 서비스에서 고객 문의가 들어오면:

- 주문 조회 API 호출
- 환불 규정 문서 확인
- 답변 초안 작성

같은 작업을 LangChain으로 연결할 수 있습니다.

---

### 사례 3: 개인 업무 도우미
예를 들어 이메일, 일정, 메모를 연결해서:

- “이번 주 회의 일정 요약해줘”
- “지난번 프로젝트 메모 기반으로 할 일 정리해줘”

처럼 개인 비서처럼 동작하는 도구를 만들 수 있습니다.

---

## 4. 더 간단한 초급 실습 코드

첫 수업에서는 체인과 출력 파서를 모두 설명하기 전에 다음 코드로 시작해도 됩니다.

```python
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY를 확인해주세요.")


model = ChatOpenAI(
    model="gpt-5.4-mini"
)

response = model.invoke(
    "LangChain이 무엇인지 비전공자가 이해할 수 있도록 설명해주세요."
)

print(response.content)
```

## 핵심변경 사항

```python
기존 방식                         현재 권장 방식
------------------------------------------------------------
langchain.llms.OpenAI          → langchain_openai.ChatOpenAI
langchain.prompts              → langchain_core.prompts
LLMChain(...)                  → prompt | model | parser
chain.run(...)                 → chain.invoke({...})
API 키 직접 입력               → .env 환경변수
일반 PromptTemplate            → ChatPromptTemplate
메시지 객체 직접 처리          → StrOutputParser로 문자열 변환
```


### 한 줄 정리
**LangChain은 LLM을 활용한 앱을 쉽게 만들기 위한 프레임워크이며, 문서 검색, 도구 연동, 대화 기억, 작업 자동화에 특히 유용합니다.**

원하시면 다음 단계로  
**“LangChain과 LlamaIndex 차이”** 또는 **“LangChain 기본 구조(Chain, Agent, RAG)”** 도 이어서 설명드릴게요.
