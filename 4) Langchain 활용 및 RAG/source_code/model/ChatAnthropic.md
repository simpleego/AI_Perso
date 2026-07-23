```py
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0,
    max_tokens=200,
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "LLM은 어떤 원리로 작동하나요? 100자 이내로 설명해주세요."},
]

response = llm.invoke(messages)
print(response.content)
```
