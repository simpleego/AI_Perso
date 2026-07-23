import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# OpenAI 모델
model = init_chat_model("gpt-4.1")
response = model.invoke("안녕하세요, 한국의 수도는 어디인가요?")
print(response.content)