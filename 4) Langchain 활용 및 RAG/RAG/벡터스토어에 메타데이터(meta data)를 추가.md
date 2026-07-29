```py
"""
Google Colab 실습: LangChain Chroma 벡터스토어에 메타데이터 추가

참고: https://wikidocs.net/231507

학습 목표
- Document에 본문과 메타데이터를 함께 저장합니다.
- Chroma 유사도 검색 결과에서 메타데이터를 확인합니다.
- 메타데이터 조건을 사용해 검색 범위를 제한합니다.
- 저장된 Chroma 데이터베이스에 다시 연결합니다.
"""

# =============================================================================
# [셀 1] 최신 패키지 설치
# Colab 코드 셀에서 다음 명령을 실행하세요.
# =============================================================================
# !pip -q install -U langchain-core langchain-openai langchain-chroma


# =============================================================================
# [셀 2] OpenAI API 키 안전하게 불러오기
# =============================================================================
import os
from getpass import getpass


def load_openai_api_key() -> str:
    """Colab 보안 비밀 또는 화면 입력으로 OpenAI API 키를 불러옵니다."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        try:
            from google.colab import userdata

            api_key = userdata.get("OPENAI_API_KEY")
        except (ImportError, KeyError, TypeError):
            api_key = None

    if not api_key:
        api_key = getpass("OpenAI API 키를 입력하세요: ").strip()

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY가 없습니다. "
            "Colab 보안 비밀에 OPENAI_API_KEY를 등록하세요."
        )

    os.environ["OPENAI_API_KEY"] = api_key
    return api_key


load_openai_api_key()
print("OpenAI API 키 설정 완료")


# =============================================================================
# [셀 3] 본문과 메타데이터를 포함한 Document 생성
# Chroma 메타데이터 값은 문자열, 정수, 실수, 불리언을 사용하는 것이 안전합니다.
# =============================================================================
from langchain_core.documents import Document


documents = [
    Document(
        page_content=(
            "LangChain은 언어 모델을 활용한 애플리케이션을 만들기 위한 "
            "오픈소스 프레임워크입니다. 모델, 프롬프트, 도구와 검색 시스템을 "
            "표준 인터페이스로 연결할 수 있습니다."
        ),
        metadata={
            "title": "LangChain 소개",
            "author": "AI 개발자",
            "url": "https://example.com/langchain-intro",
            "category": "framework",
            "year": 2026,
            "language": "ko",
        },
    ),
    Document(
        page_content=(
            "벡터 데이터베이스는 텍스트나 이미지에서 생성된 고차원 벡터를 "
            "저장하고, 의미적으로 가까운 데이터를 빠르게 검색하는 데 "
            "특화된 데이터베이스입니다."
        ),
        metadata={
            "title": "벡터 데이터베이스 개요",
            "author": "데이터 과학자",
            "url": "https://example.com/vector-db-overview",
            "category": "database",
            "year": 2025,
            "language": "ko",
        },
    ),
    Document(
        page_content=(
            "Chroma는 임베딩 벡터와 문서, 메타데이터를 함께 관리할 수 있는 "
            "오픈소스 벡터 데이터베이스입니다. 로컬 환경에서도 간단하게 "
            "유사도 검색을 실습할 수 있습니다."
        ),
        metadata={
            "title": "Chroma 벡터스토어",
            "author": "RAG 연구자",
            "url": "https://example.com/chroma",
            "category": "database",
            "year": 2026,
            "language": "ko",
        },
    ),
    Document(
        page_content=(
            "RAG는 질문과 관련된 문서를 먼저 검색한 뒤 그 문서를 언어 "
            "모델의 답변 생성에 활용하는 방식입니다. 외부 지식을 근거로 "
            "답변하도록 도와줍니다."
        ),
        metadata={
            "title": "RAG 기초",
            "author": "AI 강사",
            "url": "https://example.com/rag-basic",
            "category": "rag",
            "year": 2026,
            "language": "ko",
        },
    ),
    Document(
        page_content=(
            "Metadata describes a document using fields such as title, "
            "author, category, language, and publication year."
        ),
        metadata={
            "title": "Metadata Basics",
            "author": "Data Engineer",
            "url": "https://example.com/metadata-basics",
            "category": "database",
            "year": 2024,
            "language": "en",
        },
    ),
]

print(f"생성한 문서 수: {len(documents)}")
print("첫 번째 문서:")
print(documents[0])


# =============================================================================
# [셀 4] OpenAI 임베딩과 Chroma 벡터스토어 생성
# =============================================================================
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
persist_directory = "/content/chroma_metadata_db"
document_ids = [
    "doc-langchain",
    "doc-vector-db",
    "doc-chroma",
    "doc-rag",
    "doc-metadata-en",
]

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    ids=document_ids,
    collection_name="metadata_lab",
    persist_directory=persist_directory,
    collection_metadata={"hnsw:space": "cosine"},
)

print("Chroma 벡터스토어 생성 완료")
print(f"저장 경로: {persist_directory}")
print(f"저장된 문서 수: {vector_store._collection.count()}")


# =============================================================================
# [셀 5] 검색 결과와 메타데이터 출력 함수
# metadata["title"] 대신 get()을 사용하면 필드가 없어도 오류가 나지 않습니다.
# =============================================================================
def print_results(title: str, results: list[Document]) -> None:
    """Document 검색 결과와 메타데이터를 출력합니다."""
    print(f"\n{title}")
    print("=" * 80)

    if not results:
        print("검색 결과가 없습니다.")
        return

    for rank, document in enumerate(results, start=1):
        metadata = document.metadata

        print(f"\n[{rank}위]")
        print(f"내용     : {document.page_content}")
        print(f"제목     : {metadata.get('title', '없음')}")
        print(f"저자     : {metadata.get('author', '없음')}")
        print(f"분류     : {metadata.get('category', '없음')}")
        print(f"작성 연도: {metadata.get('year', '없음')}")
        print(f"언어     : {metadata.get('language', '없음')}")
        print(f"URL      : {metadata.get('url', '없음')}")


# =============================================================================
# [셀 6] 전체 문서에서 유사도 검색
# =============================================================================
query = "LangChain은 어떤 프레임워크인가요?"

results = vector_store.similarity_search(
    query=query,
    k=3,
)

print_results(
    title=f"전체 문서 유사도 검색\n질문: {query}",
    results=results,
)


# =============================================================================
# [셀 7] 메타데이터의 category 값으로 필터링
# database 분류에 속하는 문서 안에서만 검색합니다.
# =============================================================================
database_results = vector_store.similarity_search(
    query="벡터를 저장하고 검색하는 도구를 알려주세요.",
    k=3,
    filter={"category": "database"},
)

print_results(
    title="category='database' 조건 검색",
    results=database_results,
)


# =============================================================================
# [셀 8] 여러 메타데이터 조건으로 필터링
# database 분류이면서 한국어 문서인 결과만 검색합니다.
# =============================================================================
korean_database_results = vector_store.similarity_search(
    query="벡터 데이터베이스가 무엇인가요?",
    k=3,
    filter={
        "$and": [
            {"category": {"$eq": "database"}},
            {"language": {"$eq": "ko"}},
        ]
    },
)

print_results(
    title="category='database' AND language='ko' 조건 검색",
    results=korean_database_results,
)


# =============================================================================
# [셀 9] 작성 연도를 이용한 숫자 조건 검색
# 2025년 이상인 문서 안에서만 검색합니다.
# =============================================================================
recent_results = vector_store.similarity_search(
    query="RAG와 벡터 검색 기술을 설명해주세요.",
    k=5,
    filter={"year": {"$gte": 2025}},
)

print_results(
    title="year >= 2025 조건 검색",
    results=recent_results,
)


# =============================================================================
# [셀 10] Chroma에 실제로 저장된 원시 데이터 확인
# =============================================================================
stored_data = vector_store.get(
    include=["documents", "metadatas"],
)

print("\nChroma 내부 저장 데이터")
print("=" * 80)

for item_id, text, metadata in zip(
    stored_data["ids"],
    stored_data["documents"],
    stored_data["metadatas"],
):
    print(f"\nID       : {item_id}")
    print(f"제목     : {metadata.get('title', '없음')}")
    print(f"메타데이터: {metadata}")
    print(f"본문 앞부분: {text[:80]}")


# =============================================================================
# [셀 11] 저장된 Chroma 데이터베이스에 다시 연결
# 기존 DB를 열 때는 문서를 다시 임베딩할 필요가 없습니다.
# 검색 시 질문 임베딩은 필요하므로 같은 임베딩 모델을 연결합니다.
# =============================================================================
reloaded_vector_store = Chroma(
    collection_name="metadata_lab",
    embedding_function=embedding_model,
    persist_directory=persist_directory,
)

reloaded_results = reloaded_vector_store.similarity_search(
    query="검색한 외부 문서를 이용해 답변하는 방법은 무엇인가요?",
    k=1,
)

print_results(
    title="다시 연결한 DB의 검색 결과",
    results=reloaded_results,
)
```
