"""실습 1: Query Enhancement - 모호한 질문을 Multi Query로 확장한다."""

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.retrievers import MultiQueryRetriever


# 문서는 이미 로드되었다고 가정하고 학생들이 이해하기 쉬운 학사규정 문서를 생성한다.
documents = [
    Document(
        page_content="재학생은 직전 학기 평점평균이 3.5 이상이면 성적우수 장학금을 신청할 수 있다.",
        metadata={"id": "Q1", "source": "장학금 규정", "section": "성적우수"},
    ),
    Document(
        page_content="성적우수 장학금은 등록금의 50%를 지원하며 국가장학금과 등록금 범위 안에서 중복 수혜할 수 있다.",
        metadata={"id": "Q2", "source": "장학금 규정", "section": "지원금액"},
    ),
    Document(
        page_content="장학금 신청 기간은 매 학기 개강 30일 전부터 14일 전까지이며 학생지원포털에서 신청한다.",
        metadata={"id": "Q3", "source": "장학금 신청 안내", "section": "신청방법"},
    ),
    Document(
        page_content="가계곤란 장학금은 소득구간과 성적을 함께 심사하며 소득구간 증빙 서류가 필요하다.",
        metadata={"id": "Q4", "source": "장학금 규정", "section": "가계곤란"},
    ),
    Document(
        page_content="직전 학기 12학점 미만을 이수한 학생은 성적우수 장학금 선발 대상에서 제외한다.",
        metadata={"id": "Q5", "source": "장학금 규정", "section": "선발제외"},
    ),
    Document(
        page_content="교환학생 지원자는 평점평균 3.0 이상과 공인 외국어 성적을 갖추어야 한다.",
        metadata={"id": "Q6", "source": "국제교류 안내", "section": "지원자격"},
    ),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# MultiQueryRetriever.from_llm(): 하나의 모호한 질문을 여러 관점의 검색어로 바꾼다.
# 실행 전 OPENAI_API_KEY 환경 변수가 필요하다.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm,
    include_original=True,  # 생성 쿼리뿐 아니라 원래 질문의 검색 결과도 포함한다.
)

question = "공부 잘하면 받는 지원금은 어떻게 받아?"

# 기준선: 사용자의 표현을 그대로 사용한 단일 벡터 검색.
baseline_docs = base_retriever.invoke(question)
# 최적화: 여러 관점의 쿼리로 검색한 뒤 중복 문서를 제거하여 반환.
enhanced_docs = multi_retriever.invoke(question)


def show(label: str, docs: list[Document]) -> None:
    print(f"\n[{label}] {len(docs)}개")
    for rank, doc in enumerate(docs, 1):
        print(f"{rank}. {doc.metadata['id']} | {doc.metadata['section']} | {doc.page_content}")


show("단일 쿼리", baseline_docs)
show("Multi Query", enhanced_docs)

# 정답 문서 집합을 이용해 검색 재현율(Recall)을 간단히 비교한다.
relevant_ids = {"Q1", "Q2", "Q3", "Q5"}


def recall_at_results(docs: list[Document]) -> float:
    found = {doc.metadata["id"] for doc in docs} & relevant_ids
    return len(found) / len(relevant_ids)


print(f"\n단일 쿼리 Recall={recall_at_results(baseline_docs):.2f}")
print(f"Multi Query Recall={recall_at_results(enhanced_docs):.2f}")

# 실습 과제: 질문을 "장학금 알려줘"로 더 모호하게 바꾸고 검색 문서와 Recall을 비교하라.
