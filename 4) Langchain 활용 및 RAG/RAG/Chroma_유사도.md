```py
"""
Google Colab 실습: LangChain + Chroma 유사도 기반 검색

참고: https://wikidocs.net/231578

실행 순서
1. OpenAI Platform에서 API 키를 준비합니다.
2. Colab 왼쪽의 열쇠 모양 '보안 비밀'에 다음 값을 등록합니다.
   - 이름: OPENAI_API_KEY
   - 값: 발급받은 API 키
   - 노트북 액세스 허용: 활성화
3. 아래 [셀 1]부터 순서대로 실행합니다.

이 코드는 실습용 history.txt를 자동 생성하므로 별도 파일 업로드가 필요 없습니다.
"""

# =============================================================================
# [셀 1] 최신 패키지 설치
# Colab 코드 셀에서 다음 한 줄을 실행하세요.
# =============================================================================
# !pip -q install -U langchain-community langchain-text-splitters \
#     langchain-openai langchain-chroma tiktoken


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
# [셀 3] 실습용 한국사 텍스트 파일 생성
# =============================================================================
from pathlib import Path


HISTORY_TEXT = """
한국의 역사는 수천 년에 걸쳐 이어져 온 긴 여정 속에서 다양한 문화와
전통이 형성되고 발전해 왔습니다. 고조선에서 시작해 삼국 시대의 경쟁,
통일 신라와 고려를 거쳐 조선까지 한반도는 많은 변화를 겪었습니다.

고조선은 단군왕검에 의해 세워졌다고 전해집니다. 이후 한반도와 만주
일대에서 여러 국가가 성장했습니다. 고구려, 백제, 신라는 서로 경쟁하면서
각자의 문화와 제도를 발전시켰습니다.

신라는 삼국을 통일한 뒤 불교문화와 국제 교류를 발전시켰습니다. 이후
고려는 918년 왕건에 의해 건국되었습니다. 고려 시대에는 팔만대장경과
청자 같은 뛰어난 문화유산이 만들어졌습니다.

조선은 1392년 이성계에 의해 건국되었습니다. 조선의 제4대 왕인
세종대왕은 백성이 쉽게 글을 읽고 쓸 수 있도록 훈민정음을 창제했습니다.
훈민정음은 오늘날 한글의 바탕이 되었습니다.

조선 후기에는 실학이 발전하고 사회 변화를 위한 여러 움직임이
나타났습니다. 19세기 말에는 개항과 근대화가 진행되었으며, 일제강점기를
거쳐 1945년 광복을 맞았습니다.

대한민국은 1948년에 정부를 수립했습니다. 이후 산업화와 민주화를
거치면서 경제와 과학기술, 문화 분야에서 빠르게 성장했습니다.
""".strip()

history_path = Path("/content/history.txt")
history_path.write_text(HISTORY_TEXT, encoding="utf-8")

print(f"실습 파일 생성 완료: {history_path}")
print(f"문자 수: {len(HISTORY_TEXT):,}")


# =============================================================================
# [셀 4] 텍스트 파일 로드
# =============================================================================
from langchain_community.document_loaders import TextLoader


loader = TextLoader(str(history_path), encoding="utf-8")
documents = loader.load()

print(f"로드한 문서 수: {len(documents)}")
print("원본 문서 앞부분:")
print(documents[0].page_content[:200])


# =============================================================================
# [셀 5] 긴 문서를 작은 조각으로 분할
# =============================================================================
from langchain_text_splitters import RecursiveCharacterTextSplitter


text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base",
    chunk_size=250,
    chunk_overlap=50,
)

chunks = text_splitter.split_documents(documents)

print(f"\n생성된 청크 수: {len(chunks)}")
for index, chunk in enumerate(chunks, start=1):
    print(f"\n[{index}번 청크]")
    print(chunk.page_content)


# =============================================================================
# [셀 6] OpenAI 임베딩 모델 및 Chroma 벡터 저장소 생성
# =============================================================================
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Colab 런타임이 유지되는 동안 데이터베이스 파일이 이 경로에 저장됩니다.
persist_directory = "/content/db/chromadb"
chunk_ids = [f"history-chunk-{index:04d}" for index in range(len(chunks))]

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    ids=chunk_ids,
    collection_name="history",
    persist_directory=persist_directory,
    collection_metadata={"hnsw:space": "cosine"},
)

print("Chroma 벡터 저장소 생성 완료")
print(f"저장 경로: {persist_directory}")
print(f"저장된 문서 수: {vector_store._collection.count()}")


# =============================================================================
# [셀 7] 유사도 기반 검색
# =============================================================================
query = "누가 한글을 창제했나요?"
search_results = vector_store.similarity_search(query=query, k=3)

print(f"\n질문: {query}")
print("=" * 70)

for rank, document in enumerate(search_results, start=1):
    print(f"\n[{rank}위 검색 결과]")
    print(document.page_content)
    print("메타데이터:", document.metadata)


# =============================================================================
# [셀 8] 유사도 점수와 함께 검색
# 거리(distance)는 작을수록 질문과 가깝습니다.
# =============================================================================
results_with_score = vector_store.similarity_search_with_score(
    query=query,
    k=3,
)

print(f"\n질문: {query}")
print("=" * 70)

for rank, (document, distance) in enumerate(results_with_score, start=1):
    print(f"\n[{rank}위] 코사인 거리: {distance:.4f}")
    print(document.page_content)


# =============================================================================
# [셀 9] 재사용 가능한 검색 함수
# =============================================================================
def search_history(user_query: str, top_k: int = 3) -> None:
    """한국사 문서에서 질문과 관련된 청크를 검색하여 출력합니다."""
    if top_k < 1:
        raise ValueError("top_k는 1 이상이어야 합니다.")

    results = vector_store.similarity_search_with_score(
        query=user_query,
        k=min(top_k, len(chunks)),
    )

    print(f"\n질문: {user_query}")
    print("-" * 70)

    for rank, (document, distance) in enumerate(results, start=1):
        print(f"\n{rank}위 | 코사인 거리: {distance:.4f}")
        print(document.page_content)


search_history("고려 시대의 대표적인 문화유산은 무엇인가요?", top_k=2)


# =============================================================================
# [선택 셀 10] 기존 Chroma 데이터베이스 다시 연결
# Colab에서 셀 6을 다시 실행하지 않고 저장된 DB를 열 때 사용합니다.
# =============================================================================
reloaded_vector_store = Chroma(
    collection_name="history",
    embedding_function=embedding_model,
    persist_directory=persist_directory,
)

reloaded_results = reloaded_vector_store.similarity_search(
    "대한민국 정부는 언제 수립되었나요?",
    k=1,
)

print("\n다시 연결한 DB의 검색 결과:")
print(reloaded_results[0].page_content)
```
