"""실무형 예제: 실행 시점의 날짜를 함수 partial로 자동 삽입."""

from datetime import datetime

from langchain_core.prompts import PromptTemplate


def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


prompt = PromptTemplate(
    template="작성일: {date}\n주제: {topic}\n위 주제의 학습 목표를 3개 작성하세요.",
    input_variables=["topic"],
    partial_variables={"date": current_date},
)

print(prompt.format(topic="LangChain 프롬프트 템플릿"))
