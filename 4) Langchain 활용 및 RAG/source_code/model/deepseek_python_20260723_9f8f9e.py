import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_output_tokens=200,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "LLM은 어떤 원리로 작동하나요? 100자 이내로 설명해주세요."},
]

response = llm.invoke(messages)
print(response.content)