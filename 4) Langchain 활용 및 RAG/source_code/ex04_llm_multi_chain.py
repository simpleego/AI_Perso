from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 설정)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = init_chat_model("gpt-4o-mini")

# 1단계: 한국어를 영어로 번역
translate_prompt = ChatPromptTemplate.from_template(
    "다음 한국어를 영어로 번역하세요: {korean_word}"
)

# 2단계: 영어 단어 설명
explain_prompt = ChatPromptTemplate.from_template(
    "다음 영어 단어를 한국어로 자세히 설명하세요: {english_word}"
)

# 체인 1: 번역
chain1 = translate_prompt | llm | StrOutputParser()

# 체인 2: 번역 결과를 입력으로 사용
chain2 = (
    {"english_word": chain1}
    | explain_prompt
    | llm
    | StrOutputParser()
)

# 실행
result = chain2.invoke({"korean_word": "인공지능"})
print(result)