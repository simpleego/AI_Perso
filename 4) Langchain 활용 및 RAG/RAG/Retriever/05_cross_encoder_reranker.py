"""실습 5: Bi-Encoder로 넓게 검색한 뒤 Cross-Encoder로 정밀 재정렬."""

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker


documents = [
    Document(page_content="RAG 프로젝트는 검색 정확도 40점, 답변 근거성 30점으로 평가한다.", metadata={"id": "D1"}),
    Document(page_content="검색 성능 평가는 준비된 20개 질문에서 정답 문서가 상위 3개 안에 포함되는지 측정한다.", metadata={"id": "D2"}),
    Document(page_content="답변 생성 모델의 문체는 간결해야 하며 모든 답변은 한국어로 작성한다.", metadata={"id": "D3"}),
    Document(page_content="프로젝트 발표 점수는 내용 구성, 시간 준수, 질의응답으로 평가한다.", metadata={"id": "D4"}),
    Document(page_content="검색기가 관련 문서를 찾지 못하면 모델은 모른다고 답해야 한다.", metadata={"id": "D5"}),
    Document(page_content="최종 보고서에는 Precision@3, Recall@3, 실패 사례 분석을 포함한다.", metadata={"id": "D6"}),
    Document(page_content="임베딩 모델은 문장 의미를 벡터로 변환하여 빠른 후보 검색을 가능하게 한다.", metadata={"id": "D7"}),
    Document(page_content="Cross-Encoder는 질문과 후보 문서를 함께 읽어 관련성 점수를 직접 계산한다.", metadata={"id": "D8"}),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)

# 1단계: 빠른 Bi-Encoder 벡터 검색으로 recall 중심의 후보 6개를 가져온다.
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# HuggingFaceCrossEncoder: 질문-문서 쌍을 함께 입력하여 관련성 점수를 계산한다.
cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

# CrossEncoderReranker: 후보 문서를 점수순으로 재정렬하고 상위 top_n개만 남긴다.
reranker = CrossEncoderReranker(model=cross_encoder, top_n=3)

# ContextualCompressionRetriever는 여기서 '내용 추출'이 아니라 '재정렬+선별' 파이프라인 역할을 한다.
rerank_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=reranker,
)

question = "RAG 검색 성능은 어떤 지표와 절차로 평가하나요?"
before = base_retriever.invoke(question)
after = rerank_retriever.invoke(question)

print("[1차 Bi-Encoder 후보]")
for rank, doc in enumerate(before, 1):
    print(f"{rank}. {doc.metadata['id']} | {doc.page_content}")

print("\n[Cross-Encoder 재정렬 후]")
for rank, doc in enumerate(after, 1):
    print(f"{rank}. {doc.metadata['id']} | {doc.page_content}")

# 실습 과제: top_n을 1, 3, 5로 바꾸고 정확도와 추론 비용의 관계를 설명하라.
