"""실습 4: LLM이 만든 다중 쿼리의 검색 결과를 RRF로 융합."""

from collections import defaultdict

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI


documents = [
    Document(page_content="RAG 팀 과제의 검색 정확도 배점은 40점이다.", metadata={"id": "D1"}),
    Document(page_content="질의응답 시스템은 질문과 의미가 가까운 학교 규정 문서를 찾아야 한다.", metadata={"id": "D2"}),
    Document(page_content="답변에는 참고한 학칙 문서의 제목과 조항 번호를 출처로 표시한다.", metadata={"id": "D3"}),
    Document(page_content="근거가 없는 내용을 생성하면 답변 근거성 항목에서 감점한다.", metadata={"id": "D4"}),
    Document(page_content="프로젝트 평가는 검색 정확도 40%, 근거성 30%, 발표 20%, 협업 10%다.", metadata={"id": "D5"}),
    Document(page_content="팀별 발표에서는 시스템 구조와 검색 성능 실험 결과를 설명한다.", metadata={"id": "D6"}),
    Document(page_content="최종 보고서에는 Precision@k와 Recall@k 측정 결과를 포함한다.", metadata={"id": "D7"}),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)
vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 검색 질의 생성기다. 원래 질문과 다른 관점의 한국어 검색 질의 4개를 "
            "한 줄에 하나씩만 출력하라. 번호나 설명은 쓰지 마라.",
        ),
        ("human", "{question}"),
    ]
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# LCEL의 | 연산자로 프롬프트 → 모델 → 문자열 파서를 연결한다.
query_generator = prompt | llm | StrOutputParser()


def generate_queries(question: str) -> list[str]:
    """원본 질문을 포함해 서로 다른 관점의 검색 질의 목록을 만든다."""
    generated = query_generator.invoke({"question": question})
    variants = [line.strip("-• 1234567890.") for line in generated.splitlines() if line.strip()]
    return [question, *variants[:4]]


def reciprocal_rank_fusion(
    result_lists: list[list[Document]], rrf_k: int = 60
) -> list[tuple[Document, float]]:
    """여러 순위 목록을 RRF_score = Σ 1/(k+rank)로 병합한다."""
    scores: dict[str, float] = defaultdict(float)
    doc_by_id: dict[str, Document] = {}
    for docs in result_lists:
        for rank, doc in enumerate(docs, start=1):
            doc_id = doc.metadata["id"]
            doc_by_id[doc_id] = doc
            scores[doc_id] += 1.0 / (rrf_k + rank)
    ordered = sorted(scores, key=scores.get, reverse=True)
    return [(doc_by_id[doc_id], scores[doc_id]) for doc_id in ordered]


question = "RAG 프로젝트에서 좋은 점수를 받으려면 무엇을 해야 하나?"
queries = generate_queries(question)

# 각 변형 질의를 독립적으로 검색한다.
ranked_lists = [retriever.invoke(query) for query in queries]
fused = reciprocal_rank_fusion(ranked_lists)

print("[생성된 검색 질의]")
for query in queries:
    print("-", query)

print("\n[RRF 융합 결과]")
for rank, (doc, score) in enumerate(fused[:5], 1):
    print(f"{rank}. {doc.metadata['id']} | RRF={score:.5f} | {doc.page_content}")

# 실습 과제: 생성 질의 수와 rrf_k를 바꾸고 D5의 최종 순위가 어떻게 변하는지 관찰하라.
