from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일에 입력하세요.")
os.environ["OPENAI_API_KEY"] = api_key

llm = init_chat_model("gpt-4o-mini")

# 가상의 검색 함수
def retrieve_context(query: str) -> str:
    # 실제로는 벡터스토어 검색
    answer = f"LangChain은 LLM을 활용한 체인 구성 및 RAG를 지원하는 프레임워크입니다."
    return f"검색된 컨텍스트: {query}에 대한 정보..{answer}"

# RAG 체인 구성
rag_chain = (
    # 1. 쿼리와 컨텍스트 병렬 준비
    RunnableParallel(
        question=RunnablePassthrough(),
        context=RunnableLambda(lambda x: retrieve_context(x["question"]))
    )
    # 2. 프롬프트 생성
    | ChatPromptTemplate.from_template(
        """컨텍스트를 참고하여 질문에 답변하세요.

컨텍스트: {context}

질문: {question}

답변:"""
    )
    # 3. LLM 호출
    | llm
    # 4. 출력 파싱
    | StrOutputParser()
)

result = rag_chain.invoke({"question": "LangChain이란?"})
print(result)