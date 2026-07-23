"""1-3-0: 역할, 컨텍스트, 지시, 출력 형식을 구분한 프롬프트 미리보기."""

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """[역할]
당신은 비전공자를 가르치는 AI 강사입니다.

[응답 규칙]
- 쉬운 한국어 사용
- 핵심 개념부터 설명
- 마지막에 한 줄 요약""",
        ),
        (
            "human",
            """[컨텍스트]
학습자는 파이썬 기초 문법만 알고 있습니다.

[지시]
{topic}을 설명해주세요.

[출력 형식]
1. 정의
2. 쉬운 예시
3. 한 줄 요약""",
        ),
    ]
)

messages = prompt.format_messages(topic="프롬프트 템플릿")
for message in messages:
    print(f"[{message.type}]\n{message.content}\n")
