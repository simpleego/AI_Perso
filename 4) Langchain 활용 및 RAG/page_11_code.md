# 고급 프롬프트 패턴

- 역할 기반 프롬프팅
- Few-Shot 학습
- Chain-of-Throught

---  

```python
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI


# ==================================================
# 0. 공통 설정
# ==================================================
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
    timeout=30,
    max_retries=2,
)

parser = StrOutputParser()


def print_result(title: str, result: str) -> None:
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)
    print(result)


# ==================================================
# 1. 역할 기반 프롬프팅
# ==================================================
role_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
당신은 {role}입니다.
비전공자가 이해할 수 있도록 전문 용어를 쉽게 설명하세요.
간단한 예시를 포함해 주세요.
""",
        ),
        ("human", "{query}"),
    ]
)

role_chain = role_prompt | model | parser

role_result = role_chain.invoke(
    {
        "role": "10년 경력의 AI 강사",
        "query": "LangChain의 역할을 쉽게 설명해주세요.",
    }
)

print_result("1. 역할 기반 프롬프팅", role_result)


# ==================================================
# 2. Few-Shot 프롬프팅
# ==================================================

# 모델에게 보여줄 예시
examples = [
    {
        "input": "배송이 너무 늦어요.",
        "output": "배송 지연으로 불편을 드려 죄송합니다. 배송 상황을 확인해드리겠습니다.",
    },
    {
        "input": "상품을 환불하고 싶어요.",
        "output": "환불을 원하시는군요. 확인 후 환불 절차를 친절하게 안내해드리겠습니다.",
    },
]

# 예시 하나의 입력·출력 형식
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)

# 여러 예시를 하나의 프롬프트로 구성
few_shot_examples = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

few_shot_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "당신은 친절한 고객센터 상담원입니다. "
            "예시와 같은 말투로 고객에게 답변하세요.",
        ),
        few_shot_examples,
        ("human", "{input}"),
    ]
)

few_shot_chain = few_shot_prompt | model | parser

few_shot_result = few_shot_chain.invoke(
    {
        "input": "받은 상품이 파손되어 있어요.",
    }
)

print_result("2. Few-Shot 프롬프팅", few_shot_result)


# ==================================================
# 3. 단계적 추론 프롬프팅
# ==================================================
reasoning_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
당신은 논리적으로 문제를 해결하는 수학 강사입니다.

내부 사고 과정 전체를 그대로 출력하지 말고,
사용자가 이해하는 데 필요한 핵심 판단 근거만 요약하세요.
""",
        ),
        (
            "human",
            """
다음 문제를 해결하세요.

문제:
{query}

다음 형식으로 답변하세요.

1. 핵심 정보
2. 계산 또는 판단 근거
3. 최종 답
""",
        ),
    ]
)

reasoning_chain = reasoning_prompt | model | parser

reasoning_result = reasoning_chain.invoke(
    {
        "query": "연필 3자루의 가격이 1,500원이라면, 연필 8자루의 가격은 얼마인가요?",
    }
)

print_result("3. 단계적 추론 프롬프팅", reasoning_result)
```

## 세 가지 프롬프트의 차이

| 프롬프트 방식  | 핵심 목적                 | 코드의 주요 부분            |
| -------- | --------------------- | -------------------- |
| 역할 기반    | 특정 전문가의 관점과 말투 부여     | `당신은 {role}입니다`      |
| Few-Shot | 입력·출력 예시를 통해 답변 형식 유도 | `examples`           |
| 단계적 추론   | 복잡한 문제를 구조화하여 해결      | 핵심 정보 → 판단 근거 → 최종 답 |

세 번째 예제는 모델의 내부 사고 과정 전체를 요구하는 대신, 학습자가 확인할 수 있는 **핵심 판단 근거와 최종 답**을 구조적으로 출력하도록 구성했습니다. 이는 수업에서도 결과를 비교하고 평가하기 쉬운 방식입니다.

[1]: https://reference.langchain.com/python/langchain-core/prompts/chat/ChatPromptTemplate?utm_source=chatgpt.com "ChatPromptTemplate | langchain_core"
