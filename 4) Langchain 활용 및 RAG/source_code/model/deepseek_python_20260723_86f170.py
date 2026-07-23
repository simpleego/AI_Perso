import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "이 시스템은 천문학 질문에 답변할 수 있습니다."),
    ("user", "{user_input}"),
])

model = ChatOpenAI(model="gpt-4o-mini", max_tokens=100)

chain = prompt | model.bind(max_tokens=10)
response = chain.invoke({"user_input": "태양계에서 가장 큰 행성은 무엇인가요?"})
print(response.content)