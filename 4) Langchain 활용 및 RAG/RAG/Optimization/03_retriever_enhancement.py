"""실습 3: Retriever Enhancement - Hybrid 검색 후 Cross-Encoder 재정렬."""

from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.retrievers import EnsembleRetriever, ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker


documents = [
    Document(page_content="학칙 제27조: 재시험은 질병 또는 공결 사유로 정기시험에 응시하지 못한 학생에게 허용한다.", metadata={"id": "R1"}),
    Document(page_content="재시험 신청자는 시험일로부터 7일 안에 증빙 서류와 신청서를 학과에 제출해야 한다.", metadata={"id": "R2"}),
    Document(page_content="성적 이의신청은 성적 공시 기간에 담당 교원에게 온라인으로 제출한다.", metadata={"id": "R3"}),
    Document(page_content="학칙 제72조: 부정행위가 확인되면 해당 교과목의 성적을 F로 처리할 수 있다.", metadata={"id": "R4"}),
    Document(page_content="공결은 입원, 가족상, 공식 행사 참가 등 대학이 인정하는 결석 사유를 말한다.", metadata={"id": "R5"}),
    Document(page_content="추가 시험의 일시와 장소는 담당 교원이 학생에게 개별 통보한다.", metadata={"id": "R6"}),
    Document(page_content="중간고사 시험 범위는 1주차부터 7주차까지의 강의 내용이다.", metadata={"id": "R7"}),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# BM25는 "제27조", "재시험" 같은 정확한 키워드에 강하다.
bm25_retriever = BM25Retriever.from_documents(documents)
bm25_retriever.k = 6

# EnsembleRetriever: 키워드 검색과 의미 검색의 순위를 가중 결합한다.
hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.5, 0.5],
)

# 1차 검색은 Recall을 높이기 위해 넓게, 2차 재정렬은 Precision을 높이기 위해 좁게 수행한다.
cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
reranker = CrossEncoderReranker(model=cross_encoder, top_n=3)
optimized_retriever = ContextualCompressionRetriever(
    base_retriever=hybrid_retriever,
    base_compressor=reranker,
)

question = "아파서 정기시험을 못 봤을 때 재시험 신청 조건과 절차는?"
before = hybrid_retriever.invoke(question)
after = optimized_retriever.invoke(question)


def show(label: str, docs: list[Document]) -> None:
    print(f"\n[{label}]")
    for rank, doc in enumerate(docs, 1):
        print(f"{rank}. {doc.metadata['id']} | {doc.page_content}")


show("Hybrid 1차 후보", before)
show("Cross-Encoder 재정렬 상위 3개", after)

# 실습 과제: weights와 top_n을 변경하고 정답 문서 R1, R2, R5의 순위를 기록하라.
