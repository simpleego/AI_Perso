"""3-4. ToolRuntime: Context와 Store를 이용한 사용자별 선호도 관리."""

from __future__ import annotations

from dataclasses import dataclass

from langchain.agents import create_agent
from langchain.tools import ToolRuntime, tool
from langgraph.store.memory import InMemoryStore

from common import get_model, print_final_answer


@dataclass
class UserContext:
    """한 번의 실행 동안 바뀌지 않는 사용자 정보."""

    user_id: str
    user_name: str
    region: str = "KR"


@tool
def save_preference(
    category: str,
    value: str,
    runtime: ToolRuntime[UserContext],
) -> str:
    """현재 사용자의 선호도를 장기 메모리에 저장합니다.

    Args:
        category: 선호도 분류. 예: answer_style, food, music
        value: 저장할 선호 값
    """
    namespace = ("users", runtime.context.user_id, "preferences")
    runtime.store.put(namespace, category, {"value": value})
    return f"{runtime.context.user_name}님의 {category} 선호도를 저장했습니다."


@tool
def get_preference(
    category: str,
    runtime: ToolRuntime[UserContext],
) -> str:
    """현재 사용자의 저장된 선호도를 조회합니다.

    Args:
        category: 조회할 선호도 분류
    """
    namespace = ("users", runtime.context.user_id, "preferences")
    item = runtime.store.get(namespace, category)
    if item is None:
        return f"{category}에 저장된 선호도가 없습니다."
    return (
        f"사용자={runtime.context.user_name}, 지역={runtime.context.region}, "
        f"{category}={item.value['value']}"
    )


def main() -> None:
    store = InMemoryStore()
    agent = create_agent(
        model=get_model(),
        tools=[save_preference, get_preference],
        context_schema=UserContext,
        store=store,
        system_prompt=(
            "당신은 사용자 맞춤형 도우미입니다. 사용자가 선호도를 "
            "저장해 달라고 하면 save_preference를 사용하고, 확인해 달라고 "
            "하면 get_preference를 사용하세요. 한 요청에 두 작업이 있으면 "
            "저장 후 조회 순서로 모두 실행하세요."
        ),
    )

    context = UserContext(
        user_id="simple-001",
        user_name="심플",
        region="KR",
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "내 답변 스타일을 '초보자 수준의 쉬운 한국어'로 "
                        "저장한 다음, 저장된 값을 다시 확인해줘."
                    ),
                }
            ]
        },
        context=context,
    )
    print_final_answer(result)

    # 같은 store와 사용자 ID를 사용하면 이후 실행에서도 조회할 수 있습니다.
    second_result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "내 answer_style 선호도를 다시 알려줘.",
                }
            ]
        },
        context=context,
    )
    print_final_answer(second_result)


if __name__ == "__main__":
    main()

