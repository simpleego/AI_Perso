"""2-튜플 메시지 목록으로 ChatPromptTemplate 생성."""

from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "이 시스템은 천문학 질문에 한국어로 답변합니다."),
        ("human", "{user_input}"),
    ]
)

messages = chat_prompt.format_messages(
    user_input="태양계에서 가장 큰 행성은 무엇인가요?"
)

for message in messages:
    print(type(message).__name__)
    print(message.content)
    print()
