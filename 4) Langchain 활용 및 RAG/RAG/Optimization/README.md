# RAG 최적화 5가지 카테고리 실습

위키독스의 RAG 최적화 의사결정 가이드와 품질 체크리스트를 바탕으로 만든
독립 실행형 Python 실습입니다. 필요한 문서는 Loader로 이미 불러왔다고 가정하고
각 파일에서 학사규정 예제 `Document`를 생성합니다.

## 실습 구성

| 파일 | 문제 증상 | 적용 기법 | 비교 포인트 |
|---|---|---|---|
| `01_query_enhancement.py` | 질문이 모호함 | Multi Query | 단일 검색 대비 Recall |
| `02_indexing_enhancement.py` | 작은 청크는 문맥이 부족함 | Small-to-Big | 검색 정밀도와 부모 문맥 |
| `03_retriever_enhancement.py` | 키워드·의미 검색의 한계 | Hybrid + Reranker | 재정렬 전후 순위 |
| `04_generator_enhancement.py` | 긴 문맥·근거 없는 생성 | LongContextReorder + 근거 프롬프트 | 문서 순서와 인용 |
| `05_pipeline_enhancement.py` | 모든 질문에 같은 전략 사용 | 동적 라우팅 | 품질·지연·비용 |

## 설치와 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:OPENAI_API_KEY="본인의_API_키"

python 01_query_enhancement.py
python 02_indexing_enhancement.py
python 03_retriever_enhancement.py
python 04_generator_enhancement.py
python 05_pipeline_enhancement.py
```

최초 실행 시 Hugging Face 임베딩·Reranker 모델을 내려받으므로 시간이 걸릴 수 있습니다.
실습 1, 4, 5는 OpenAI API를 사용하고 실습 2는 로컬 임베딩만 사용합니다.

## 학생 결과 보고서 권장 항목

1. 기준선과 최적화 방식의 검색 결과
2. Recall@k 또는 정답 문서 순위
3. 반환 컨텍스트 길이
4. LLM 호출 횟수와 대략적인 비용
5. 지연 시간
6. 품질 향상과 비용 증가 사이의 결론

전자책 체크리스트처럼 인덱싱, 검색, 생성 단계를 따로 점검한 뒤 전체 파이프라인을
평가하는 것이 핵심입니다.
