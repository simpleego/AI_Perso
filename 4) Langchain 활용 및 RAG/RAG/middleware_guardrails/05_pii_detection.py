"""실습 5: PII 탐지 - 내장 PIIMiddleware의 redact/mask/block 전략."""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware


# 이메일은 완전 삭제, 신용카드는 일부 마스킹한다.
protected_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    middleware=[
        # apply_to_input=True: 모델에 보내기 전에 사용자 입력을 보호한다.
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
    system_prompt="입력에서 확인되는 안전한 정보만 요약하세요. 개인정보 원문을 복원하지 마세요.",
)

safe_result = protected_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "상담 기록을 요약해줘. 이메일은 student@example.com이고 "
                    "테스트 카드 번호는 4111-1111-1111-1111이야."
                ),
            }
        ]
    }
)
print("[redact + mask 결과]")
print(safe_result["messages"][-1].content)

# block 전략은 민감정보가 있으면 모델 호출 자체를 허용하지 않는 엄격한 방식이다.
strict_agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[],
    middleware=[PIIMiddleware("credit_card", strategy="block", apply_to_input=True)],
)

print("\n[block 결과]")
try:
    strict_agent.invoke(
        {"messages": [{"role": "user", "content": "카드 4111-1111-1111-1111로 결제해줘."}]}
    )
except Exception as error:
    print("요청 차단:", error)

# 실습 과제:
# 1. email 전략을 mask와 hash로 바꾸어 출력 차이를 비교한다.
# 2. 실제 개인정보 대신 반드시 교사가 제공한 가상 테스트 데이터만 사용한다.
