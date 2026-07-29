```py
"""
Google Colab 실습: LangChain + Chroma MMR 검색

참고: https://wikidocs.net/231585

학습 목표
- 일반 유사도 검색과 MMR 검색 결과를 비교합니다.
- k, fetch_k, lambda_mult의 역할을 확인합니다.
- 최신 langchain-chroma 패키지를 사용합니다.

기본 실습은 별도 PDF 없이 실행됩니다.
실제 PDF를 사용하는 선택 코드도 파일 아래쪽에 포함되어 있습니다.
"""

# =============================================================================
# [셀 1] 최신 패키지 설치
# Colab 코드 셀에서 다음 명령을 실행하세요.
# =============================================================================
# !pip -q install -U langchain-core langchain-openai langchain-chroma \
#     langchain-community langchain-text-splitters pymupdf tiktoken


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
# [셀 3] MMR 비교용 ESG 샘플 문서 생성
# 서로 비슷한 환경 문서와 서로 다른 관점의 문서를 함께 구성합니다.
# =============================================================================
from langchain_core.documents import Document


sample_records = [
    (
        "환경경영",
        "회사는 전사 환경경영 정책을 수립하고 환경 지표와 성과를 "
        "정기적으로 관리합니다. 환경경영 조직과 관리 체계를 단계적으로 "
        "구축하고 환경영향평가를 실시합니다.",
    ),
    (
        "온실가스",
        "회사는 Scope 1, Scope 2, Scope 3 온실가스 배출량을 측정하고 "
        "모니터링합니다. 중장기 감축 목표를 세우고 배출량 저감 성과를 "
        "경영진과 ESG위원회에 보고합니다.",
    ),
    (
        "에너지",
        "데이터센터와 사무공간의 전력 사용량을 줄이고 재생에너지 사용을 "
        "확대합니다. 고효율 LED와 자동 점등 센서를 도입하여 에너지 "
        "효율을 높입니다.",
    ),
    (
        "종이절감",
        "비대면 계좌 개설과 전자서식을 확대하여 종이 사용량을 줄입니다. "
        "모바일 영수증과 전자문서를 활용하는 페이퍼리스 정책을 추진합니다.",
    ),
    (
        "폐기물",
        "사업장에서 발생하는 폐기물을 분리 배출하고 재활용률을 관리합니다. "
        "일회용품 사용을 줄이고 친환경 구매 지침에 따라 사무용품을 "
        "구매합니다.",
    ),
    (
        "용수관리",
        "건물의 용수 사용량을 측정하고 절수 설비를 도입합니다. 정기적으로 "
        "사용량 추이를 분석하여 물 사용으로 인한 환경 영향을 줄입니다.",
    ),
    (
        "환경리스크",
        "기후변화를 주요 경영 리스크로 인식하고 포트폴리오의 탄소 배출과 "
        "환경 위험을 평가합니다. 투자 의사결정에도 환경 요소를 반영합니다.",
    ),
    (
        "녹색금융",
        "녹색채권과 ESG 펀드 등 친환경 금융상품의 기반을 마련합니다. "
        "고객의 친환경 활동에 혜택을 주는 금융상품도 검토합니다.",
    ),
    (
        "사회책임",
        "중저신용 고객을 위한 금융 접근성을 높이고 금융 취약계층을 "
        "지원합니다. 보이스피싱 예방과 안전한 모바일 금융 서비스에도 "
        "역량을 투입합니다.",
    ),
    (
        "지배구조",
        "이사회 산하 위원회가 ESG 전략과 주요 성과를 검토합니다. "
        "담당 조직은 목표 이행 결과와 주요 위험을 정기적으로 경영진에게 "
        "보고합니다.",
    ),
    (
        "환경목표",
        "단기적으로 환경관리 조직을 구성하고, 중기적으로 환경 성과와 "
        "리스크 관리 체계를 강화하며, 장기적으로 사업 전반의 환경 영향을 "
        "줄이는 것을 목표로 합니다.",
    ),
    (
        "환경성과",
        "에너지, 용수, 폐기물, 온실가스 지표를 설정하고 매년 성과를 "
        "점검합니다. 목표 대비 결과를 분석하여 다음 연도의 세부 추진 "
        "계획에 반영합니다.",
    ),
]

documents = [
    Document(
        page_content=content,
        metadata={"category": category, "source": "교육용 ESG 샘플"},
    )
    for category, content in sample_records
]

print(f"샘플 문서 수: {len(documents)}")
print("첫 번째 문서:", documents[0])


# =============================================================================
# [셀 4] OpenAI 임베딩과 Chroma 벡터 저장소 생성
# =============================================================================
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
persist_directory = "/content/db/chromadb"
document_ids = [f"esg-sample-{index:03d}" for index in range(len(documents))]

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    ids=document_ids,
    collection_name="esg_mmr_lab",
    persist_directory=persist_directory,
    collection_metadata={"hnsw:space": "cosine"},
)

print("Chroma 벡터 저장소 생성 완료")
print(f"저장 문서 수: {vector_store._collection.count()}")
print(f"저장 경로: {persist_directory}")


# =============================================================================
# [셀 5] 결과 출력 함수
# =============================================================================
def print_documents(title: str, results: list[Document]) -> None:
    """검색된 문서의 순위, 분류, 내용을 보기 좋게 출력합니다."""
    print(f"\n{title}")
    print("=" * 80)

    for rank, document in enumerate(results, start=1):
        category = document.metadata.get("category", "분류 없음")
        print(f"\n[{rank}위 | {category}]")
        print(document.page_content)


# =============================================================================
# [셀 6] 일반 유사도 검색
# 질문과 가장 가까운 문서를 순서대로 반환합니다.
# 비슷한 내용의 문서가 여러 개 포함될 수 있습니다.
# =============================================================================
query = "회사의 환경목표와 세부 추진 내용을 알려주세요."

similarity_results = vector_store.similarity_search(
    query=query,
    k=4,
)

print_documents(
    title=f"일반 유사도 검색 결과\n질문: {query}",
    results=similarity_results,
)


# =============================================================================
# [셀 7] MMR 검색
# 상위 fetch_k개 후보 중 관련성과 다양성을 고려하여 k개를 선택합니다.
# =============================================================================
mmr_results = vector_store.max_marginal_relevance_search(
    query=query,
    k=4,
    fetch_k=10,
    lambda_mult=0.5,
)

print_documents(
    title=(
        "MMR 검색 결과 "
        "(k=4, fetch_k=10, lambda_mult=0.5)\n"
        f"질문: {query}"
    ),
    results=mmr_results,
)


# =============================================================================
# [셀 8] 일반 검색과 MMR 검색의 분류 비교
# =============================================================================
similarity_categories = [
    document.metadata.get("category") for document in similarity_results
]
mmr_categories = [document.metadata.get("category") for document in mmr_results]

print("\n검색 방식별 선택된 문서 분류")
print("-" * 80)
print("일반 유사도 검색:", similarity_categories)
print("MMR 검색       :", mmr_categories)


# =============================================================================
# [셀 9] lambda_mult 값에 따른 결과 변화 비교
# 1.0에 가까울수록 질문과의 관련성을 더 중시합니다.
# 0.0에 가까울수록 검색 결과 사이의 다양성을 더 중시합니다.
# =============================================================================
for lambda_value in [1.0, 0.5, 0.0]:
    results = vector_store.max_marginal_relevance_search(
        query=query,
        k=4,
        fetch_k=10,
        lambda_mult=lambda_value,
    )

    categories = [
        document.metadata.get("category", "분류 없음")
        for document in results
    ]
    print(f"lambda_mult={lambda_value:.1f} -> {categories}")


# =============================================================================
# [셀 10] Retriever 형태로 MMR 검색 사용
# RAG 체인과 연결할 때 주로 사용하는 형태입니다.
# =============================================================================
mmr_retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5,
    },
)

retriever_results = mmr_retriever.invoke(query)

print_documents(
    title="Retriever로 실행한 MMR 검색 결과",
    results=retriever_results,
)


# =============================================================================
# [선택 셀 11] 사용자가 가진 PDF를 Colab에 업로드하여 로드
# 이 셀은 실제 PDF로 실습할 때만 실행합니다.
# =============================================================================
def load_pdf_from_colab() -> list[Document]:
    """Colab 파일 업로드 창에서 PDF를 받아 문서를 분할합니다."""
    try:
        from google.colab import files
    except ImportError as error:
        raise RuntimeError(
            "이 함수는 Google Colab에서 실행하세요."
        ) from error

    from langchain_community.document_loaders import PyMuPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    uploaded = files.upload()
    pdf_names = [
        name for name in uploaded if name.lower().endswith(".pdf")
    ]

    if not pdf_names:
        raise ValueError("업로드된 PDF 파일이 없습니다.")

    pdf_name = pdf_names[0]
    loader = PyMuPDFLoader(pdf_name)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name="cl100k_base",
        chunk_size=1000,
        chunk_overlap=200,
    )
    pdf_chunks = splitter.split_documents(pages)

    print(f"PDF 파일: {pdf_name}")
    print(f"페이지 수: {len(pages)}")
    print(f"분할된 청크 수: {len(pdf_chunks)}")
    return pdf_chunks


# 실제 PDF로 실습할 때 아래 주석을 해제합니다.
# pdf_documents = load_pdf_from_colab()
```
