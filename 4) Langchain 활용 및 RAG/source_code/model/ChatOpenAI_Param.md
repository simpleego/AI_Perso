```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

params = {
    "temperature": 0.7,
    "max_tokens": 100,
}
kwargs = {
    "frequency_penalty": 0.5,
    "presence_penalty": 0.5,
    "stop": ["\n"]
}

model = ChatOpenAI(model="gpt-4o-mini", **params, model_kwargs=kwargs)
response = model.invoke("태양계에서 가장 큰 행성은 무엇인가요?")
print(response.content)
```
