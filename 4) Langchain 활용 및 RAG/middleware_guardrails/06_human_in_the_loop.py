"""실습 6: Human-in-the-Loop - 공지 발송 전 승인·수정·거부."""

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, InterruptOnConfig
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


# 실제 전송 대신 콘솔에 기록하는 안전한 모의 도구다.
@tool
def send_course_notice(channel: str, title: str, body: str) -> str:
    """학생들에게 강의 공지사항을 발송한다."""
    print(f"[모의 발송 실행] channel={channel}, title={title}, body={body}")
    return f"{channel} 채널에 '{title}' 공지를 발송했습니다."


# HumanInTheLoopMiddleware는 지정된 고위험 도구 호출을 실행 직전에 중단한다.
hitl = HumanInTheLoopMiddleware(
    interrupt_on={
        "send_course_notice": InterruptOnConfig(
            allowed_decisions=["approve", "edit", "reject"],
            description="학생 전체에게 공지하기 전 담당 교원의 검토가 필요합니다.",
        )
    },
    action_request_description_prefix="다음 외부 발송 작업을 검토하세요:",
)

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[send_course_notice],
    middleware=[hitl],
    # HITL은 중단 상태를 저장했다 같은 thread_id로 재개해야 하므로 체크포인터가 필수다.
    checkpointer=InMemorySaver(),
    system_prompt="사용자 요청에 맞는 간결한 강의 공지를 작성하고 발송 도구를 사용하세요.",
)

config = {"configurable": {"thread_id": "middleware-lab-hitl-001"}}
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "LMS에 '보강 안내' 제목으로 금요일 6교시 보강 공지를 보내줘.",
            }
        ]
    },
    config=config,
)

if "__interrupt__" in result:
    interrupt = result["__interrupt__"][0]
    action_requests = interrupt.value["action_requests"]

    print("[승인 대기 작업]")
    for index, action in enumerate(action_requests, 1):
        print(f"{index}. {action['name']}: {action['args']}")

    # 수업에서는 아래 결정을 approve/edit/reject로 바꾸어 각각 실행한다.
    decision = {"type": "approve"}

    # Command(resume=...): 동일 thread_id의 저장된 실행 지점에서 작업을 재개한다.
    final_result = agent.invoke(
        Command(resume={"decisions": [decision]}),
        config=config,
    )
    print("\n[최종 결과]", final_result["messages"][-1].content)
else:
    print("예상과 달리 인터럽트 없이 완료되었습니다.")

# 실습 과제:
# 1. edit 결정에 수정된 args를 넣어 공지 제목과 본문을 변경한다.
# 2. reject 결정과 feedback을 넣어 발송이 실행되지 않는지 확인한다.
