"""5-4. Skills: 필요한 전문 지침만 도구로 불러오는 점진적 공개."""

from __future__ import annotations

from typing import Literal

from langchain.agents import create_agent
from langchain.tools import tool

from common import ask, get_model


SKILLS = {
    "sales_sql": """
[매출 분석 SQL 스킬]
- 테이블: sales(order_id, order_date, product_id, quantity, unit_price)
- 매출액: quantity * unit_price
- 월별 집계: DATE_FORMAT(order_date, '%Y-%m')
- 집계되지 않은 열은 GROUP BY에 포함한다.
- 읽기 전용 SELECT만 생성하며 DELETE/UPDATE/INSERT는 금지한다.
""",
    "inventory_sql": """
[재고 분석 SQL 스킬]
- 테이블: inventory(product_id, product_name, stock_qty, safety_stock)
- 부족 재고 조건: stock_qty < safety_stock
- 부족 수량: safety_stock - stock_qty
- 읽기 전용 SELECT만 생성하며 DELETE/UPDATE/INSERT는 금지한다.
""",
}


@tool
def load_sql_skill(
    skill_name: Literal["sales_sql", "inventory_sql"],
) -> str:
    """요청과 관련된 SQL 전문 지침과 스키마를 불러옵니다.

    Args:
        skill_name: 매출은 sales_sql, 재고는 inventory_sql
    """
    return SKILLS[skill_name]


def main() -> None:
    agent = create_agent(
        model=get_model(),
        tools=[load_sql_skill],
        system_prompt=(
            "당신은 SQL 비서입니다. 처음에는 스키마를 알지 못합니다. "
            "매출 질문에는 sales_sql, 재고 질문에는 inventory_sql 스킬을 "
            "반드시 먼저 로드하세요. 여러 영역이면 필요한 스킬을 모두 "
            "로드하세요. 로드된 지침만 사용하여 MySQL SELECT문과 설명을 "
            "작성하고 데이터 변경 SQL은 작성하지 마세요."
        ),
    )

    question = (
        input(
            "SQL 요청(기본값: 월별 매출과 안전재고 미달 상품을 조회해줘): "
        ).strip()
        or "월별 매출과 안전재고 미달 상품을 각각 조회하는 SQL을 작성해줘."
    )
    print("\n=== Skills 적용 결과 ===")
    print(ask(agent, question))


if __name__ == "__main__":
    main()

