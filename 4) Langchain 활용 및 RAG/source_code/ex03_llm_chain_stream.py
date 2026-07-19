from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 설정)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# 프롬프트 템플릿
prompt = ChatPromptTemplate.from_template(
    "{topic}에 대해 간단히 설명해주세요."
)

# LLM
llm = init_chat_model("gpt-4o-mini")

# 체인 구성 (프롬프트 | LLM)
chain = prompt | llm | StrOutputParser()

stream = chain.stream({"topic":"인공지능"})
print("streaming 결과:")

for chunk in stream:
    print(chunk, end="", flush=True)

print("\n[OK] streaming 완료")
