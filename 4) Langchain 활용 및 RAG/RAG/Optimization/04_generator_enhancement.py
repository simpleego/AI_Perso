"""실습 4: Generator Enhancement - 문서 재배치와 근거 중심 프롬프트."""

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_transformers import LongContextReorder
from langchain_openai import ChatOpenAI


# Retriever가 관련도 순으로 문서를 반환했다고 가정한다.
retrieved_docs = [
    Document(page_content="졸업에 필요한 총 이수학점은 130학점 이상이다.", metadata={"id": "G1", "source": "졸업규정 제3조"}),
    Document(page_content="전공필수 교과목은 모두 이수해야 하며 전공 총 이수학점은 60학점 이상이어야 한다.", metadata={"id": "G2", "source": "졸업규정 제4조"}),
    Document(page_content="교양필수 영역에서는 대학글쓰기와 데이터리터러시를 반드시 이수해야 한다.", metadata={"id": "G3", "source": "교양교육과정"}),
    Document(page_content="졸업논문은 4학년 2학기 종료 전까지 학과 심사를 통과해야 한다.", metadata={"id": "G4", "source": "졸업규정 제8조"}),
    Document(page_content="도서관 연체 도서가 있으면 졸업증명서 발급이 제한될 수 있다.", metadata={"id": "G5", "source": "도서관 규정"}),
    Document(page_content="졸업인증을 위해 공인 외국어 성적 또는 대학 지정 대체 과정을 이수해야 한다.", metadata={"id": "G6", "source": "졸업인증 규정"}),
]

# LongContextReorder.transform_documents():
# 관련도 높은 문서를 긴 컨텍스트의 앞과 뒤에 배치해 Lost in the Middle 현상을 완화한다.
reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(retrieved_docs)


def format_context(docs: list[Document]) -> str:
    """출처 식별자를 문맥에 포함하여 모델이 근거를 인용할 수 있게 한다."""
    return "\n\n".join(
        f"[{doc.metadata['id']}] 출처: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "아래 컨텍스트만 사용해 답하세요. 각 문장 끝에 [문서ID]를 인용하세요. "
            "컨텍스트에 없는 내용은 추측하지 말고 '제공된 문서에서 확인할 수 없습니다'라고 답하세요.",
        ),
        ("human", "컨텍스트:\n{context}\n\n질문: {question}"),
    ]
)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
rag_chain = prompt | llm | StrOutputParser()

question = "졸업하려면 학점, 필수 과목, 논문과 인증 측면에서 무엇이 필요한가?"

print("[재배치 전]", [doc.metadata["id"] for doc in retrieved_docs])
print("[재배치 후]", [doc.metadata["id"] for doc in reordered_docs])

# invoke(): 재배치한 문맥과 명확한 생성 규칙을 함께 전달한다.
answer = rag_chain.invoke(
    {"context": format_context(reordered_docs), "question": question}
)
print("\n[근거 중심 답변]\n", answer)

# 간단한 생성 단계 검사: 답변에 최소 하나 이상의 문서 인용이 있는지 확인한다.
has_citation = any(f"[{doc.metadata['id']}]" in answer for doc in reordered_docs)
print("\n인용 포함 여부:", has_citation)

# 실습 과제: 문서에 없는 "졸업 평점 기준"을 질문하고 불확실성 규칙이 작동하는지 확인하라.
