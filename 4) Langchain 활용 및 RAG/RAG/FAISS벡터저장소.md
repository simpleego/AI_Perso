아래 코드는 위키독스의 **FAISS + Hugging Face 임베딩 + 코사인 거리 기반 검색** 흐름을 참고하되, 최신 LangChain 패키지 구조에 맞춰 수정한 Colab 실습 예제입니다. 참고 페이지에서는 `jhgan/ko-sbert-nli` 모델과 `FAISS.from_documents()`를 이용해 유사도 검색을 수행합니다. ([위키독스][1])

이번 실습은 별도 파일 업로드 없이 코드에서 직접 문서를 생성하며, 동일한 질문에 대해 다음 두 결과를 비교합니다.

* **유사도 검색**: 질문과 가장 비슷한 문서를 우선 선택
* **MMR 검색**: 질문과 관련성이 있으면서, 검색 결과끼리는 서로 중복되지 않도록 선택

---

# Colab 전체 실습 코드

## 셀 1. 라이브러리 설치

```python
# =============================================================================
# [셀 1] 필요한 라이브러리 설치
# =============================================================================

!pip install -qU \
    langchain \
    langchain-community \
    langchain-huggingface \
    faiss-cpu \
    sentence-transformers \
    pandas
```

설치가 끝난 뒤 import 오류가 발생하면 다음 메뉴에서 런타임을 다시 시작합니다.

```text
런타임 → 세션 다시 시작
```

---

## 셀 2. 라이브러리 불러오기

```python
# =============================================================================
# [셀 2] 라이브러리 불러오기
# =============================================================================

import pandas as pd

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_huggingface import HuggingFaceEmbeddings
```

---

## 셀 3. 실습용 문서 직접 생성

비슷한 내용의 문서를 여러 개 넣어야 유사도 검색과 MMR 검색의 차이를 쉽게 확인할 수 있습니다.

```python
# =============================================================================
# [셀 3] 실습용 문서 생성
# =============================================================================

documents = [
    Document(
        page_content=(
            "파이썬은 문법이 간결하고 배우기 쉬운 프로그래밍 언어이다. "
            "데이터 분석, 인공지능, 웹 개발, 자동화 등 다양한 분야에서 사용된다."
        ),
        metadata={
            "id": 1,
            "title": "파이썬 개요",
            "category": "파이썬"
        }
    ),

    Document(
        page_content=(
            "파이썬은 데이터 분석 분야에서 널리 사용된다. "
            "Pandas를 사용하면 표 형태의 데이터를 처리하고 분석할 수 있다."
        ),
        metadata={
            "id": 2,
            "title": "파이썬 데이터 분석",
            "category": "파이썬"
        }
    ),

    Document(
        page_content=(
            "파이썬의 NumPy 라이브러리는 배열과 행렬 계산을 지원한다. "
            "대규모 수치 데이터를 빠르게 처리할 때 유용하다."
        ),
        metadata={
            "id": 3,
            "title": "파이썬 수치 계산",
            "category": "파이썬"
        }
    ),

    Document(
        page_content=(
            "파이썬은 머신러닝 모델을 개발할 때 많이 사용된다. "
            "Scikit-learn을 이용하면 분류, 회귀, 군집화 모델을 구현할 수 있다."
        ),
        metadata={
            "id": 4,
            "title": "파이썬 머신러닝",
            "category": "인공지능"
        }
    ),

    Document(
        page_content=(
            "딥러닝은 인공신경망을 여러 층으로 구성하여 복잡한 패턴을 학습하는 기술이다. "
            "대표적인 프레임워크로 PyTorch와 TensorFlow가 있다."
        ),
        metadata={
            "id": 5,
            "title": "딥러닝 개요",
            "category": "인공지능"
        }
    ),

    Document(
        page_content=(
            "자연어 처리는 컴퓨터가 사람의 언어를 이해하고 생성하도록 만드는 인공지능 기술이다. "
            "번역, 문서 요약, 감정 분석, 챗봇 등에 활용된다."
        ),
        metadata={
            "id": 6,
            "title": "자연어 처리",
            "category": "인공지능"
        }
    ),

    Document(
        page_content=(
            "LangChain은 대규모 언어 모델을 활용한 애플리케이션 개발을 지원하는 프레임워크이다. "
            "프롬프트, 모델, 검색기, 도구 등을 연결하여 사용할 수 있다."
        ),
        metadata={
            "id": 7,
            "title": "LangChain 개요",
            "category": "LangChain"
        }
    ),

    Document(
        page_content=(
            "RAG는 외부 문서에서 관련 정보를 검색한 후, 검색 결과를 언어 모델에 제공하여 "
            "답변의 정확성과 근거성을 높이는 방법이다."
        ),
        metadata={
            "id": 8,
            "title": "RAG 개요",
            "category": "RAG"
        }
    ),

    Document(
        page_content=(
            "벡터 데이터베이스는 문서를 임베딩 벡터로 저장하고, "
            "사용자의 질문과 의미적으로 유사한 문서를 검색하는 데 사용된다."
        ),
        metadata={
            "id": 9,
            "title": "벡터 데이터베이스",
            "category": "RAG"
        }
    ),

    Document(
        page_content=(
            "FAISS는 고차원 벡터에서 유사한 벡터를 빠르게 찾기 위한 검색 라이브러리이다. "
            "LangChain의 벡터 저장소로 활용할 수 있다."
        ),
        metadata={
            "id": 10,
            "title": "FAISS 검색",
            "category": "RAG"
        }
    ),

    Document(
        page_content=(
            "MMR 검색은 질문과 관련성이 높은 문서를 선택하면서도 "
            "검색 결과 사이의 중복을 줄여 다양한 정보를 제공하는 검색 방법이다."
        ),
        metadata={
            "id": 11,
            "title": "MMR 검색",
            "category": "검색"
        }
    ),

    Document(
        page_content=(
            "코사인 유사도는 두 벡터가 이루는 각도를 이용하여 유사성을 측정한다. "
            "문서 길이보다 벡터의 방향을 중심으로 비교하는 특징이 있다."
        ),
        metadata={
            "id": 12,
            "title": "코사인 유사도",
            "category": "검색"
        }
    ),
]

print(f"생성된 문서 수: {len(documents)}개")

for document in documents:
    print(
        f"[{document.metadata['id']:02d}] "
        f"{document.metadata['title']} "
        f"- {document.metadata['category']}"
    )
```

---

## 셀 4. Hugging Face 임베딩 모델 생성

API 키가 필요 없는 다국어 임베딩 모델을 사용합니다.

```python
# =============================================================================
# [셀 4] Hugging Face 임베딩 모델 생성
# =============================================================================

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,

    # Colab CPU에서도 실행 가능
    # GPU를 사용하려면 {"device": "cuda"}로 변경할 수 있음
    model_kwargs={
        "device": "cpu"
    },

    # 코사인 유사도 계산에 적합하도록 벡터 정규화
    encode_kwargs={
        "normalize_embeddings": True
    }
)

print("임베딩 모델 생성 완료")
print("모델:", MODEL_NAME)
```

처음 실행할 때 Hugging Face에서 모델을 내려받으므로 다운로드 메시지가 출력될 수 있습니다.

---

## 셀 5. FAISS 벡터 저장소 생성

```python
# =============================================================================
# [셀 5] FAISS 벡터 저장소 생성
# =============================================================================

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings,
    distance_strategy=DistanceStrategy.COSINE
)

print("FAISS 벡터 저장소 생성 완료")
print("저장된 문서 수:", vectorstore.index.ntotal)
print("거리 계산 방식:", vectorstore.distance_strategy)
```

위키독스 예제 역시 문서를 임베딩 벡터로 변환해 FAISS에 저장하고, `DistanceStrategy.COSINE`으로 코사인 기반 검색을 설정합니다. ([위키독스][1])

---

# 1. 유사도 기반 검색

## 셀 6. 유사도 검색 실행

```python
# =============================================================================
# [셀 6] 유사도 기반 검색
# =============================================================================

query = "파이썬을 이용한 데이터 분석과 인공지능 활용 방법을 알려줘"

similarity_results = vectorstore.similarity_search(
    query=query,
    k=4
)

print("=" * 80)
print("유사도 기반 검색 결과")
print("=" * 80)
print("질문:", query)

for rank, document in enumerate(similarity_results, start=1):
    print(f"\n[{rank}위]")
    print("문서 ID:", document.metadata["id"])
    print("제목:", document.metadata["title"])
    print("분류:", document.metadata["category"])
    print("내용:", document.page_content)
```

### 예상 결과의 특징

상위 결과에 다음처럼 **파이썬 관련 문서가 집중**될 가능성이 큽니다.

```text
파이썬 데이터 분석
파이썬 머신러닝
파이썬 개요
파이썬 수치 계산
```

질문과 직접적으로 비슷한 문서를 잘 찾지만, 결과 내용이 서로 비슷할 수 있습니다.

---

## 셀 7. 거리 점수를 포함한 유사도 검색

```python
# =============================================================================
# [셀 7] 거리 점수를 포함한 유사도 검색
# =============================================================================

similarity_results_with_score = vectorstore.similarity_search_with_score(
    query=query,
    k=4
)

similarity_rows = []

for rank, (document, score) in enumerate(
    similarity_results_with_score,
    start=1
):
    similarity_rows.append({
        "순위": rank,
        "문서 ID": document.metadata["id"],
        "제목": document.metadata["title"],
        "분류": document.metadata["category"],
        "FAISS 거리": round(float(score), 4),
        "문서 내용": document.page_content
    })

similarity_df = pd.DataFrame(similarity_rows)

display(similarity_df)
```

### 점수 해석 시 주의점

여기서 반환되는 값은 일반적인 의미의 “유사도 확률”이 아니라 FAISS 검색에서 사용하는 **거리 값**입니다.

```text
거리 값이 작음 → 질문과 더 가까움
거리 값이 큼 → 질문과 더 멂
```

따라서 점수가 높을수록 항상 더 좋은 결과라고 해석하면 안 됩니다.

---

# 2. MMR 기반 검색

## 셀 8. MMR 검색 실행

```python
# =============================================================================
# [셀 8] MMR 기반 검색
# =============================================================================

mmr_results = vectorstore.max_marginal_relevance_search(
    query=query,

    # 최종 반환할 문서 수
    k=4,

    # 우선 검색할 후보 문서 수
    fetch_k=10,

    # 관련성과 다양성의 균형
    # 1에 가까울수록 질문과의 유사도 중심
    # 0에 가까울수록 문서 간 다양성 중심
    lambda_mult=0.3
)

print("=" * 80)
print("MMR 기반 검색 결과")
print("=" * 80)
print("질문:", query)

for rank, document in enumerate(mmr_results, start=1):
    print(f"\n[{rank}위]")
    print("문서 ID:", document.metadata["id"])
    print("제목:", document.metadata["title"])
    print("분류:", document.metadata["category"])
    print("내용:", document.page_content)
```

### 예상 결과의 특징

MMR은 다음과 같이 서로 다른 관점의 문서를 선택할 가능성이 있습니다.

```text
파이썬 데이터 분석
파이썬 머신러닝
자연어 처리
LangChain 개요
```

또는 다음처럼 검색 관련 배경 문서를 포함할 수도 있습니다.

```text
파이썬 데이터 분석
파이썬 머신러닝
벡터 데이터베이스
MMR 검색
```

즉, MMR은 질문과 관련된 문서를 선택하면서도 파이썬 설명만 반복되지 않도록 결과를 다양화합니다.

---

# 3. 두 검색 결과 비교

## 셀 9. 비교 테이블 출력

```python
# =============================================================================
# [셀 9] 유사도 검색과 MMR 검색 결과 비교
# =============================================================================

comparison_rows = []

max_length = max(
    len(similarity_results),
    len(mmr_results)
)

for index in range(max_length):
    similarity_doc = (
        similarity_results[index]
        if index < len(similarity_results)
        else None
    )

    mmr_doc = (
        mmr_results[index]
        if index < len(mmr_results)
        else None
    )

    comparison_rows.append({
        "순위": index + 1,

        "유사도 검색 제목": (
            similarity_doc.metadata["title"]
            if similarity_doc
            else ""
        ),

        "유사도 검색 분류": (
            similarity_doc.metadata["category"]
            if similarity_doc
            else ""
        ),

        "MMR 검색 제목": (
            mmr_doc.metadata["title"]
            if mmr_doc
            else ""
        ),

        "MMR 검색 분류": (
            mmr_doc.metadata["category"]
            if mmr_doc
            else ""
        )
    })

comparison_df = pd.DataFrame(comparison_rows)

display(comparison_df)
```

---

## 셀 10. 문서 분류 다양성 비교

```python
# =============================================================================
# [셀 10] 검색 결과의 다양성 비교
# =============================================================================

similarity_categories = [
    document.metadata["category"]
    for document in similarity_results
]

mmr_categories = [
    document.metadata["category"]
    for document in mmr_results
]

print("유사도 검색 분류 목록:")
print(similarity_categories)

print("\nMMR 검색 분류 목록:")
print(mmr_categories)

print("\n유사도 검색의 서로 다른 분류 수:")
print(len(set(similarity_categories)))

print("\nMMR 검색의 서로 다른 분류 수:")
print(len(set(mmr_categories)))
```

예를 들어 다음과 같이 출력될 수 있습니다.

```text
유사도 검색 분류 목록:
['파이썬', '인공지능', '파이썬', '파이썬']

MMR 검색 분류 목록:
['파이썬', '인공지능', 'RAG', 'LangChain']

유사도 검색의 서로 다른 분류 수:
2

MMR 검색의 서로 다른 분류 수:
4
```

실제 순위는 임베딩 모델이나 라이브러리 버전에 따라 조금 달라질 수 있지만, 일반적으로 MMR 결과의 주제 구성이 더 다양하게 나타납니다.

---

# 4. Retriever 방식으로 검색

실제 RAG 프로그램에서는 벡터 저장소의 검색 메서드를 직접 호출하기보다 Retriever로 변환하여 사용하는 경우가 많습니다.

## 셀 11. 유사도 검색 Retriever

```python
# =============================================================================
# [셀 11] 유사도 검색 Retriever
# =============================================================================

similarity_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4
    }
)

similarity_retriever_results = similarity_retriever.invoke(query)

print("=" * 80)
print("Similarity Retriever 검색 결과")
print("=" * 80)

for rank, document in enumerate(
    similarity_retriever_results,
    start=1
):
    print(
        f"{rank}위: "
        f"{document.metadata['title']} "
        f"({document.metadata['category']})"
    )
```

---

## 셀 12. MMR 검색 Retriever

```python
# =============================================================================
# [셀 12] MMR 검색 Retriever
# =============================================================================

mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.3
    }
)

mmr_retriever_results = mmr_retriever.invoke(query)

print("=" * 80)
print("MMR Retriever 검색 결과")
print("=" * 80)

for rank, document in enumerate(
    mmr_retriever_results,
    start=1
):
    print(
        f"{rank}위: "
        f"{document.metadata['title']} "
        f"({document.metadata['category']})"
    )
```

---

# 5. `lambda_mult` 값에 따른 결과 비교

`lambda_mult`는 MMR 검색에서 매우 중요한 설정입니다.

|     값 | 검색 성향                |
| ----: | -------------------- |
| `1.0` | 질문과의 유사도를 가장 중요하게 평가 |
| `0.7` | 유사도를 비교적 중요하게 평가     |
| `0.5` | 유사도와 다양성을 균형 있게 평가   |
| `0.3` | 결과의 다양성을 비교적 중요하게 평가 |
| `0.0` | 문서 간 다양성을 가장 중요하게 평가 |

## 셀 13. 여러 설정값 비교

```python
# =============================================================================
# [셀 13] lambda_mult 값에 따른 MMR 결과 비교
# =============================================================================

lambda_values = [0.0, 0.3, 0.5, 0.7, 1.0]

lambda_comparison_rows = []

for lambda_value in lambda_values:
    results = vectorstore.max_marginal_relevance_search(
        query=query,
        k=4,
        fetch_k=10,
        lambda_mult=lambda_value
    )

    titles = [
        document.metadata["title"]
        for document in results
    ]

    categories = [
        document.metadata["category"]
        for document in results
    ]

    lambda_comparison_rows.append({
        "lambda_mult": lambda_value,
        "검색 성향": (
            "다양성 중심"
            if lambda_value < 0.5
            else "유사도 중심"
            if lambda_value > 0.5
            else "균형"
        ),
        "서로 다른 분류 수": len(set(categories)),
        "분류": " → ".join(categories),
        "검색 문서": " → ".join(titles)
    })

lambda_comparison_df = pd.DataFrame(lambda_comparison_rows)

display(lambda_comparison_df)
```

---

# 6. 질문을 바꾸어 반복 실습

## 셀 14. 검색 비교 함수

```python
# =============================================================================
# [셀 14] 유사도 검색과 MMR 검색을 비교하는 함수
# =============================================================================

def compare_search_results(
    query: str,
    k: int = 4,
    fetch_k: int = 10,
    lambda_mult: float = 0.3
) -> pd.DataFrame:
    """
    같은 질문에 대한 유사도 검색과 MMR 검색 결과를 비교합니다.

    Parameters
    ----------
    query : str
        검색 질문
    k : int
        최종 반환할 문서 수
    fetch_k : int
        MMR이 먼저 검색할 후보 문서 수
    lambda_mult : float
        MMR의 관련성-다양성 조절값
    """

    similarity_docs = vectorstore.similarity_search(
        query=query,
        k=k
    )

    mmr_docs = vectorstore.max_marginal_relevance_search(
        query=query,
        k=k,
        fetch_k=fetch_k,
        lambda_mult=lambda_mult
    )

    rows = []

    for index in range(k):
        similarity_doc = (
            similarity_docs[index]
            if index < len(similarity_docs)
            else None
        )

        mmr_doc = (
            mmr_docs[index]
            if index < len(mmr_docs)
            else None
        )

        rows.append({
            "순위": index + 1,

            "유사도 검색": (
                similarity_doc.metadata["title"]
                if similarity_doc
                else ""
            ),

            "유사도 분류": (
                similarity_doc.metadata["category"]
                if similarity_doc
                else ""
            ),

            "MMR 검색": (
                mmr_doc.metadata["title"]
                if mmr_doc
                else ""
            ),

            "MMR 분류": (
                mmr_doc.metadata["category"]
                if mmr_doc
                else ""
            )
        })

    print("=" * 80)
    print("질문:", query)
    print("k:", k)
    print("fetch_k:", fetch_k)
    print("lambda_mult:", lambda_mult)
    print("=" * 80)

    return pd.DataFrame(rows)
```

---

## 셀 15. 비교 함수 실행

```python
result_df = compare_search_results(
    query="RAG 시스템에서 문서를 검색하는 방법은 무엇인가?",
    k=4,
    fetch_k=10,
    lambda_mult=0.3
)

display(result_df)
```

다른 질문도 실행할 수 있습니다.

```python
result_df = compare_search_results(
    query="인공지능을 파이썬으로 개발하려면 무엇을 공부해야 하는가?",
    k=4,
    fetch_k=10,
    lambda_mult=0.3
)

display(result_df)
```

```python
result_df = compare_search_results(
    query="의미가 비슷한 문서를 벡터로 검색하는 방법을 설명해줘",
    k=4,
    fetch_k=10,
    lambda_mult=0.2
)

display(result_df)
```

---

# 핵심 코드만 정리

```python
# 유사도 검색
similarity_docs = vectorstore.similarity_search(
    query,
    k=4
)

# MMR 검색
mmr_docs = vectorstore.max_marginal_relevance_search(
    query,
    k=4,
    fetch_k=10,
    lambda_mult=0.3
)
```

Retriever로 사용할 때는 다음과 같습니다.

```python
# 유사도 Retriever
similarity_retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# MMR Retriever
mmr_retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.3
    }
)
```

# 결과 해석

**유사도 검색**은 질문과 가장 가까운 문서를 순서대로 반환합니다. 관련성이 높은 문서를 찾는 데 효과적이지만, 내용이 비슷한 문서가 반복될 수 있습니다. 위키독스에서도 질문을 임베딩하고, 저장된 문서 벡터와 비교한 다음 유사도 순서로 결과를 반환하는 과정으로 설명합니다. ([위키독스][1])

**MMR 검색**은 두 가지를 함께 고려합니다.

```text
1. 질문과 문서가 얼마나 관련 있는가
2. 이미 선택한 문서와 얼마나 다른 정보를 제공하는가
```

따라서 동일한 내용이 반복되는 것을 줄이고 여러 관점의 문서를 가져와야 하는 RAG 시스템에서 유용합니다.

실무에서는 다음 설정부터 시작하는 것이 무난합니다.

```python
search_kwargs={
    "k": 4,
    "fetch_k": 10,
    "lambda_mult": 0.3
}
```

* 정확한 한 가지 답을 찾는 경우: `similarity`
* 폭넓은 근거와 다양한 문맥이 필요한 경우: `mmr`
* MMR 결과가 지나치게 넓어지면: `lambda_mult`를 `0.5~0.8`로 높임
* 결과가 너무 비슷하면: `lambda_mult`를 `0.1~0.4`로 낮춤

[1]: https://wikidocs.net/231593 "2-5-2-1. 유사도 기반 검색 (Similarity search) - 랭체인(LangChain) 입문부터 응용까지 [ver 1.0+]"
