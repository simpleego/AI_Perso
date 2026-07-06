# 2-6-RAG_retriver

Retrieval Augmented Generation (RAG)에서 검색도구(Retrievers)는 벡터 저장소에서 문서를 검색하는 핵심 구성 요소입니다.   
LangChain은 간단한 의미 검색부터 성능 향상을 위한 다양한 고급 검색 알고리즘을 지원합니다.  

## 주요내용

- 검색 기법 개요
- 검색 기법 선택 가이드
- 성능 비교


## 검색 기법 개요
RAG 시스템의 검색 품질은 최종 답변의 정확도에 직접적인 영향을 미칩니다. LangChain은 다양한 검색 전략을 제공하여 사용 사례에 맞는 최적의 검색 방식을 선택할 수 있습니다.

이 섹션에서는 기본 검색 기법과 검색 결과 최적화 기법을 다룹니다. 쿼리 자체를 개선하는 Query Enhancement 기법(Multi Query, Decomposition, Step Back, HyDE)은 2-7. RAG 최적화 > Query Enhancement에서 다룹니다.

## 기법	핵심 원리	장점	적합한 상황
Vector Store Retriever	벡터 유사도 검색	간단, 빠름	기본 RAG 구현
Contextual Compression	관련 내용만 추출	노이즈 제거, 비용 절감	긴 문서에서 핵심 추출
Ensemble Retriever	BM25 + 벡터 결합	키워드와 의미 검색 통합	전문 용어가 중요한 도메인
RAG-Fusion	RRF로 결과 병합	다양성과 관련성 균형	복잡한 질문
Reranker	Cross-Encoder 재정렬	검색 결과 정밀도 향상	정확도가 중요한 경우
검색 기법 선택 가이드
기본 검색

Vector Store Retriever: 모든 RAG 시스템의 기본. 단순하고 빠른 검색이 필요할 때
Contextual Compression: 검색된 문서가 길고 관련 없는 내용이 많을 때
검색 결과 최적화

Ensemble Retriever: 키워드 매칭이 중요한 기술/법률/의료 도메인
RAG-Fusion: 검색 결과의 다양성과 정확도를 모두 높이고 싶을 때
Reranker: 검색 결과의 순위를 정밀하게 재조정하고 싶을 때
Query Enhancement 기법 (2-7. RAG 최적화 참조)

쿼리 자체를 변환하거나 확장하여 검색 품질을 높이는 기법들은 2-7. RAG 최적화 > Query Enhancement 섹션에서 다룹니다:

Multi Query Retriever, Decomposition, Step Back Prompting, HyDE

## 성능 비교

<img width="688" height="342" alt="image" src="https://github.com/user-attachments/assets/3660a50f-82f7-47ec-be12-ca8040e5aefe" />

--- 
## 검색 기법 조합
여러 기법을 조합하여 사용할 수 있습니다. 예를 들어:

- Ensemble + Contextual Compression: 하이브리드 검색 후 관련 내용만 추출
- Ensemble + Reranker: 하이브리드 검색 후 재정렬로 정밀도 향상
- RAG-Fusion + Reranker: 다중 쿼리 검색 후 재정렬
상황에 맞는 최적의 조합을 실험해보세요.

<img width="1240" height="526" alt="image" src="https://github.com/user-attachments/assets/73f12b24-9d25-44bf-ba65-6a2c13723f61" />
