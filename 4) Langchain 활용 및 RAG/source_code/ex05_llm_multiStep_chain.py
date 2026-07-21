from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# API 키 설정 (환경 변수 또는 직접 설정)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = init_chat_model("gpt-4o-mini")

# 3단계 처리: 주제 분석 → 개요 작성 → 본문 작성
analyze_prompt = ChatPromptTemplate.from_template(
    "다음 주제의 핵심 키워드 3개를 추출하세요: {topic}"
)

outline_prompt = ChatPromptTemplate.from_template(
    """다음 키워드를 바탕으로 글의 개요를 작성하세요:
키워드: {keywords}
원본 주제: {topic}"""
)

content_prompt = ChatPromptTemplate.from_template(
    """다음 개요를 바탕으로 300자 내외의 글을 작성하세요:
개요: {outline}"""
)

# 체인 구성
chain = (
    {"topic": RunnablePassthrough()}
    | RunnablePassthrough.assign(
        keywords=analyze_prompt | llm | StrOutputParser()
    )
    | RunnablePassthrough.assign(
        outline=outline_prompt | llm | StrOutputParser()
    )
    | content_prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke("기후 변화와 지속 가능한 발전")
print(result)