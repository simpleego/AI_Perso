"""
1-6-4. 단기 메모리 패턴 - (4) 메시지 요약 (Summarization)
트리밍/삭제는 정보 손실 발생 → 오래된 메시지를 "요약"으로 압축해 손실 최소화
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langgraph.checkpoint.memory import MemorySaver
from _common import check_api_key, GEMINI_MODEL


def main():
    check_api_key()

    # 요약 미들웨어: 컨텍스트가 임계치를 넘으면 오래된 메시지를 자동 요약
    # (요약용 모델은 저렴한 모델을 쓰는 것이 일반적 - 여기서는 동일한 무료 Gemini 사용)
    summarization = SummarizationMiddleware(
        model=GEMINI_MODEL,                  # 요약을 수행할 모델
        max_tokens_before_summary=500,       # 이 토큰 수를 넘으면 요약 발동 (실습용으로 작게)
        messages_to_keep=4,                  # 최근 4개 메시지는 원본 그대로 유지
    )

    agent = create_agent(
        GEMINI_MODEL,
        tools=[],
        checkpointer=MemorySaver(),
        middleware=[summarization],
    )

    config = {"configurable": {"thread_id": "summary-demo"}}

    # 요약이 발동될 만큼 대화를 길게 진행
    agent.invoke({"messages": [("user", "제 이름은 철수이고, 파이썬을 공부하는 학생입니다.")]}, config=config)
    topics = ["리스트와 튜플의 차이", "딕셔너리 사용법", "클래스와 객체", "예외 처리 방법"]
    for t in topics:
        agent.invoke({"messages": [("user", f"{t}에 대해 두 문장으로 설명해주세요.")]}, config=config)

    # 오래된 대화가 요약으로 대체된 상태에서도 핵심 정보(이름)를 기억하는지 확인
    result = agent.invoke(
        {"messages": [("user", "지금까지 무슨 얘기를 했고, 제 이름이 뭐였죠?")]}, config=config)
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
