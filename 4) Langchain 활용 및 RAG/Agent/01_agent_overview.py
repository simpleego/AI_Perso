"""3-1. Agent 개요: 질문에 따라 스스로 도구를 선택하는 에이전트."""

from langchain.agents import create_agent
from langchain.tools import tool

from common import get_model, print_final_answer


@tool
def get_product_price(product_name: str) -> int:
    """상품 이름으로 실습용 상품 가격(원)을 조회합니다."""
    prices = {
        "무선 키보드": 45000,
        "무선 마우스": 30000,
        "USB 허브": 25000,
    }
    return prices.get(product_name, 0)


@tool
def calculate_discount(price: int, discount_rate: float) -> dict:
    """가격과 할인율(%)을 받아 할인 금액과 최종 가격을 계산합니다."""
    discount = round(price * discount_rate / 100)
    return {
        "original_price": price,
        "discount_rate": discount_rate,
        "discount_amount": discount,
        "final_price": price - discount,
    }


def main() -> None:
    agent = create_agent(
        model=get_model(),
        tools=[get_product_price, calculate_discount],
        system_prompt=(
            "당신은 쇼핑 도우미입니다. 상품 가격은 반드시 "
            "get_product_price로 조회하고, 할인 계산은 반드시 "
            "calculate_discount로 수행하세요. 계산 결과는 원 단위로 "
            "명확하게 설명하세요."
        ),
    )

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "무선 키보드 가격을 조회하고 15% 할인 가격을 계산해줘.",
                }
            ]
        }
    )
    print_final_answer(result)


if __name__ == "__main__":
    main()

