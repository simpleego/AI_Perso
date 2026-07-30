"""실습 3: BM25 키워드 검색과 벡터 의미 검색을 결합한 하이브리드 검색."""

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.retrievers import EnsembleRetriever


documents = [
    Document(page_content="RAG101 프로젝트는 검색 증강 생성 챗봇 구현 과제다.", metadata={"id": "D1"}),
    Document(page_content="검색 정확도는 전체 프로젝트 점수의 40%를 차지한다.", metadata={"id": "D2"}),
    Document(page_content="문서에서 근거를 찾아 답변에 출처를 표시하면 근거성 점수를 받는다.", metadata={"id": "D3"}),
    Document(page_content="RAG101 결과물은 보고서 PDF와 GitHub 저장소 주소다.", metadata={"id": "D4"}),
    Document(page_content="과제 식별 코드 RAG101의 제출 마감은 6월 14일이다.", metadata={"id": "D5"}),
    Document(page_content="AI개론 중간고사는 4월 22일에 실시한다.", metadata={"id": "D6"}),
]

# BM25Retriever.from_documents(): 단어가 정확히 일치하는 문서에 강한 키워드 검색기.
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 3

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# EnsembleRetriever: 각 검색기의 순위를 가중 Reciprocal Rank 방식으로 결합한다.
# 정확한 코드명이 중요하므로 BM25 가중치를 조금 높였다.
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.6, 0.4],
)

query = "RAG101 과제에서 검색 품질이 차지하는 비율은?"


def show(label: str, docs: list[Document]) -> None:
    print(f"\n[{label}]")
    for rank, doc in enumerate(docs, 1):
        print(f"{rank}. {doc.metadata['id']} | {doc.page_content}")


show("BM25", bm25_retriever.invoke(query))
show("Vector", vector_retriever.invoke(query))
show("Ensemble", ensemble_retriever.invoke(query)[:3])

# 실습 과제: weights를 [0.2, 0.8]로 바꾼 뒤 정확한 식별 코드와 의미 검색의 순위를 비교하라.
