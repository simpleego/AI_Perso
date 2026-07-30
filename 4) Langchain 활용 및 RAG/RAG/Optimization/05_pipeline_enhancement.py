"""실습 5: RAG Pipeline Enhancement - 질문 복잡도에 따라 검색 전략을 동적 선택."""

from typing import Literal

from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_classic.retrievers import MultiQueryRetriever


documents = [
    Document(page_content="일반휴학은 한 번에 최대 2학기이며 재학 중 총 6학기까지 가능하다.", metadata={"id": "P1"}),
    Document(page_content="군휴학은 복무 기간 동안 허용되며 일반휴학 사용 횟수에 포함하지 않는다.", metadata={"id": "P2"}),
    Document(page_content="일반휴학 신청은 개강 전까지 포털에서 하며 지도교수 승인이 필요하다.", metadata={"id": "P3"}),
    Document(page_content="군휴학 신청에는 입영통지서 사본을 첨부해야 하며 입영일 전후 14일 안에 신청한다.", metadata={"id": "P4"}),
    Document(page_content="일반휴학 중에는 등록금을 납부하지 않으며 납부 후 휴학한 등록금은 복학 학기로 이월한다.", metadata={"id": "P5"}),
    Document(page_content="군복무 중 취득한 일부 온라인 강좌 학점은 심사를 거쳐 인정할 수 있다.", metadata={"id": "P6"}),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
multi_retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever, llm=llm, include_original=True
)


class RouteDecision(BaseModel):
    """LLM 라우터가 반드시 선택해야 하는 구조화된 출력 형식."""

    strategy: Literal["direct", "multi_query"] = Field(
        description="단일 사실 질문은 direct, 비교·복합 질문은 multi_query"
    )
    reason: str = Field(description="선택 이유를 한 문장으로 설명")


router_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "질문의 검색 전략을 선택하라. 하나의 사실만 묻는 질문은 direct, "
            "둘 이상의 대상을 비교하거나 여러 조건을 묻는 질문은 multi_query를 선택하라.",
        ),
        ("human", "{question}"),
    ]
)

# with_structured_output(): 자유 텍스트가 아니라 RouteDecision 형식으로 라우팅 결과를 받는다.
router = router_prompt | llm.with_structured_output(RouteDecision)


def adaptive_retrieve(question: str) -> tuple[RouteDecision, list[Document]]:
    """질문 난이도를 판별하고 적합한 Retriever를 동적으로 실행한다."""
    decision = router.invoke({"question": question})
    if decision.strategy == "direct":
        docs = base_retriever.invoke(question)       # 빠르고 비용이 낮은 단일 검색
    else:
        docs = multi_retriever.invoke(question)      # 비교·복합 질문을 위한 다중 검색
    return decision, docs


questions = [
    "일반휴학은 한 번에 몇 학기까지 가능한가?",
    "일반휴학과 군휴학의 기간, 신청 서류, 등록금 처리를 비교해줘.",
]

for question in questions:
    decision, docs = adaptive_retrieve(question)
    print(f"\n질문: {question}")
    print(f"선택 전략: {decision.strategy} ({decision.reason})")
    for rank, doc in enumerate(docs, 1):
        print(f"{rank}. {doc.metadata['id']} | {doc.page_content}")

# 실습 과제:
# 1. "direct", "multi_query"별 LLM 호출 수와 검색 시간을 기록한다.
# 2. 성능과 비용을 함께 고려해 어떤 질문에 고급 전략을 사용할지 기준을 작성한다.
