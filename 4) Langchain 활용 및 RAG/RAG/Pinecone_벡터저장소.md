이번 페이지는 **Pinecone 벡터 저장소에서 유사도 기반 검색을 수행하는 방법**을 다룹니다. 원문은 OpenAI 임베딩을 사용하지만, 실습 비용을 줄이기 위해 아래 코드는 **무료 Hugging Face 다국어 임베딩 모델**을 사용하도록 수정했습니다.

Pinecone은 클라우드 관리형 벡터 데이터베이스이므로 **Pinecone 계정과 API 키가 반드시 필요**합니다. 또한 Pinecone 인덱스는 LangChain의 `PineconeVectorStore`를 연결하기 전에 먼저 생성되어 있어야 합니다. ([위키독스][1])

---

# 실습 목표

이번 코드에서는 다음 작업을 수행합니다.

1. 한국 역사 예제 문서를 코드에서 직접 생성
2. 문서를 일정 크기로 분할
3. Hugging Face 임베딩 모델로 문서를 벡터화
4. Pinecone Serverless 인덱스 생성
5. 문서를 Pinecone에 저장
6. 유사도 기반 검색 수행
7. 유사도 점수와 함께 결과 출력
8. Retriever 방식으로 검색
9. 기존 인덱스에 다시 연결
10. 실습 데이터 삭제

---

# 사전 준비

## 1. Pinecone API 키 발급

Pinecone에 가입한 후 API 키를 발급받습니다.

Colab에서는 다음 위치에 API 키를 등록합니다.

```text
왼쪽 메뉴 → 열쇠 모양 아이콘(보안 비밀) → 새 보안 비밀 추가
```

다음 이름으로 저장합니다.

```text
이름: PINECONE_API_KEY
값: 발급받은 Pinecone API 키
```

**노트북 액세스**도 활성화합니다.

---

# Colab 전체 실습 코드

## 셀 1. 라이브러리 설치

```python
# =============================================================================
# [셀 1] 필요한 라이브러리 설치
# =============================================================================

!pip install -qU \
    langchain \
    langchain-core \
    langchain-pinecone \
    langchain-huggingface \
    langchain-text-splitters \
    sentence-transformers \
    pinecone \
    pandas
```

LangChain 공식 문서는 Pinecone 연동에 `langchain-pinecone` 패키지를 사용하도록 안내합니다. 이전의 `langchain_community.vectorstores.Pinecone` 구현 대신 `PineconeVectorStore`를 사용하는 방식이 현재 권장됩니다. ([Docs by LangChain][2])

설치 직후 import 오류가 발생한다면 다음 메뉴를 실행합니다.

```text
런타임 → 세션 다시 시작
```

---

## 셀 2. 라이브러리 불러오기

```python
# =============================================================================
# [셀 2] 라이브러리 불러오기
# =============================================================================

import os
import time
import uuid
import pandas as pd

from google.colab import userdata

from pinecone import Pinecone, ServerlessSpec

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

---

## 셀 3. Pinecone API 키 가져오기

```python
# =============================================================================
# [셀 3] Colab 보안 비밀에서 Pinecone API 키 가져오기
# =============================================================================

try:
    PINECONE_API_KEY = userdata.get("PINECONE_API_KEY")
except Exception:
    PINECONE_API_KEY = None

if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY가 설정되지 않았습니다.\n"
        "Colab 왼쪽 메뉴의 열쇠 아이콘에서 "
        "PINECONE_API_KEY를 등록하고 노트북 액세스를 허용하세요."
    )

# 일부 라이브러리에서도 환경 변수를 사용할 수 있도록 설정
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

print("Pinecone API 키 로드 완료")
```

API 키 전체 값은 화면에 출력하지 않는 것이 안전합니다.

확인이 필요하다면 앞부분만 출력합니다.

```python
print("API 키 확인:", PINECONE_API_KEY[:6] + "...")
```

---

## 셀 4. 실습용 역사 문서 직접 생성

실제 환경에서는 업로드한 TXT, PDF, DOCX 문서를 로드하면 됩니다. 이번 실습에서는 파일이 이미 준비되었다고 가정하고, 동일한 역할을 하는 예제 문서를 코드 안에서 생성합니다.

```python
# =============================================================================
# [셀 4] 한국 역사 실습용 문서 생성
# =============================================================================

history_text = """
고조선은 한국 역사에서 최초의 국가로 알려져 있다.
단군왕검이 고조선을 건국했다는 이야기가 삼국유사에 기록되어 있다.
고조선은 청동기 문화를 바탕으로 성장했으며, 8조법을 통해 당시의 사회 모습을 확인할 수 있다.

삼국 시대에는 고구려, 백제, 신라가 서로 경쟁하며 발전했다.
고구려는 광개토대왕과 장수왕 시기에 영토를 크게 확장했다.
백제는 중국 및 일본과 활발하게 교류하며 문화를 발전시켰다.
신라는 화랑도를 중심으로 인재를 양성했고, 당나라와 연합하여 삼국을 통일했다.

통일신라는 불교문화를 발전시켰으며 불국사와 석굴암 같은 문화유산을 남겼다.
발해는 고구려 계승 의식을 가진 국가로 대조영이 건국했다.
발해는 넓은 영토와 활발한 국제 교류를 바탕으로 해동성국이라 불렸다.

고려는 918년 왕건에 의해 건국되었다.
고려는 후삼국을 통일하고 개경을 수도로 삼았다.
고려 시대에는 불교가 크게 발전했고 팔만대장경과 고려청자가 만들어졌다.
또한 금속활자를 이용한 인쇄술이 발전했다.

조선은 1392년 이성계가 건국했다.
조선은 유교를 국가 통치 이념으로 삼고 중앙집권적 정치 체제를 확립했다.
조선의 제4대 왕 세종대왕은 백성들이 쉽게 글을 읽고 쓸 수 있도록 훈민정음을 창제했다.
훈민정음은 1443년에 창제되고 1446년에 반포되었다.

세종대왕 시기에는 장영실을 비롯한 과학자들이 활약했다.
측우기, 해시계, 물시계 등 다양한 과학 기구가 제작되었다.
농업 기술 발전을 위해 농사직설도 편찬되었다.

임진왜란은 1592년 일본이 조선을 침략하면서 시작되었다.
이순신 장군은 거북선과 조선 수군을 이끌고 여러 해전에서 승리했다.
한산도 대첩은 임진왜란의 대표적인 해전 중 하나이다.

조선 후기에는 실학이 발전했다.
정약용은 백성의 생활을 개선하기 위한 다양한 개혁 사상을 제시했다.
정약용은 목민심서와 경세유표 등의 저서를 남겼다.

1910년 조선은 일본에 의해 국권을 상실했다.
일제강점기에는 독립을 되찾기 위한 다양한 독립운동이 전개되었다.
1919년 3월 1일에는 전국적으로 3·1 운동이 일어났다.
같은 해 중국 상하이에서 대한민국 임시정부가 수립되었다.

대한민국은 1945년 8월 15일 광복을 맞이했다.
1948년에는 대한민국 정부가 수립되었다.
이후 대한민국은 산업화와 민주화를 거치며 발전했다.
"""

print(history_text[:500])
```

---

## 셀 5. 원본을 LangChain Document로 변환

```python
# =============================================================================
# [셀 5] Document 객체 생성
# =============================================================================

source_document = Document(
    page_content=history_text,
    metadata={
        "source": "history_example.txt",
        "subject": "한국사",
        "language": "ko"
    }
)

print("문서 내용 길이:", len(source_document.page_content))
print("메타데이터:", source_document.metadata)
```

---

## 셀 6. 문서 분할

원문 페이지는 `RecursiveCharacterTextSplitter`를 사용해 문서를 작은 조각으로 나눕니다. Pinecone에 전체 문서를 하나의 벡터로 저장하기보다 의미 단위의 청크로 분할하면, 질문과 직접 관련된 부분을 더 정확히 검색할 수 있습니다. ([위키독스][1])

```python
# =============================================================================
# [셀 6] RecursiveCharacterTextSplitter로 문서 분할
# =============================================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

docs = text_splitter.split_documents([source_document])

# 각 청크에 고유 메타데이터 추가
for index, doc in enumerate(docs):
    doc.metadata.update({
        "chunk_id": index,
        "document_id": "korean-history-001"
    })

print(f"분할된 문서 수: {len(docs)}개")

for index, doc in enumerate(docs):
    print("=" * 80)
    print(f"청크 번호: {index}")
    print(f"문자 수: {len(doc.page_content)}")
    print("메타데이터:", doc.metadata)
    print("내용:")
    print(doc.page_content)
```

---

## 셀 7. Hugging Face 임베딩 모델 생성

OpenAI API 키 없이 사용할 수 있는 다국어 임베딩 모델을 사용합니다.

```python
# =============================================================================
# [셀 7] Hugging Face 임베딩 모델 생성
# =============================================================================

EMBEDDING_MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)

print("임베딩 모델 생성 완료")
print("모델:", EMBEDDING_MODEL_NAME)
```

Colab GPU 런타임을 사용한다면 다음과 같이 바꿀 수 있습니다.

```python
model_kwargs={
    "device": "cuda"
}
```

---

## 셀 8. 임베딩 차원 확인

Pinecone 인덱스의 `dimension`은 임베딩 모델이 생성하는 벡터 차원과 정확히 같아야 합니다. 원문에서 사용하는 OpenAI `text-embedding-3-small`은 1,536차원이지만, 이번 실습 모델은 직접 차원을 계산해 설정합니다. Pinecone 인덱스 생성 시 벡터 차원과 유사도 측정 방식을 지정해야 합니다. ([위키독스][1])

```python
# =============================================================================
# [셀 8] 임베딩 벡터 차원 자동 확인
# =============================================================================

test_vector = embeddings.embed_query("임베딩 차원 확인")

EMBEDDING_DIMENSION = len(test_vector)

print("임베딩 벡터 차원:", EMBEDDING_DIMENSION)
print("벡터 앞부분:", test_vector[:5])
```

일반적으로 다음과 같이 출력됩니다.

```text
임베딩 벡터 차원: 384
```

차원을 직접 `384`라고 고정하는 대신, 코드에서 자동 계산하면 모델을 변경해도 오류를 줄일 수 있습니다.

---

## 셀 9. Pinecone 클라이언트 생성

```python
# =============================================================================
# [셀 9] Pinecone 클라이언트 생성
# =============================================================================

pc = Pinecone(api_key=PINECONE_API_KEY)

print("Pinecone 클라이언트 생성 완료")
```

---

## 셀 10. 인덱스 이름 설정

Pinecone 인덱스 이름에는 영문 소문자, 숫자, 하이픈을 사용하는 것이 안전합니다.

```python
# =============================================================================
# [셀 10] 인덱스와 네임스페이스 설정
# =============================================================================

INDEX_NAME = "langchain-history-practice"

# 같은 인덱스에서 실습 데이터를 분리하기 위한 공간
NAMESPACE = "similarity-search-practice"

print("인덱스 이름:", INDEX_NAME)
print("네임스페이스:", NAMESPACE)
```

---

## 셀 11. Pinecone Serverless 인덱스 생성

Pinecone 공식 Python SDK는 `Pinecone` 클라이언트와 `ServerlessSpec`을 이용해 Serverless 인덱스를 생성하는 방식을 지원합니다. ([Pinecone Docs][3])

```python
# =============================================================================
# [셀 11] Pinecone Serverless 인덱스 생성
# =============================================================================

existing_indexes = pc.list_indexes().names()

if INDEX_NAME not in existing_indexes:
    print(f"'{INDEX_NAME}' 인덱스를 생성합니다.")

    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled"
    )

    print("인덱스 생성 요청 완료")

else:
    print(f"'{INDEX_NAME}' 인덱스가 이미 존재합니다.")
```

---

## 셀 12. 인덱스가 준비될 때까지 확인

인덱스 생성 요청 직후에는 아직 준비가 끝나지 않았을 수 있습니다.

```python
# =============================================================================
# [셀 12] Pinecone 인덱스 준비 상태 확인
# =============================================================================

while True:
    description = pc.describe_index(INDEX_NAME)
    status = description.status

    # SDK 버전에 따라 dict 또는 객체 형태로 반환될 수 있음
    if isinstance(status, dict):
        is_ready = status.get("ready", False)
        state = status.get("state", "Unknown")
    else:
        is_ready = getattr(status, "ready", False)
        state = getattr(status, "state", "Unknown")

    print("현재 상태:", state)

    if is_ready:
        break

    time.sleep(2)

print("Pinecone 인덱스 준비 완료")
```

---

## 셀 13. 기존 인덱스 설정 검증

같은 이름의 인덱스가 이미 있지만 임베딩 차원이 다르면 업로드할 수 없습니다.

```python
# =============================================================================
# [셀 13] 인덱스 차원과 metric 검증
# =============================================================================

description = pc.describe_index(INDEX_NAME)

index_dimension = description.dimension
index_metric = description.metric

print("Pinecone 인덱스 차원:", index_dimension)
print("현재 임베딩 모델 차원:", EMBEDDING_DIMENSION)
print("Pinecone metric:", index_metric)

if index_dimension != EMBEDDING_DIMENSION:
    raise ValueError(
        f"인덱스 차원이 일치하지 않습니다.\n"
        f"- 기존 Pinecone 인덱스: {index_dimension}차원\n"
        f"- 현재 임베딩 모델: {EMBEDDING_DIMENSION}차원\n\n"
        f"다른 INDEX_NAME을 사용하거나 기존 인덱스를 삭제한 후 "
        f"다시 생성하세요."
    )

print("인덱스 설정 검증 완료")
```

---

## 셀 14. Pinecone 인덱스 객체 가져오기

```python
# =============================================================================
# [셀 14] Pinecone 인덱스 객체 가져오기
# =============================================================================

index = pc.Index(INDEX_NAME)

print("Pinecone 인덱스 연결 완료")
```

---

## 셀 15. 재실행을 위해 기존 네임스페이스 데이터 삭제

Colab 셀을 반복 실행하면 같은 문서가 여러 번 저장될 수 있습니다. 이를 막기 위해 실습용 네임스페이스만 비우고 다시 저장합니다.

```python
# =============================================================================
# [셀 15] 기존 실습 네임스페이스 초기화
# =============================================================================

try:
    index.delete(
        delete_all=True,
        namespace=NAMESPACE
    )

    print(f"기존 '{NAMESPACE}' 데이터 삭제 요청 완료")

    # 삭제 반영 시간을 조금 기다림
    time.sleep(2)

except Exception as error:
    print("기존 데이터가 없거나 삭제 과정에서 다음 메시지가 발생했습니다.")
    print(error)
```

인덱스 전체를 삭제하는 것이 아니라 `similarity-search-practice` 네임스페이스의 데이터만 삭제합니다.

---

## 셀 16. 문서별 ID 생성

Pinecone에 문서를 저장할 때 고유한 ID를 명시하면 데이터 관리가 쉬워집니다.

```python
# =============================================================================
# [셀 16] Pinecone에 저장할 문서 ID 생성
# =============================================================================

document_ids = [
    f"history-chunk-{index:03d}"
    for index in range(len(docs))
]

print("생성된 문서 ID:")
print(document_ids)
```

---

## 셀 17. Pinecone에 문서 저장

```python
# =============================================================================
# [셀 17] 문서를 임베딩하여 Pinecone에 저장
# =============================================================================

vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name=INDEX_NAME,
    namespace=NAMESPACE,
    ids=document_ids
)

print("Pinecone 문서 저장 완료")
```

`PineconeVectorStore.from_documents()`는 문서를 임베딩한 뒤 Pinecone 인덱스에 저장합니다. 원문 예제도 동일한 흐름을 사용합니다. ([위키독스][1])

---

## 셀 18. 저장 상태 확인

```python
# =============================================================================
# [셀 18] Pinecone 인덱스 통계 확인
# =============================================================================

# 업로드 반영을 위해 잠시 대기
time.sleep(3)

stats = index.describe_index_stats()

print("인덱스 통계:")
print(stats)

namespace_info = stats.namespaces.get(NAMESPACE)

if namespace_info:
    print(
        f"\n'{NAMESPACE}'에 저장된 벡터 수:",
        namespace_info.vector_count
    )
else:
    print(f"\n'{NAMESPACE}' 네임스페이스를 아직 확인할 수 없습니다.")
```

---

# 1. 기본 유사도 검색

## 셀 19. `similarity_search()` 실행

```python
# =============================================================================
# [셀 19] 기본 유사도 검색
# =============================================================================

query = "누가 한글을 만들었나요?"

results = vectorstore.similarity_search(
    query=query,
    k=3
)

print("=" * 80)
print("유사도 기반 검색 결과")
print("=" * 80)
print("질문:", query)

for rank, doc in enumerate(results, start=1):
    print(f"\n[{rank}위]")
    print("내용:")
    print(doc.page_content)
    print("메타데이터:")
    print(doc.metadata)
```

예상 상위 결과에는 다음 내용이 포함됩니다.

```text
조선의 제4대 왕 세종대왕은 백성들이 쉽게 글을 읽고 쓸 수 있도록
훈민정음을 창제했다.
```

---

## 셀 20. 다른 질문으로 검색

```python
# =============================================================================
# [셀 20] 여러 질문으로 검색
# =============================================================================

queries = [
    "고려를 세운 사람은 누구인가요?",
    "임진왜란 때 활약한 장군은 누구인가요?",
    "대한민국 임시정부는 언제 어디에서 세워졌나요?",
    "조선 후기 실학자는 누구인가요?"
]

for query in queries:
    print("\n" + "=" * 80)
    print("질문:", query)
    print("=" * 80)

    results = vectorstore.similarity_search(
        query=query,
        k=2
    )

    for rank, doc in enumerate(results, start=1):
        print(f"\n[{rank}위]")
        print(doc.page_content)
```

---

# 2. 유사도 점수와 함께 검색

## 셀 21. `similarity_search_with_score()` 실행

```python
# =============================================================================
# [셀 21] 유사도 점수와 함께 검색
# =============================================================================

query = "세종대왕은 어떤 업적을 남겼나요?"

results_with_score = vectorstore.similarity_search_with_score(
    query=query,
    k=4
)

print("=" * 80)
print("유사도 점수 포함 검색 결과")
print("=" * 80)
print("질문:", query)

for rank, (doc, score) in enumerate(
    results_with_score,
    start=1
):
    print(f"\n[{rank}위]")
    print(f"점수: {score:.4f}")
    print("내용:")
    print(doc.page_content)
    print("메타데이터:")
    print(doc.metadata)
```

Pinecone 인덱스의 metric을 `cosine`으로 설정한 경우 일반적으로 점수가 클수록 쿼리와 가까운 문서입니다. 원문 역시 코사인 검색 점수를 1에 가까울수록 유사한 값으로 설명합니다. ([위키독스][1])

다만 점수는 확률이 아닙니다.

```text
0.85 → 85% 확률이라는 의미가 아님
```

검색 후보 사이의 상대적인 관련성을 비교하는 값으로 해석하는 것이 적절합니다.

---

## 셀 22. 검색 결과를 DataFrame으로 출력

```python
# =============================================================================
# [셀 22] 유사도 검색 결과를 표로 출력
# =============================================================================

query = "한글이 만들어진 시기와 목적을 알려주세요."

results_with_score = vectorstore.similarity_search_with_score(
    query=query,
    k=5
)

rows = []

for rank, (doc, score) in enumerate(
    results_with_score,
    start=1
):
    rows.append({
        "순위": rank,
        "유사도 점수": round(float(score), 4),
        "청크 번호": doc.metadata.get("chunk_id"),
        "출처": doc.metadata.get("source"),
        "문서 내용": doc.page_content
    })

result_df = pd.DataFrame(rows)

print("질문:", query)
display(result_df)
```

---

# 3. 점수 기준 검색

## 셀 23. `similarity_score_threshold` Retriever

유사도 점수가 일정 기준 이상인 문서만 반환하도록 설정할 수 있습니다.

```python
# =============================================================================
# [셀 23] 유사도 점수 임계값 기반 Retriever
# =============================================================================

threshold_retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.45
    }
)

query = "한글을 만든 왕은 누구인가요?"

threshold_results = threshold_retriever.invoke(query)

print("=" * 80)
print("점수 임계값 기반 검색")
print("=" * 80)
print("질문:", query)
print("반환된 문서 수:", len(threshold_results))

for rank, doc in enumerate(threshold_results, start=1):
    print(f"\n[{rank}위]")
    print(doc.page_content)
```

임계값이 너무 높으면 검색 결과가 없을 수 있습니다.

```python
"score_threshold": 0.8
```

반대로 너무 낮으면 관련성이 약한 문서도 포함될 수 있습니다.

```python
"score_threshold": 0.2
```

초기에는 실제 점수 분포를 확인한 후 기준을 조정하는 것이 좋습니다.

---

# 4. Retriever 방식으로 검색

## 셀 24. Vector Store Retriever 생성

RAG 체인에서는 벡터 저장소를 Retriever로 변환해 사용하는 경우가 많습니다.

```python
# =============================================================================
# [셀 24] Pinecone Vector Store Retriever 생성
# =============================================================================

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 3
    }
)

print(retriever)
```

---

## 셀 25. Retriever 검색 실행

```python
# =============================================================================
# [셀 25] Retriever로 문서 검색
# =============================================================================

query = "이순신 장군은 어떤 전쟁에서 활약했나요?"

retrieved_docs = retriever.invoke(query)

print("=" * 80)
print("Retriever 검색 결과")
print("=" * 80)
print("질문:", query)

for rank, doc in enumerate(retrieved_docs, start=1):
    print(f"\n[{rank}위]")
    print(doc.page_content)
    print("메타데이터:", doc.metadata)
```

---

# 5. 검색 결과를 RAG 컨텍스트로 변환

## 셀 26. 검색 문서를 하나의 문자열로 결합

```python
# =============================================================================
# [셀 26] 검색 결과를 LLM에 전달할 컨텍스트로 변환
# =============================================================================

def format_documents(documents: list[Document]) -> str:
    """
    검색된 Document 목록을 하나의 컨텍스트 문자열로 결합합니다.
    """

    if not documents:
        return "검색된 문서가 없습니다."

    formatted_chunks = []

    for index, doc in enumerate(documents, start=1):
        formatted_chunks.append(
            f"[문서 {index}]\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(formatted_chunks)


query = "세종대왕 시기의 과학 기술을 설명해주세요."

retrieved_docs = retriever.invoke(query)
context = format_documents(retrieved_docs)

print("질문:")
print(query)

print("\n검색 컨텍스트:")
print(context)
```

이 `context`를 LLM 프롬프트에 전달하면 기본적인 RAG 구조를 만들 수 있습니다.

```text
사용자 질문
    ↓
질문 임베딩
    ↓
Pinecone 유사도 검색
    ↓
관련 문서 반환
    ↓
LLM 프롬프트에 컨텍스트 전달
    ↓
최종 답변 생성
```

---

# 6. 재사용 가능한 검색 함수

## 셀 27. 검색 함수 작성

```python
# =============================================================================
# [셀 27] 재사용 가능한 Pinecone 검색 함수
# =============================================================================

def search_history(
    query: str,
    k: int = 3,
    include_score: bool = True
) -> pd.DataFrame:
    """
    한국사 Pinecone 벡터 저장소에서 문서를 검색합니다.

    Parameters
    ----------
    query : str
        검색할 질문
    k : int
        반환할 최대 문서 수
    include_score : bool
        유사도 점수 포함 여부

    Returns
    -------
    pd.DataFrame
        검색 결과
    """

    if not query or not query.strip():
        raise ValueError("검색 질문을 입력해야 합니다.")

    if k <= 0:
        raise ValueError("k는 1 이상의 정수여야 합니다.")

    rows = []

    if include_score:
        search_results = vectorstore.similarity_search_with_score(
            query=query,
            k=k
        )

        for rank, (doc, score) in enumerate(
            search_results,
            start=1
        ):
            rows.append({
                "순위": rank,
                "점수": round(float(score), 4),
                "청크 번호": doc.metadata.get("chunk_id"),
                "출처": doc.metadata.get("source"),
                "내용": doc.page_content
            })

    else:
        search_results = vectorstore.similarity_search(
            query=query,
            k=k
        )

        for rank, doc in enumerate(
            search_results,
            start=1
        ):
            rows.append({
                "순위": rank,
                "청크 번호": doc.metadata.get("chunk_id"),
                "출처": doc.metadata.get("source"),
                "내용": doc.page_content
            })

    return pd.DataFrame(rows)
```

---

## 셀 28. 검색 함수 실행

```python
result_df = search_history(
    query="정약용이 남긴 책과 사상은 무엇인가요?",
    k=4,
    include_score=True
)

display(result_df)
```

```python
result_df = search_history(
    query="한국의 대표적인 불교 문화유산은 무엇인가요?",
    k=3,
    include_score=True
)

display(result_df)
```

---

# 7. 기존 인덱스에 다시 연결

Colab 세션을 다시 시작해도 Pinecone에 저장된 데이터는 클라우드에 남아 있습니다. 따라서 문서를 다시 업로드하지 않고 기존 인덱스에 연결할 수 있습니다.

## 셀 29. 기존 Pinecone 인덱스 연결

```python
# =============================================================================
# [셀 29] 기존 Pinecone 인덱스에 다시 연결
# =============================================================================

existing_index = pc.Index(INDEX_NAME)

existing_vectorstore = PineconeVectorStore(
    index=existing_index,
    embedding=embeddings,
    namespace=NAMESPACE
)

print("기존 Pinecone 인덱스 연결 완료")
```

원문도 기존 인덱스에 다시 연결할 때 `PineconeVectorStore` 생성자를 직접 사용하는 방식을 제시합니다. ([위키독스][1])

---

## 셀 30. 기존 인덱스에서 검색

```python
# =============================================================================
# [셀 30] 기존 인덱스 검색
# =============================================================================

results = existing_vectorstore.similarity_search(
    query="고조선의 사회 모습을 알 수 있는 법은 무엇인가요?",
    k=2
)

for rank, doc in enumerate(results, start=1):
    print(f"\n[{rank}위]")
    print(doc.page_content)
```

---

# 8. 문서 추가

## 셀 31. 새 문서 추가

```python
# =============================================================================
# [셀 31] 기존 Pinecone 인덱스에 새 문서 추가
# =============================================================================

new_documents = [
    Document(
        page_content=(
            "직지심체요절은 고려 시대에 금속활자로 인쇄된 불교 서적이다. "
            "현존하는 세계에서 가장 오래된 금속활자 인쇄본으로 알려져 있다."
        ),
        metadata={
            "source": "additional_history.txt",
            "subject": "한국사",
            "topic": "고려 문화",
            "document_id": "korean-history-002"
        }
    ),
    Document(
        page_content=(
            "수원 화성은 정조가 건설한 성곽이다. "
            "정약용이 거중기 등의 기구를 설계하여 건설 과정에 활용했다."
        ),
        metadata={
            "source": "additional_history.txt",
            "subject": "한국사",
            "topic": "조선 후기",
            "document_id": "korean-history-003"
        }
    )
]

new_ids = [
    "additional-history-001",
    "additional-history-002"
]

added_ids = vectorstore.add_documents(
    documents=new_documents,
    ids=new_ids
)

print("추가된 문서 ID:", added_ids)
```

---

## 셀 32. 추가 문서 검색 확인

```python
# =============================================================================
# [셀 32] 새로 추가된 문서 검색
# =============================================================================

query = "세계에서 가장 오래된 금속활자 인쇄본은 무엇인가요?"

results = vectorstore.similarity_search_with_score(
    query=query,
    k=3
)

print("질문:", query)

for rank, (doc, score) in enumerate(results, start=1):
    print(f"\n[{rank}위] 점수: {score:.4f}")
    print(doc.page_content)
    print(doc.metadata)
```

---

# 9. 실습 데이터 정리

## 셀 33. 네임스페이스 데이터만 삭제

```python
# =============================================================================
# [셀 33] 실습 네임스페이스 데이터 삭제
# =============================================================================

index.delete(
    delete_all=True,
    namespace=NAMESPACE
)

print(f"'{NAMESPACE}' 네임스페이스 데이터 삭제 요청 완료")
```

이 코드는 Pinecone 인덱스 자체는 유지하고, 현재 실습에서 사용한 네임스페이스 데이터만 삭제합니다.

---

## 셀 34. 인덱스 전체 삭제

인덱스 자체가 더 이상 필요하지 않은 경우에만 실행합니다.

```python
# =============================================================================
# [셀 34] Pinecone 인덱스 전체 삭제
# 주의: 인덱스와 그 안의 모든 데이터가 삭제됩니다.
# =============================================================================

DELETE_INDEX = False

if DELETE_INDEX:
    pc.delete_index(INDEX_NAME)
    print(f"'{INDEX_NAME}' 인덱스를 삭제했습니다.")
else:
    print(
        "인덱스를 유지합니다.\n"
        "삭제하려면 DELETE_INDEX = True로 변경하세요."
    )
```

---

# 핵심 코드만 정리

## Pinecone 인덱스 생성

```python
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=PINECONE_API_KEY)

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )
```

## 문서 저장

```python
from langchain_pinecone import PineconeVectorStore

vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    index_name=INDEX_NAME,
    namespace=NAMESPACE
)
```

## 유사도 검색

```python
results = vectorstore.similarity_search(
    query="누가 한글을 만들었나요?",
    k=3
)
```

## 점수 포함 검색

```python
results = vectorstore.similarity_search_with_score(
    query="누가 한글을 만들었나요?",
    k=3
)

for doc, score in results:
    print(score)
    print(doc.page_content)
```

## Retriever 검색

```python
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

results = retriever.invoke(
    "세종대왕의 업적을 알려주세요."
)
```

---

# 원문 코드와 수정 코드의 주요 차이

| 항목             | 원문 예제            | 수정한 Colab 예제        |
| -------------- | ---------------- | ------------------- |
| 벡터 저장소         | Pinecone         | Pinecone            |
| 임베딩            | OpenAIEmbeddings | 무료 Hugging Face 임베딩 |
| OpenAI API 키   | 필요               | 불필요                 |
| Pinecone API 키 | 필요               | 필요                  |
| 문서 입력          | `history.txt`    | 코드에서 직접 생성          |
| 인덱스 차원         | 1,536 고정         | 임베딩 모델에서 자동 계산      |
| 재실행 처리         | 문서 중복 가능         | 네임스페이스 초기화          |
| 검색 방식          | 유사도 검색           | 유사도·점수·Retriever    |
| 결과 출력          | 텍스트              | 텍스트 및 DataFrame     |
| 기존 연결          | 기본 예제            | 재연결 코드 포함           |
| 데이터 정리         | 없음               | 네임스페이스·인덱스 삭제 포함    |

Pinecone은 외부 임베딩 모델을 사용할 때 인덱스의 `dimension`을 해당 모델의 출력 차원과 일치시켜야 합니다. 이번 코드가 차원을 자동으로 계산하도록 한 이유도 이 설정 오류를 방지하기 위한 것입니다. ([위키독스][1])

[1]: https://wikidocs.net/329474 "
            
    2-5-3-1. 유사도 기반 검색 (Similarity Search) - 랭체인(LangChain) 입문부터 응용까지 [ver 1.0+]

        "
[2]: https://docs.langchain.com/oss/python/integrations/vectorstores/pinecone?utm_source=chatgpt.com "Pinecone integration - Docs by LangChain"
[3]: https://docs.pinecone.io/reference/sdks/python/overview?utm_source=chatgpt.com "Pinecone Python SDK"
