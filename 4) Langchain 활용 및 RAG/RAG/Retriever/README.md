# RAG Retriever 5종 학생 실습

위키독스의 Retriever 단원 구성을 참고해 같은 예제 문서군으로 검색 방식의 차이를
관찰하도록 만든 독립 실행형 Python 실습입니다. 원본 PDF 로딩은 완료되었다고 가정하고
각 파일 안에서 `Document` 객체를 직접 생성합니다.

## 환경 준비

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

실습 2와 4는 OpenAI API를 사용합니다.

```powershell
$env:OPENAI_API_KEY="본인의_API_키"
```

첫 실행 때 Hugging Face 모델이 다운로드되므로 시간이 걸릴 수 있습니다.

## 권장 실행 순서

1. `python 01_vector_store_retriever.py`
2. `python 02_contextual_compression.py`
3. `python 03_ensemble_retriever.py`
4. `python 04_rag_fusion.py`
5. `python 05_cross_encoder_reranker.py`

각 파일 끝의 `실습 과제`를 수행하고, 변경 전후의 검색 결과 순위와 이유를 표로
정리해 보세요.

## 학습 포인트

| 파일 | 핵심 메서드/개념 | 관찰할 점 |
|---|---|---|
| 01 | `as_retriever()`, `invoke()`, MMR | 관련성과 다양성의 균형 |
| 02 | `LLMChainExtractor`, `ContextualCompressionRetriever` | 문서 수·문자 수 감소 |
| 03 | `BM25Retriever`, `EnsembleRetriever` | 키워드와 의미 검색의 상호 보완 |
| 04 | 다중 쿼리, 사용자 정의 RRF | 여러 검색 순위의 융합 |
| 05 | `CrossEncoderReranker` | recall 중심 후보 검색과 precision 중심 재정렬 |
