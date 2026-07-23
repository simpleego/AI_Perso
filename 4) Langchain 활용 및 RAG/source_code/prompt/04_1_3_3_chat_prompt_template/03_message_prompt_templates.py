"""SystemMessagePromptTemplate과 HumanMessagePromptTemplate 활용."""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

system_template = SystemMessagePromptTemplate.from_template(
    "이 시스템은 {domain} 질문에 답변할 수 있습니다."
)
human_template = HumanMessagePromptTemplate.from_template("{user_input}")

chat_prompt = ChatPromptTemplate.from_messages(
    [system_template, human_template]
)

messages = chat_prompt.format_messages(
    domain="천문학",
    user_input="태양계에서 가장 큰 행성은 무엇인가요?",
)

for message in messages:
    print(f"[{message.type}] {message.content}")
