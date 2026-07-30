"""실습 3: Custom Middleware - 도구 호출 로깅과 비즈니스 규칙 검증."""

import json
import time

from langchain.agents import create_agent
from langchain.agents.middleware import before_model, after_model, wrap_tool_call
from langchain.tools import tool
from langchain_core.messages import ToolMessage


@tool
def calculate_scholarship(gpa: float, completed_credits: int) -> str:
    """평점과 이수학점으로 성적우수 장학금 대상 여부를 판정한다."""
    eligible = gpa >= 3.5 and completed_credits >= 12
    return "신청 가능" if eligible else "신청 불가"


@before_model
def log_input(request, state):
    """매 모델 호출 전에 입력 메시지 유형과 길이를 기록한다."""
    last = state["messages"][-1]
    print(f"[모델 입력] type={last.type}, length={len(str(last.content))}")
    return None


@after_model
def log_output(request, state):
    """매 모델 호출 후 모델이 선택한 도구와 인자를 기록한다."""
    last = state["messages"][-1]
    for call in getattr(last, "tool_calls", []):
        print("[모델 출력/도구 선택]", call["name"], json.dumps(call["args"], ensure_ascii=False))
    return None


# wrap_tool_call은 도구 실행을 감싸므로 사전 검증, 시간 측정, 오류 변환에 적합하다.
@wrap_tool_call
def validate_and_monitor_tool(request, handler):
    args = request.tool_call["args"]

    # 대학 비즈니스 규칙을 도구 본체와 분리하여 횡단 관심사로 처리한다.
    if "gpa" in args and not 0.0 <= args["gpa"] <= 4.5:
        return ToolMessage(
            content="검증 실패: 평점은 0.0부터 4.5 사이여야 합니다.",
            tool_call_id=request.tool_call["id"],
        )

    started = time.perf_counter()
    try:
        return handler(request)  # 실제 도구를 정확히 한 번 실행한다.
    except Exception as error:
        return ToolMessage(
            content=f"도구 오류가 안전하게 처리되었습니다: {error}",
            tool_call_id=request.tool_call["id"],
        )
    finally:
        print(f"[도구 실행 시간] {time.perf_counter() - started:.4f}초")


agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[calculate_scholarship],
    middleware=[log_input, log_output, validate_and_monitor_tool],
    system_prompt="장학금 자격 계산은 반드시 도구를 사용하세요.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "평점 3.8, 이수학점 15학점이면 장학금 신청이 가능해?"}]}
)
print("\n최종 답변:", result["messages"][-1].content)

# 실습 과제: 평점 5.0을 요청해 미들웨어 검증 메시지가 Agent 답변에 반영되는지 확인하라.
