"""실습 1: Vector Store Retriever의 similarity 검색과 MMR 검색 비교."""

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def make_documents() -> list[Document]:
    """PDF 등에서 문서가 이미 로드되었다고 가정하고 실습용 Document를 만든다."""
    return [
        Document(
            page_content="AI개론은 인공지능의 역사, 탐색, 머신러닝의 기본 개념을 다룬다. 평가는 중간고사 30%, 기말고사 30%, 과제 30%, 출석 10%이다.",
            metadata={"id": "D1", "title": "AI개론 강의계획서"},
        ),
        Document(
            page_content="RAG 실습 수업은 문서 로딩, 분할, 임베딩, 벡터 검색을 학습한다. 평가는 프로젝트 50%, 실습 보고서 30%, 출석 20%이다.",
            metadata={"id": "D2", "title": "RAG 실습 강의계획서"},
        ),
        Document(
            page_content="RAG 프로젝트는 학교 규정 질의응답 챗봇을 만드는 팀 과제다. 검색 정확도 40%, 답변 근거성 30%, 발표 20%, 협업 10%로 평가한다.",
            metadata={"id": "D3", "title": "RAG 프로젝트 안내"},
        ),
        Document(
            page_content="벡터 데이터베이스는 문서 임베딩을 저장하고 의미적 유사도로 검색한다. FAISS와 Chroma가 대표적인 도구다.",
            metadata={"id": "D4", "title": "벡터 검색 노트"},
        ),
        Document(
            page_content="팀 프로젝트 제출 마감은 6월 14일 23시 59분이다. 보고서 PDF와 소스 코드 저장소 주소를 LMS에 제출한다.",
            metadata={"id": "D5", "title": "제출 공지"},
        ),
        Document(
            page_content="출석은 매주 수업 시작 후 10분 이내에 전자출결로 확인한다. 지각 3회는 결석 1회로 처리한다.",
            metadata={"id": "D6", "title": "출석 규정"},
        ),
    ]


def print_results(label: str, docs: list[Document]) -> None:
    print(f"\n[{label}] {len(docs)}개")
    for rank, doc in enumerate(docs, start=1):
        print(f"{rank}. {doc.metadata['id']} | {doc.metadata['title']}")
        print(f"   {doc.page_content}")


documents = make_documents()

# 한국어를 포함한 다국어 문장을 벡터로 바꾸는 임베딩 모델이다.
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

# from_documents(): 문서 임베딩을 계산하여 메모리 내 FAISS 인덱스를 만든다.
vectorstore = FAISS.from_documents(documents, embeddings)
query = "RAG 팀 프로젝트의 평가 기준과 제출 방법은?"

# as_retriever(): 벡터스토어를 표준 Retriever 인터페이스로 변환한다.
similarity_retriever = vectorstore.as_retriever(
    search_type="similarity", search_kwargs={"k": 3}
)
# invoke(): 질문 문자열을 입력해 관련 Document 목록을 받는다.
similarity_docs = similarity_retriever.invoke(query)
print_results("유사도 검색", similarity_docs)

# MMR은 관련성뿐 아니라 결과 간 다양성도 고려한다.
# fetch_k는 먼저 뽑을 후보 수, k는 최종 반환 수, lambda_mult가 작을수록 다양성을 중시한다.
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 6, "lambda_mult": 0.3},
)
mmr_docs = mmr_retriever.invoke(query)
print_results("MMR 검색", mmr_docs)

# 실습 과제: lambda_mult를 0.0, 0.5, 1.0으로 바꾸고 결과 순서의 차이를 설명하라.
