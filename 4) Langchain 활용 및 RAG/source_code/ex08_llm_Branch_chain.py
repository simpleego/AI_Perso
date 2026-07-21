from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 설정)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = init_chat_model("gpt-4o-mini")

# 언어별 다른 프롬프트
korean_prompt = ChatPromptTemplate.from_template(
    "다음 한국어 질문에 한국어로 답변하세요: {question}"
)

english_prompt = ChatPromptTemplate.from_template(
    "Answer the following question in English: {question}"
)

default_prompt = ChatPromptTemplate.from_template(
    "Please answer: {question}"
)

# 언어 감지 함수
def detect_language(input_dict):
    question = input_dict.get("question", "")
    # 간단한 한글 감지
    if any('\uac00' <= char <= '\ud7a3' for char in question):
        return "korean"
    return "english"

# 조건부 분기
branch_chain = RunnableBranch(
    # (조건 함수, 실행할 체인) 튜플 목록
    (lambda x: detect_language(x) == "korean", korean_prompt | llm | StrOutputParser()),
    (lambda x: detect_language(x) == "english", english_prompt | llm | StrOutputParser()),
    # 기본값 (조건에 맞지 않을 때)
    default_prompt | llm | StrOutputParser()
)

# 테스트
result_kr = branch_chain.invoke({"question": "파이썬이란 무엇인가요?"})
result_en = branch_chain.invoke({"question": "What is Python?"})

print("한국어 질문 결과:", result_kr)
print("영어 질문 결과:", result_en)