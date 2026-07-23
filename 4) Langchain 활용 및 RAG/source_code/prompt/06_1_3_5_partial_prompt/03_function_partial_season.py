"""함수가 반환하는 동적 값을 partial_variables로 사용."""

from datetime import datetime

from langchain_core.prompts import PromptTemplate


def get_current_season() -> str:
    """현재 월을 한국의 일반적인 계절 구분으로 변환합니다."""
    month = datetime.now().month
    if 3 <= month <= 5:
        return "봄"
    if 6 <= month <= 8:
        return "여름"
    if 9 <= month <= 11:
        return "가을"
    return "겨울"


prompt = PromptTemplate(
    template="{season}에 관찰하기 쉬운 대표 현상은 {phenomenon}입니다.",
    input_variables=["phenomenon"],
    partial_variables={"season": get_current_season},
)

print(prompt.format(phenomenon="계절에 따른 기온 변화"))
