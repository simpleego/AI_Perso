from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

from dotenv import load_dotenv
import os, sys
from typing import Dict, Any

from langchain_openai import ChatOpenAI


"""
RAG(Retrieval-Augmented Generation) 스타일 멀티 체인 예제
- 병렬 처리로 쿼리와 컨텍스트 동시 준비
- 검색된 컨텍스트를 포함(참고)하여 더 정확한 답변 생성
"""

# .env 파일 로드
load_dotenv()

# Windows 콘솔에서 UTF-8 출력을 강제 설정
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# API 키 설정
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다. .env 파일에 입력하세요.")
os.environ["OPENAI_API_KEY"] = api_key

# ============================================================================
# 가상의 지식 베이스 (실제는 벡터스토어 검색으로 대체)
# ============================================================================
KNOWLEDGE_BASE = {
    "langchain": """LangChain은 언어 모델 애플리케이션 개발을 위한 프레임워크입니다.
- 주요 기능: 체이닝, 메모리 관리, 에이전트, RAG 지원
- 지원되는 모델: OpenAI, Anthropic, Hugging Face 등 여러 LLM 제공자
- 핵심 컴포넌트: Prompts, LLMs, Output Parsers, Runnables
- 사용 사례: 챗봇, QA 시스템, 문서 분석, 코드 생성
- 최신 버전에서는 LCEL (LangChain Expression Language) 도입""",
    
    "python": """Python은 1991년 귀도 반 로썸이 만든 인터프리터 언어입니다.
- 특징: 간결한 문법, 강력한 라이브러리, 높은 생산성
- 주요 용도: 웹 개발, 데이터 과학, AI/ML, 자동화
- 인기 라이브러리: NumPy, Pandas, TensorFlow, PyTorch, Django
- Python의 장점: 배우기 쉬움, 커뮤니티 활발, 크로스 플랫폼 지원""",
    
    "artificial-intelligence": """인공지능(AI)은 인간의 지능을 모방하는 컴퓨터 시스템입니다.
- 주요 분야: 머신러닝, 자연어처리, 컴퓨터 비전, 음성인식
- 머신러닝 종류: 지도학습, 비지도학습, 강화학습
- 현대 AI 기술: 딥러닝, 트랜스포머, LLM(대규모 언어 모델)
- 응용 분야: 추천 시스템, 자동 번역, 이미지 분석, 챗봇""",
}

def retrieve_context(query: Dict[str, Any]) -> str:
    """
    쿼리에 기반한 컨텍스트 검색 (벡터스토어 검색 시뮬레이션)
    
    Args:
        query: 'question' 키를 포함하는 딕셔너리
        
    Returns:
        검색된 컨텍스트 문자열
    """
    question = query.get("question", "").lower()
    
    # 키워드 기반 검색
    best_match = None
    best_score = 0
    
    for keyword, content in KNOWLEDGE_BASE.items():
        # 간단한 키워드 매칭 (실제는 임베딩 유사도 사용)
        keywords_in_question = question.split()
        score = sum(1 for kw in keywords_in_question if kw in keyword)
        
        if score > best_score:
            best_score = score
            best_match = content
    
    # 매칭이 없으면 첫 번째 항목 반환 (기본값)
    if best_match is None:
        best_match = list(KNOWLEDGE_BASE.values())[0]
    
    return best_match



# 가상의 검색 함수
def retrieve_context(query: str) -> str:
    # 실제로는 벡터스토어 검색
    answer = f"LangChain은 LLM을 활용한 체인 구성 및 RAG를 지원하는 프레임워크입니다."
    return f"검색된 컨텍스트: {query}에 대한 정보..{answer}"

def create_rag_chain(llm: ChatOpenAI) -> RunnableParallel:
    """
    RAG 스타일 멀티 체인 생성
    
    Args:
        llm: ChatOpenAI 인스턴스
        
    Returns:
        구성된 RAG 체인
    """
    
    # RAG 체인 구성
    # 1. 쿼리와 컨텍스트를 병렬로 준비
    rag_chain = (
        RunnableParallel(
            question=RunnablePassthrough(),
            context=RunnableLambda(retrieve_context)
        )
        # 2. 프롬프트 생성
        | ChatPromptTemplate.from_template(
            """당신은 지식이 풍부한 AI 어시스턴트입니다.
주어진 컨텍스트를 참고하여 사용자의 질문에 정확하고 자세하게 답변하세요.

컨텍스트:
{context}

질문: {question}

답변:"""
        )
        # 3. LLM 호출
        | llm
        # 4. 출력 파싱
        | StrOutputParser()
    )
    
    return rag_chain


# RAG 체인 구성
# rag_chain = (
#     # 1. 쿼리와 컨텍스트 병렬 준비
#     RunnableParallel(
#         question=RunnablePassthrough(),
#         context=RunnableLambda(lambda x: retrieve_context(x["question"]))
#     )
#     # 2. 프롬프트 생성
#     | ChatPromptTemplate.from_template(
#         """컨텍스트를 참고하여 질문에 답변하세요.

# 컨텍스트: {context}

# 질문: {question}

# 답변:"""
#     )
#     # 3. LLM 호출
#     | llm
#     # 4. 출력 파싱
#     | StrOutputParser()
# )

# result = rag_chain.invoke({"question": "LangChain이란?"})
# print(result)

def main()-> None:

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    # RAG 체인 생성
    rag_chain = create_rag_chain(llm)
    
    # 테스트 질문
    test_question = "LangChain의 주요 기능은 무엇인가요?"

    # 테스트 케이스
    test_cases = [
        {
            "question": "LangChain이란 무엇인가요?",
            "description": "LangChain 설명"
        },
        {
            "question": "Python의 주요 특징과 용도는?",
            "description": "Python 정보"
        },
        {
            "question": "인공지능의 주요 분야에는 어떤 것들이 있나요?",
            "description": "AI 분야 설명"
        },
        {
            "question": "머신러닝이란 무엇입니까?",
            "description": "머신러닝에 대한 질문"
        },
    ]


    # 각 테스트 케이스 실행
    for idx, test_case in enumerate(test_cases, 1):
        question = test_case["question"]
        description = test_case["description"]
        
        print(f"{'='*80}")
        print(f"[테스트 {idx}] {description}")
        print(f"{'='*80}")
        print(f"질문: {question}\n")
        
        try:
            # RAG 체인 실행
            # 이 과정에서:
            # 1. 질문이 RunnablePassthrough로 그대로 전달
            # 2. 동시에 retrieve_context에 전달되어 관련 컨텍스트 검색
            # 3. 검색된 컨텍스트와 질문으로 프롬프트 생성
            # 4. LLM이 답변 생성
            result = rag_chain.invoke({"question": question})
            
            print(f"응답:\n{result}\n")
            
        except Exception as e:
            print(f"[ERROR] 응답 생성 실패: {e}\n")
    
    # RAG 체인 실행
    result = rag_chain.invoke({"question": test_question})
    
    print("질문:", test_question)
    print("응답:", result)
    # 추가 설명
    print("RAG 체인 동작 원리:")
    print("1. RunnableParallel: 쿼리와 컨텍스트를 동시에 처리")
    print("2. RunnablePassthrough: 질문을 그대로 통과")
    print("3. RunnableLambda(retrieve_context): 관련 컨텍스트 검색")
    print("4. ChatPromptTemplate: 컨텍스트와 질문 조합하여 프롬프트 생성")
    print("5. ChatOpenAI: 결합된 입력으로 답변 생성")
    print("6. StrOutputParser: 최종 결과를 문자열로 파싱")

if __name__ == "__main__":
    main()