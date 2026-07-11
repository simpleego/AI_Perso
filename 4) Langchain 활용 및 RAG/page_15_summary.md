# autogen multi agent examples

<img width="974" height="792" alt="image" src="https://github.com/user-attachments/assets/64c45070-afbf-4e0e-84c4-f39059be0693" />


## 먼저 그림의 성격부터 바로잡으면

이 그림은 **LangChain의 메모리 기능을 직접 설명한 그림이라기보다**, Microsoft 연구진이 제안한 **AutoGen 멀티에이전트 프레임워크의 6가지 응용 구조**입니다. 다만 각 에이전트가 대화 기록, 검색 문서, 실행 결과, 환경 상태를 어떻게 공유하거나 분리하는지를 보여주기 때문에 **멀티에이전트 시스템에서 메모리가 작동하는 방식**을 설명하기에 적합합니다. ([ar5iv][1])

LangChain·LangGraph 관점에서 메모리는 단순한 채팅 기록만 의미하지 않습니다.

| 메모리 종류       | 저장되는 내용                        |
| ------------ | ------------------------------ |
| 대화 메모리       | 사용자 질문, 에이전트 답변, 이전 메시지        |
| 작업 상태 메모리    | 현재 단계, 실행 결과, 오류, 다음 수행 작업     |
| 외부 지식 메모리    | PDF, DB, 벡터 데이터베이스, 검색 결과      |
| 환경 상태 메모리    | 체스판, 게임 위치, 보유 물건, 실행 중인 코드 상태 |
| 에이전트별 개별 메모리 | 특정 역할에만 필요한 대화와 정보             |
| 공유 메모리       | 여러 에이전트가 공동으로 읽는 대화 및 작업 기록    |

현재 LangGraph에서는 대화 단위의 단기 메모리를 `State`와 `checkpointer`로 관리하고, 세션을 넘어 유지해야 하는 정보는 별도의 장기 저장소인 `Store`로 관리합니다. ([Docs by LangChain][2])

---

# A1. Math Problem Solving

## 수학 문제 해결과 전문가 호출 구조

### 구성요소

```text
학생 Student
    ↕
학생용 Assistant
    ↕ 필요할 때 전문가 호출
Expert
    ↕
전문가용 Assistant
```

학생은 먼저 일반 Assistant에게 수학 문제를 질문합니다. Assistant가 직접 해결할 수 있으면 답변하고, 어려운 문제이거나 검증이 필요하면 내부적으로 `Ask expert` 기능을 호출합니다.

전문가와 전문가용 Assistant가 별도의 대화를 진행한 후, 최종 결과만 학생용 Assistant에게 전달합니다. 학생용 Assistant는 전문가의 결과를 기존 학생과의 대화에 합쳐 최종 답변을 만듭니다. ([ar5iv][3])

### 예시 흐름

```text
학생:
방정식 x² - 5x + 6 = 0을 풀어줘.

학생 Assistant:
해를 구했지만 검증이 필요하다.
→ Expert에게 질문

Expert Assistant:
인수분해하면 (x-2)(x-3)=0이다.
따라서 x=2, x=3이다.

학생 Assistant:
전문가 검증 결과를 반영하여 학생에게 설명
```

### 이 구조에서 메모리의 역할

**주 대화 메모리**

```text
학생 질문
→ Assistant의 풀이
→ 이전 설명 내용
```

학생용 Assistant가 유지하는 기본 대화 기록입니다.

**전문가 전용 메모리**

```text
전문가에게 전달된 문제
→ 전문가의 풀이 과정
→ 검증 결과
```

학생과 전문가의 대화는 분리될 수 있습니다. 이렇게 하면 전문가에게 불필요한 학생 대화 전체를 전달하지 않아도 됩니다.

**결과 전달 메모리**

전문가의 전체 대화가 아니라 필요한 결론만 주 대화로 돌려보냅니다.

### LangChain·LangGraph로 표현하면

```text
상위 그래프: 학생 Assistant
      ↓
하위 그래프: 수학 전문가 Agent
      ↓
전문가의 최종 결과만 상위 그래프로 반환
```

LangGraph의 Subgraph를 사용하면 상위 에이전트와 전문가 에이전트가 서로 다른 상태 구조와 개별 메시지 기록을 가질 수 있습니다. 이는 에이전트별 대화 기록을 분리할 때 유용합니다. ([Docs by LangChain][4])

### 응용 분야

* 과목별 AI 튜터
* 일반 상담사와 전문 상담사의 협업
* 의료 상담의 전문과 연결
* 법률·세무 전문가 호출
* 일반 코딩 Assistant와 언어별 전문가 연결

### 핵심

> 일반 에이전트가 모든 것을 처리하지 않고, 어려운 문제만 전문가 에이전트에 위임하는 구조입니다.

---

# A2. Retrieval-Augmented Chat

## 검색 증강 대화 구조

### 구성요소

```text
Retrieval-augmented User Proxy
- 문서 관리
- 문서 검색
- 벡터 데이터베이스
- 필요하면 코드 실행

             ↕

Retrieval-augmented Assistant
- 검색 결과 분석
- 답변 생성
- 추가 검색 요청
```

왼쪽의 User Proxy는 단순 사용자가 아니라 **검색과 문서 관리를 담당하는 에이전트**입니다. 문서를 분할하고 임베딩한 뒤 벡터 데이터베이스에 저장합니다.

질문이 들어오면 관련 문서 조각을 검색하여 질문과 함께 Assistant에게 전달합니다. Assistant는 검색 결과가 충분하면 답변하고, 정보가 부족하면 새로운 문서를 요청합니다. 원 논문에서는 Assistant가 `UPDATE CONTEXT`라는 신호를 보내면 User Proxy가 다음 검색 결과를 가져오는 방식으로 반복 검색합니다. ([ar5iv][3])

### 처리 흐름

```text
사용자 질문
   ↓
벡터 DB 검색
   ↓
관련 문서 전달
   ↓
Assistant 답변 시도
   ↓
정보가 충분한가?
   ├─ 예 → 최종 답변
   └─ 아니요 → 새로운 문서 검색
```

### 예시

질문:

```text
충청남도에서 첫만남이용권을 어떻게 신청하나요?
```

첫 번째 검색 결과:

```text
첫만남이용권의 지원 금액만 검색됨
```

Assistant:

```text
신청 장소에 대한 정보가 부족합니다.
추가 문서가 필요합니다.
```

두 번째 검색 결과:

```text
읍·면·동 주민센터 또는 복지로에서 신청 가능
```

최종 답변:

```text
주소지 관할 주민센터를 방문하거나 복지로에서 온라인으로
신청할 수 있습니다.
```

### 이 구조에서 메모리의 역할

**외부 지식 메모리**

벡터 데이터베이스에 저장된 PDF, 매뉴얼, 사내 문서입니다.

```text
PDF → 청크 분할 → 임베딩 → 벡터 DB
```

이는 대화 메모리라기보다 **검색 가능한 장기 지식 저장소**에 가깝습니다.

**대화 메모리**

```text
사용자 질문
→ 첫 번째 검색 결과
→ Assistant의 판단
→ 두 번째 검색 결과
→ 최종 답변
```

**검색 상태 메모리**

이미 사용한 문서 청크와 다음에 검색할 문서 범위를 관리해야 합니다.

### LangChain으로 표현하면

```text
Retriever Tool
      ↓
Agent
      ↓
검색 결과가 부족하면 Retriever 재호출
```

현재 LangChain의 Agentic RAG는 에이전트가 답변 과정에서 검색 도구를 언제 사용할지 판단하는 구조입니다. ([Docs by LangChain][5])

### 응용 분야

* PDF 기반 질의응답
* 사내 규정 챗봇
* 제품 매뉴얼 상담
* 최신 API 기반 코드 생성
* 정책·법률·교육 자료 검색
* PERSO AI의 사용자 문서 기반 답변

### 핵심

> LLM의 기억에만 의존하지 않고 외부 문서를 검색하여 필요한 지식을 공급하는 구조입니다.

---

# A3. Decision Making

## 환경과 상호작용하는 의사결정 구조

### 구성요소

```text
Assistant
- 계획 수립
- 다음 행동 결정

ALFWorld Executor
- 실제 행동 실행
- 환경 상태 변경
- 실행 결과 반환

Grounding Agent
- 상식과 규칙 제공
- 잘못된 행동 교정
```

ALFWorld는 자연어로 표현된 가상의 가정환경입니다. 예를 들어 다음과 같은 과제를 수행합니다.

```text
사과를 찾아서 데운 다음 냉장고에 넣어라.
```

Assistant는 다음 행동을 결정하고, Executor가 실제 환경에서 행동을 실행합니다. Grounding Agent는 가정환경의 상식이나 규칙을 제공합니다. ([ar5iv][3])

### 처리 흐름

```text
목표 입력
   ↓
Assistant가 행동 결정
   ↓
Executor가 행동 수행
   ↓
환경의 결과 반환
   ↓
Assistant가 다음 행동 결정
```

예:

```text
목표: 뜨거운 사과를 냉장고에 넣기

1. 주방으로 이동
2. 사과 찾기
3. 사과 집기
4. 전자레인지 찾기
5. 사과 데우기
6. 냉장고 열기
7. 사과 넣기
```

### Grounding Agent가 필요한 이유

Assistant가 다음과 같이 같은 행동을 반복할 수 있습니다.

```text
사과를 찾는다.
사과를 찾는다.
사과를 찾는다.
```

Grounding Agent는 다음과 같은 상식을 전달합니다.

```text
물건을 찾은 것과 물건을 집은 것은 다른 행동입니다.
사과를 찾았다면 다음에는 사과를 집어야 합니다.
```

원 연구에서는 Assistant가 같은 행동을 반복할 경우 Grounding Agent가 개입하여 잘못된 반복 루프를 벗어나도록 구성했습니다. ([ar5iv][3])

### 이 구조에서 메모리의 역할

**행동 기록 메모리**

```text
지금까지 이동한 장소
수행한 행동
행동 성공 여부
실패한 행동
```

**환경 상태 메모리**

```text
현재 위치: 주방
보유 물건: 사과
전자레인지 상태: 닫힘
사과 상태: 차가움
```

이 환경 상태는 LLM이 임의로 기억하는 것이 아니라 Executor가 관리하는 실제 상태입니다.

**Grounding 메모리**

```text
물건을 사용하려면 먼저 집어야 한다.
닫힌 용기는 먼저 열어야 한다.
뜨거운 물건을 만들려면 가열 장치를 사용해야 한다.
```

### LangGraph로 표현하면

```text
Assistant 노드
     ↓
Executor 노드
     ↓
결과 검사
 ┌───┴────┐
정상     반복·오류
 ↓          ↓
다음 행동  Grounding Agent
```

LangGraph의 `State`는 여러 노드가 함께 사용하는 작업 노트와 같은 역할을 합니다. 위치, 도구 실행 결과, 과거 행동 등을 상태에 저장하면 다음 노드가 이를 참고할 수 있습니다. ([Docs by LangChain][6])

### 응용 분야

* 로봇 행동 계획
* 게임 AI
* 업무 자동화 Agent
* 웹 브라우저 조작
* 스마트홈 제어
* 드론 임무 수행
* 단계별 문제 해결 시스템

### 핵심

> 메모리는 단순 대화가 아니라 지금까지 무엇을 했고 환경이 어떻게 변했는지를 저장하는 작업 상태입니다.

---

# A4. Multi-Agent Coding

## 코드 작성·검사·실행을 분리한 구조

### 구성요소

```text
Commander
- 사용자와 대화
- 전체 작업 조정
- 코드 실행
- 결과 통합

Writer
- 코드 작성
- 오류 수정
- 실행 결과 해석

Safeguard
- 코드 안전성 검사
- 민감정보 노출 검사
- 위험한 코드 차단
```

사용자 질문은 Commander에게 전달됩니다. Commander는 Writer에게 코드를 작성하게 하고, 작성된 코드는 실행 전에 Safeguard의 검사를 받습니다.

안전하다고 판단되면 Commander가 코드를 실행하고, 실행 결과는 다시 Writer에게 보내 해석하게 합니다. 오류나 보안 문제가 발견되면 Writer가 코드를 수정하며 이 과정이 반복됩니다. ([ar5iv][3])

### 처리 흐름

```text
사용자 질문
   ↓
Commander
   ↓
Writer가 코드 작성
   ↓
Safeguard가 안전성 검사
   ├─ 위험 → Writer에게 수정 요청
   └─ 안전 → Commander가 코드 실행
                  ↓
            실행 결과 해석
                  ↓
              사용자 답변
```

### 예시

사용자:

```text
CSV 파일을 분석해서 월별 매출을 계산해줘.
```

Writer:

```python
import pandas as pd

df = pd.read_csv("sales.csv")
result = df.groupby("month")["sales"].sum()
print(result)
```

Safeguard:

```text
파일 삭제, 외부 전송, 시스템 명령이 없으므로 실행 가능
```

Commander:

```text
코드 실행 → 결과 확보
```

Writer:

```text
3월 매출이 가장 높고 1월 매출이 가장 낮습니다.
```

### 이 구조에서 메모리의 역할

**Commander의 사용자 메모리**

Commander는 사용자의 원래 요청, 이전 질문, 실행 결과를 유지합니다. 원 논문에서도 Commander가 사용자 상호작용에 관한 메모리를 관리한다고 설명합니다. ([ar5iv][3])

**Writer의 작업 메모리**

```text
이전에 작성한 코드
오류 메시지
수정 사항
실행 로그
```

**Safeguard의 독립 메모리**

```text
보안 규칙
검사 결과
위험 코드 패턴
```

Writer가 Safeguard의 판단을 미리 알고 검사에 맞춰 편법을 사용하지 않도록, 역할별 메모리를 일정 부분 분리할 수 있습니다. 원 연구는 역할 분리를 통해 에이전트별 메모리를 격리하는 효과를 설명합니다. ([ar5iv][3])

### LangChain·LangGraph로 표현하면

```text
Supervisor Agent
   ├─ Coder Subagent
   ├─ Safety Checker
   └─ Python Tool
```

실제 파일 변경, SQL 실행, 외부 전송과 같이 위험할 수 있는 작업에는 Human-in-the-Loop를 추가하여 사람이 승인한 후 실행하도록 만들 수 있습니다. ([Docs by LangChain][7])

### 응용 분야

* 코드 자동 생성
* 데이터 분석 자동화
* SQL 생성과 검증
* 최적화 프로그램 작성
* 보안 코드 리뷰
* 자동 디버깅
* 업무 자동화 스크립트 생성

### 핵심

> 코드를 만드는 역할, 검사하는 역할, 실행하는 역할을 분리하여 오류와 보안 위험을 줄이는 구조입니다.

---

# A5. Dynamic Group Chat

## 동적으로 발언자를 선택하는 그룹 협업 구조

### 구성요소

```text
             Manager
                ↓
       다음 발언자 선택
                ↓
Engineer / Critic / Executor / User Proxy
                ↓
       모든 참여자에게 방송
```

Manager는 회의 진행자와 같은 역할을 합니다.

1. 현재 대화 내용을 분석합니다.
2. 다음에 발언할 에이전트를 선택합니다.
3. 선택된 에이전트에게 답변을 요청합니다.
4. 답변을 그룹 전체에 전달합니다.
5. 다음 발언자를 다시 선택합니다.

이 과정은 미리 정해진 고정 순서가 아니라 현재 문제와 대화 내용에 따라 동적으로 달라집니다. ([ar5iv][3])

### 예시

과제:

```text
주식 데이터를 가져와 수익률을 계산하고 결과를 파일로 저장하라.
```

가능한 대화:

```text
Manager → Engineer:
데이터 수집 코드를 작성하세요.

Engineer → 전체:
주가 조회 코드를 작성했습니다.

Manager → Executor:
코드를 실행하세요.

Executor → 전체:
날짜 형식 오류가 발생했습니다.

Manager → Engineer:
날짜 오류를 수정하세요.

Engineer → 전체:
코드를 수정했습니다.

Manager → Critic:
결과가 정확한지 검토하세요.

Critic → 전체:
수익률 계산식이 올바릅니다.
```

### 이 구조에서 메모리의 역할

**그룹 공유 메모리**

모든 에이전트가 공통 대화 기록을 읽습니다.

```text
현재까지의 대화
작성된 코드
실행 결과
검토 의견
남은 작업
```

**Manager의 진행 상태 메모리**

```text
직전에 누가 발언했는가?
현재 어떤 문제가 남았는가?
누가 다음 작업에 가장 적합한가?
작업이 종료되었는가?
```

**에이전트별 전문 메모리**

Engineer는 코드 중심, Critic은 검사 기준 중심, Executor는 실행 로그 중심으로 필요한 맥락이 다릅니다.

### 공유 메모리의 문제점

모든 대화를 모든 에이전트에게 계속 전달하면 다음 문제가 생길 수 있습니다.

```text
대화 길이 증가
→ 토큰 사용량 증가
→ 비용 증가
→ 중요한 정보가 묻힘
→ 응답 일관성 저하
```

현재 LangChain의 멀티에이전트 구조도 주요 목적 중 하나를 **필요한 에이전트에 필요한 컨텍스트만 제공하는 Context Management**로 설명합니다. ([Docs by LangChain][8])

### LangChain의 Supervisor와 연결

LangChain의 Supervisor Agent는 전체 대화 맥락을 유지하면서 여러 하위 에이전트 중 누구를 호출할지 동적으로 결정합니다. 단순 Router가 한 번 분류하고 끝나는 것과 달리, Supervisor는 여러 대화 단계에 걸쳐 계속 하위 에이전트를 호출할 수 있습니다. ([Docs by LangChain][9])

### 응용 분야

* 소프트웨어 개발팀 Agent
* 회의형 문제 해결
* 기획·개발·검수 협업
* 연구 논문 분석팀
* 콘텐츠 제작팀
* 복합 업무 자동화
* 역할 기반 프로젝트 수행

### 핵심

> Manager가 현재 상황을 보고 가장 적합한 전문가에게 차례로 발언권을 주는 AI 회의 구조입니다.

---

# A6. Conversational Chess

## 대화형 체스와 권위 있는 상태 관리

### 구성요소

```text
Player A
   ↘
   Chess Board Agent
   ↗
Player B
```

Player A와 Player B는 사람, AI 또는 사람과 AI의 혼합 형태가 될 수 있습니다.

Chess Board Agent는 다음을 담당합니다.

```text
현재 체스판 상태 관리
말의 위치 관리
차례 관리
합법적인 수인지 확인
승패 판단
```

플레이어가 자연어로 수를 말하면 Board Agent가 이를 체스 명령으로 변환하고 유효성을 검사합니다. 불가능한 수이면 오류를 반환하고, 플레이어가 다시 수를 제안하도록 합니다. ([ar5iv][3])

### 예시

Player A:

```text
왕 앞의 폰을 두 칸 전진할게.
```

Board Agent:

```text
e2 → e4로 해석했습니다.
합법적인 수입니다.
```

Player B:

```text
나이트를 e5로 이동할게.
```

Board Agent:

```text
현재 위치에서는 해당 이동이 불가능합니다.
다른 수를 선택하세요.
```

### 이 구조에서 메모리의 역할

**체스판 상태 메모리**

```text
각 말의 현재 위치
누구의 차례인가?
캐슬링 가능 여부
앙파상 가능 여부
체크 상태
```

이 정보는 가장 신뢰도가 높은 **권위 있는 상태, 즉 Source of Truth**입니다.

**수의 기록**

```text
1. e4 e5
2. Nf3 Nc6
3. Bb5
```

**플레이어별 비공개 대화**

Player A와 Board Agent의 오류 수정 대화가 Player B에게 모두 공개될 필요는 없습니다. 원 연구에서도 플레이어와 Board Agent 사이의 일부 대화를 상대방에게 보이지 않게 분리하여 컨텍스트를 관리합니다. ([ar5iv][3])

**공개 대화 메모리**

합법적으로 확정된 수와 플레이어 간 메시지만 상대방에게 전달합니다.

### 중요한 설계 원칙

체스판 상태를 LLM의 대화 기억에만 맡기면 안 됩니다.

```text
잘못된 구조:
LLM이 체스판을 기억하고 스스로 합법 여부 판단

권장 구조:
Board Agent의 프로그램 상태가 체스판 관리
LLM은 전략과 자연어 대화 담당
```

즉, 정확한 규칙과 상태는 일반 프로그램이 관리하고, LLM은 설명·전략·대화에 집중합니다.

### LangGraph로 표현하면

```text
Player A Agent
      ↓
Board Validation Node
      ↓
상태 업데이트
      ↓
Player B Agent
```

각 차례가 끝날 때마다 체스판 상태를 `State`에 저장하며, checkpointer를 사용하면 실행이 중단되더라도 같은 게임을 이어갈 수 있습니다. LangGraph의 persistence는 중단 복구와 대화 연속성을 위해 그래프 상태를 저장합니다. ([Docs by LangChain][10])

### 응용 분야

* 보드게임 AI
* 턴제 게임
* 교육용 시뮬레이션
* 협상 시뮬레이션
* 규칙 기반 업무 처리
* 예약·승인 프로세스
* 상태 변화가 중요한 Agent 시스템

### 핵심

> LLM은 플레이어 역할을 맡고, Board Agent는 정확한 규칙과 상태를 관리하는 구조입니다.

---

# 여섯 그림의 메모리 구조 비교

| 그림           | 주요 메모리                   | 공유 방식                               | 핵심 목적            |
| ------------ | ------------------------ | ----------------------------------- | ---------------- |
| A1 수학 문제 해결  | 학생 대화, 전문가 대화            | 전문가 결과만 주 Agent로 전달                 | 전문가 위임           |
| A2 검색 증강 대화  | 벡터 DB, 검색 결과, 대화 기록      | 검색 Agent와 답변 Agent가 문맥 교환           | 외부 지식 활용         |
| A3 의사결정      | 행동 기록, 환경 상태, 상식         | Assistant·Executor·Grounding이 상태 교환 | 반복 행동과 잘못된 계획 방지 |
| A4 멀티에이전트 코딩 | 사용자 요구, 코드, 오류 로그, 보안 검사 | Commander가 필요한 정보 전달                | 작성·검사·실행 분리      |
| A5 동적 그룹 채팅  | 전체 그룹 대화와 작업 상태          | Manager가 메시지를 전체에 방송                | 전문가 협업과 동적 작업 배분 |
| A6 대화형 체스    | 체스판, 수의 기록, 차례           | 공개 상태와 비공개 대화 분리                    | 정확한 규칙과 상태 유지    |

---

# LangChain·LangGraph 관점의 통합 구조

```text
                    사용자
                       ↓
             Supervisor / Manager
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
   전문 Agent      RAG Agent      실행 Agent
        ↓              ↓              ↓
  개별 대화 상태    Vector DB      Tool / Environment
        └──────────────┼──────────────┘
                       ↓
                 Shared State
                       ↓
                  Checkpointer
```

여기에서 각 요소는 다음과 대응됩니다.

| 그림의 개념                    | LangChain·LangGraph 구성요소   |
| ------------------------- | -------------------------- |
| Assistant, Writer, Expert | Agent 또는 Subagent          |
| Commander, Manager        | Supervisor Agent           |
| Ask Expert                | Tool 호출 또는 Subgraph 호출     |
| Retrieval User Proxy      | Retriever Tool             |
| Vector Database           | Chroma, FAISS, Qdrant 등    |
| Executor                  | Python·SQL·API Tool        |
| Board·환경 상태               | LangGraph State            |
| 대화 기록                     | Messages State             |
| 실행 중단 후 복원                | Checkpointer               |
| 사용자별 장기 정보                | Store                      |
| 에이전트별 비공개 대화              | 개별 Subgraph State          |
| 그룹 전체 대화                  | Parent Graph의 Shared State |

## 한 문장으로 정리

> 이 그림은 메모리를 단순히 “이전 대화를 기억하는 기능”으로 보지 않고, 여러 에이전트가 **대화 기록, 외부 지식, 실행 결과, 환경 상태를 선택적으로 공유하거나 분리하여 복잡한 작업을 해결하는 구조**로 보여줍니다.

[1]: https://ar5iv.labs.arxiv.org/html/2308.08155?utm_source=chatgpt.com "AutoGen: Enabling Next-Gen LLM Applications via Multi ..."
[2]: https://docs.langchain.com/oss/python/langgraph/add-memory?utm_source=chatgpt.com "Memory - Docs by LangChain"
[3]: https://ar5iv.labs.arxiv.org/html/2308.08155 "[2308.08155] AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
[4]: https://docs.langchain.com/oss/python/langgraph/use-subgraphs?utm_source=chatgpt.com "Subgraphs - Docs by LangChain"
[5]: https://docs.langchain.com/oss/python/langchain/retrieval?utm_source=chatgpt.com "Retrieval - Docs by LangChain"
[6]: https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph?utm_source=chatgpt.com "Thinking in LangGraph - Docs by LangChain"
[7]: https://docs.langchain.com/oss/python/langchain/human-in-the-loop?utm_source=chatgpt.com "Human-in-the-loop - Docs by LangChain"
[8]: https://docs.langchain.com/oss/python/langchain/multi-agent?utm_source=chatgpt.com "Multi-agent - Docs by LangChain"
[9]: https://docs.langchain.com/oss/python/langchain/multi-agent/subagents?utm_source=chatgpt.com "Subagents - Docs by LangChain"
[10]: https://docs.langchain.com/oss/python/langgraph/persistence?utm_source=chatgpt.com "Persistence - Docs by LangChain"
