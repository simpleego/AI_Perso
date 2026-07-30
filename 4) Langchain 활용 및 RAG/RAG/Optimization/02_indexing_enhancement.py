"""실습 2: Indexing Enhancement - Small-to-Big(부모-자식) 검색."""

from langchain_core.documents import Document
from langchain_core.stores import InMemoryStore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import ParentDocumentRetriever


# 실제 수업에서는 Loader가 반환한 긴 문서라고 가정한다.
documents = [
    Document(
        page_content=(
            "제1장 수강신청. 재학생은 지정된 기간에 수강신청 시스템을 이용한다. "
            "학기당 기본 신청 가능 학점은 18학점이다. 직전 학기 평점평균이 4.0 이상인 "
            "학생은 최대 21학점까지 신청할 수 있다. 졸업예정자는 졸업 필수과목의 잔여 "
            "좌석이 없을 때 학과 사무실에 증원 신청서를 제출할 수 있다. "
            "수강 정정은 개강 후 7일 동안 가능하며 정정 기간 이후에는 과목 변경이 불가능하다."
        ),
        metadata={"id": "I1", "source": "학사규정", "chapter": "수강신청"},
    ),
    Document(
        page_content=(
            "제2장 휴학과 복학. 일반휴학은 한 번에 두 학기까지 신청할 수 있다. "
            "군휴학과 질병휴학은 증빙 서류를 첨부해야 한다. 복학 신청은 개강 30일 전부터 "
            "개강 후 7일까지 가능하다. 등록금을 납부한 뒤 휴학한 학생은 복학 학기로 등록금을 이월한다."
        ),
        metadata={"id": "I2", "source": "학사규정", "chapter": "휴복학"},
    ),
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    encode_kwargs={"normalize_embeddings": True},
)

# 부모 청크는 LLM에 전달할 풍부한 문맥, 자식 청크는 정밀 검색에 사용할 짧은 단위다.
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
child_splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=15)

# 빈 FAISS 인덱스를 만들기 위해 최소 문서를 넣고 인덱스를 초기화한다.
seed = Document(page_content="인덱스 초기화용 문서", metadata={"id": "SEED"})
vectorstore = FAISS.from_documents([seed], embeddings)

# InMemoryStore에는 큰 부모 청크를 보관한다.
parent_store = InMemoryStore()

# ParentDocumentRetriever:
# 1) 작은 자식 청크를 임베딩하여 정확하게 검색하고,
# 2) 매칭된 자식이 속한 큰 부모 청크를 반환한다.
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=parent_store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": 3},
)
parent_retriever.add_documents(documents)

question = "성적이 매우 우수하면 한 학기에 몇 학점까지 신청할 수 있나요?"
results = parent_retriever.invoke(question)

print("[Small-to-Big 검색 결과]")
for rank, doc in enumerate(results, 1):
    print(f"\n{rank}. 출처={doc.metadata.get('source')} / 장={doc.metadata.get('chapter')}")
    print(doc.page_content)

print("\n검색에는 80자 자식 청크를 사용하지만 답변 생성에는 더 큰 부모 문맥을 제공합니다.")

# 실습 과제:
# 1. child_splitter의 chunk_size를 40, 160으로 변경한다.
# 2. 정답을 포함한 부모 문서가 검색되는지와 반환 문맥의 완전성을 비교한다.
