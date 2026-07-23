"""
1-6-1. 메모리의 필요성과 개념 - (4) 토큰 비용 최적화 3가지 방법
긴 대화에서 컨텍스트 토큰이 누적 증가하는 문제를 해결하는 기법 데모.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages
from _common import get_llm

# 실습용 긴 대화 기록 생성 (12개 메시지)
messages = []
for i in range(1, 7):
    messages.append(HumanMessage(content=f"{i}번째 질문입니다."))
    messages.append(AIMessage(content=f"{i}번째 질문에 대한 답변입니다."))


def method1_window_trimming():
    """방법 1: 윈도우 트리밍 - 최근 N개 메시지만 유지 (가장 단순)"""
    recent = messages[-10:]  # 리스트 슬라이싱만으로 구현
    print(f"[방법1] 전체 {len(messages)}개 → 최근 {len(recent)}개 유지")


def method2_token_trimming():
    """방법 2: 토큰 기반 트리밍 - trim_messages로 토큰 한도 내 유지"""
    llm = get_llm()
    trimmed = trim_messages(
        messages,
        max_tokens=100,      # 유지할 최대 토큰 수 (실습용으로 작게 설정)
        strategy="last",     # 최근 메시지 우선 유지
        token_counter=llm,   # 모델 기반 토큰 카운팅
    )
    print(f"[방법2] 전체 {len(messages)}개 → 토큰 한도 내 {len(trimmed)}개 유지")
    for m in trimmed:
        print("   -", m.type, ":", m.content)


def method3_summary():
    """방법 3: 요약 기반 - 오래된 메시지를 LLM 요약으로 대체 (정보 손실 최소화)"""
    llm = get_llm()
    old_messages = messages[:8]     # 오래된 메시지
    recent_messages = messages[8:]  # 최근 메시지

    old_text = "\n".join(f"{m.type}: {m.content}" for m in old_messages)
    summary = llm.invoke(f"다음 대화를 한 문장으로 요약: {old_text}")

    # 요약(SystemMessage) + 최근 메시지로 컨텍스트 재구성
    new_context = [SystemMessage(content=f"이전 대화 요약: {summary.content}")] + recent_messages
    print(f"[방법3] {len(messages)}개 → 요약 1개 + 최근 {len(recent_messages)}개")
    print("   요약:", summary.content)


if __name__ == "__main__":
    method1_window_trimming()
    method2_token_trimming()
    method3_summary()
