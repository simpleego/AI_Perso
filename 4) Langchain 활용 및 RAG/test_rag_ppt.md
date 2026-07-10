# RAG Document Loader 강의자료

## 슬라이드 1: 표지
```markdown
# RAG (Retrieval-Augmented Generation)
## 2-2. Document Loader

강사: [이름]
날짜: [날짜]
```

---

## 슬라이드 2: 목차
```markdown
# 목차

1. RAG 개요
2. Document Loader란?
3. WebBaseLoader - 웹 문서 로딩
4. TextLoader - 텍스트 문서 로딩
5. DirectoryLoader - 디렉토리 로딩
6. 실습 및 요약
```

---

## 슬라이드 3: RAG 개요
```markdown
# 1. RAG (Retrieval-Augmented Generation) 개요

## RAG 파이프라인의 5단계

1. **데이터 로드 (Load Data)** ← 오늘 배울 내용
2. 텍스트 분할 (Text Split)
3. 인덱싱 (Indexing)
4. 검색 (Retrieval)
5. 생성 (Generation)

## RAG의 핵심
- 외부 데이터를 LLM에 주입하여 정확하고 풍부한 정보 기반 답변 생성
```

---

## 슬라이드 4: Document Loader란?
```markdown
# 2. Document Loader란?

## 정의
- 다양한 소스에서 데이터를 불러와 LangChain의 Document 형식으로 변환하는 도구

## 주요 기능
1. **웹 페이지**: URL에서 데이터 추출
2. **텍스트 파일**: .txt 파일 로드
3. **PDF 문서**: PDF 파일 파싱
4. **디렉토리**: 폴더 내 여러 파일 일괄 로드

## 중요성
- RAG 시스템의 첫 단계
- 품질 좋은 데이터 수집이 시스템 성능 결정
```

---

## 슬라이드 5: WebBaseLoader 소개
```markdown
# 3. WebBaseLoader - 웹 문서 로딩

## 기능
- 웹페이지의 HTML을 파싱하여 텍스트 추출
- BeautifulSoup을 사용하여 HTML 구조 분석

## 주요 파라미터
- `web_paths`: 로드할 URL 목록
- `bs_kwargs`: BeautifulSoup 설정 옵션
```

---

## 슬라이드 6: WebBaseLoader 실습
```markdown
## WebBaseLoader 코드 예제

```python
from langchain_community.document_loaders import WebBaseLoader
import bs4

# 단일 URL 로드
loader = WebBaseLoader("https://example.com")
docs = loader.load()

# 여러 URL 로드 + 특정 태그만 추출
loader = WebBaseLoader(
    web_paths=("https://url1.com", "https://url2.com"),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("article-header", "article-content")
        )
    ),
)
docs = loader.load()
```

## 출력 확인
```python
print(len(docs))  # 문서 개수
print(docs[0].page_content[:100])  # 첫 100자
print(docs[0].metadata)  # 메타데이터 (source URL)
```
```

---

## 슬라이드 7: TextLoader 소개
```markdown
# 4. TextLoader - 텍스트 문서 로딩

## 기능
- 로컬 텍스트 파일(.txt)을 로드
- 가장 기본적인 Document Loader

## 사용법
```python
from langchain_community.document_loaders import TextLoader

# 텍스트 파일 로드
loader = TextLoader("history.txt")
data = loader.load()

# 결과 확인
print(type(data))  # <class 'list'>
print(len(data))   # 1 (문서 1개)
print(data[0].page_content)  # 파일 내용
print(data[0].metadata)  # {'source': 'history.txt'}
```

## Document 객체 구조
- `page_content`: 실제 텍스트 내용
- `metadata`: 소스 파일 정보
```

---

## 슬라이드 8: DirectoryLoader 소개
```markdown
# 5. DirectoryLoader - 디렉토리 로딩

## 기능
- 특정 폴더 내의 여러 파일을 한 번에 로드
- glob 패턴을 사용하여 파일 필터링

## 사용법
```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader

# './' 폴더의 모든 .txt 파일 로드
loader = DirectoryLoader(
    path='./',
    glob='*.txt',
    loader_cls=TextLoader
)
data = loader.load()

print(len(data))  # 로드된 문서 개수
```

## glob 패턴 예시
- `*.txt`: 모든 txt 파일
- `*.pdf`: 모든 PDF 파일
- `**/*.txt`: 하위 폴더 포함 모든 txt 파일
```

---

## 슬라이드 9: Document Loader 비교
```markdown
# Document Loader 비교

| 로더 | 용도 | 입력 | 출력 |
|------|------|------|------|
| **WebBaseLoader** | 웹페이지 크롤링 | URL | HTML 파싱 텍스트 |
| **TextLoader** | 단일 텍스트 파일 | .txt 파일 | 텍스트 내용 |
| **DirectoryLoader** | 폴더 내 여러 파일 | 디렉토리 경로 | 여러 Document |

## 공통점
- 모두 `load()` 메서드 사용
- `Document` 객체 리스트 반환
- `page_content`와 `metadata` 포함
```

---

## 슬라이드 10: 실습 예제
```markdown
# 6. 실습 예제

## 예제 1: 위키백과 데이터 로드
```python
from langchain_community.document_loaders import WebBaseLoader

url = "https://ko.wikipedia.org/wiki/인공지능"
loader = WebBaseLoader(url)
docs = loader.load()

print(f"문서 길이: {len(docs[0].page_content)}자")
```

## 예제 2: 여러 텍스트 파일 로드
```python
from langchain_community.document_loaders import DirectoryLoader

# data 폴더의 모든 txt 파일 로드
loader = DirectoryLoader('./data', glob='*.txt')
documents = loader.load()

print(f"총 {len(documents)}개 문서 로드")
```
```

---

## 슬라이드 11: 주의사항
```markdown
## 주의사항 및 팁

### WebBaseLoader
- ✅ 웹사이트의 robots.txt 확인
- ✅ 너무 많은 URL 동시 요청 금지
- ✅ HTML 구조 변경 시 파싱 오류 가능

### TextLoader & DirectoryLoader
- ✅ 인코딩 문제 주의 (utf-8 권장)
- ✅ 대용량 파일은 메모리 주의
- ✅ 파일 경로 확인 필수

### 공통
- ✅ 메타데이터 활용 (source 추적)
- ✅ 로드 후 데이터 품질 확인
```

---

## 슬라이드 12: 다음 단계
```markdown
## RAG 파이프라인 다음 단계

Document Loader로 데이터 로드 후:

1. ✅ **데이터 로드** (완료)
2. ➡️ **텍스트 분할** (Text Splitter)
   - 긴 문서를 작은 chunk로 분할
3. ➡️ **인덱싱** (Embedding & Vector Store)
   - 텍스트를 벡터로 변환하여 저장
4. ➡️ **검색** (Retrieval)
   - 사용자 질문과 유사한 문서 검색
5. ➡️ **생성** (Generation)
   - LLM이 검색된 문서 기반으로 답변 생성

## 다음 강의 예고
- Text Splitter: 문서를 효과적으로 분할하는 방법
```

---

## 슬라이드 13: 요약
```markdown
# 요약

## 핵심 포인트

1. **Document Loader**는 RAG의 첫 단계
2. 다양한 소스에서 데이터 로드 가능
   - 웹: `WebBaseLoader`
   - 텍스트: `TextLoader`
   - 폴더: `DirectoryLoader`
3. 모두 `Document` 객체 리스트 반환
4. `page_content` (내용) + `metadata` (정보)

## 실습 과제
1. 관심 있는 웹사이트 3개에서 데이터 로드
2. 로컬 텍스트 파일 5개以上 로드
3. 로드한 문서의 메타데이터 확인
```

---

## 슬라이드 14: Q&A
```markdown
# Q&A

## 질문 시간

## 참고 자료
- LangChain 공식 문서: https://python.langchain.com/
- Wikidocs RAG 강의: https://wikidocs.net/

## 감사합니다!
```

---

이 PPT 강의자료는 마크다운 형식으로 작성되었으며, 각 슬라이드는 `---`로 구분됩니다. 이 내용을 PPT 제작 도구(Google Slides, PowerPoint, Marp, Reveal.js 등)에 맞게 변환하여 사용하시면 됩니다.
