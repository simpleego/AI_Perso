"""실습 2: 기본 검색 결과에서 질문과 관련된 문장만 LLM으로 압축."""

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor


documents = [
    Document(
        page_content=(
            "RAG 실습은 화요일 3교시에 진행한다. 수업에서는 FAISS를 사용한다. "
            "팀 프로젝트는 학교 규정 질의응답 챗봇을 구현하는 과제다. "
            "평가는 검색 정확도 40%, 답변 근거성 30%, 발표 20%, 협업 10%이다. "
            "발표 자료는 자유 형식이며 발표 시간은 팀당 10분이다."
        ),
        metadata={"id": "D1", "title": "RAG 실습 종합 안내"},
    ),
    Document(
        page_content=(
            "프로젝트 제출 마감은 6월 14일 23시 59분이다. "
            "보고서 PDF와 GitHub 저장소 주소를 LMS에 제출한다. "
            "저장소에는 README와 실행 방법을 반드시 포함해야 한다."
        ),
        metadata={"id": "D2", "title": "프로젝트 제출 안내"},
    ),
    Document(
        page_content=(
            "출석은 전자출결로 확인하며 지각 3회는 결석 1회로 처리한다. "
            "공결은 증빙 서류를 수업일로부터 7일 안에 제출해야 한다."
        ),
        metadata={"id": "D3", "title": "출석 안내"},
    ),
    Document(
        page_content=(
            "중간고사는 객관식과 단답형으로 구성된다. 시험 범위는 1주차부터 7주차이며 "
            "전자기기와 참고 자료를 사용할 수 없다."
        ),
        metadata={"id": "D4", "title": "중간고사 안내"},
    ),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
question = "RAG 팀 프로젝트의 평가 기준은 무엇인가?"

# 기본 검색기는 관련 문서 전체를 반환하므로 질문과 무관한 문장도 포함될 수 있다.
base_retriever = vectorstore.as_retriever(
    search_type="mmr", search_kwargs={"k": 3, "fetch_k": 4}
)
base_docs = base_retriever.invoke(question)

# LLMChainExtractor.from_llm(): 각 후보 문서에서 질문과 관련된 구절만 추출한다.
# 실행 전 환경 변수 OPENAI_API_KEY가 필요하다.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, max_tokens=500)
compressor = LLMChainExtractor.from_llm(llm)

# ContextualCompressionRetriever: 1차 검색기와 문서 압축기를 하나의 검색기로 결합한다.
compression_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=compressor,
)
compressed_docs = compression_retriever.invoke(question)

print(f"[압축 전] 문서 수={len(base_docs)}, 전체 글자 수={sum(len(d.page_content) for d in base_docs)}")
for doc in base_docs:
    print(f"- {doc.metadata['id']}: {doc.page_content}")

print(f"\n[압축 후] 문서 수={len(compressed_docs)}, 전체 글자 수={sum(len(d.page_content) for d in compressed_docs)}")
for doc in compressed_docs:
    print(f"- {doc.metadata['id']}: {doc.page_content}")

# 실습 과제: 질문을 "제출물과 마감 시각은?"으로 바꾸고 압축 전후의 글자 수를 비교하라.
