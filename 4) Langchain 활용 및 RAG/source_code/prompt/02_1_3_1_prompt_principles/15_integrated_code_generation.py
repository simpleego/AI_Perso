"""실전 예제: 역할, 제약, 출력 구조를 결합한 코드 생성 프롬프트."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """당신은 시니어 Python 개발자입니다.
코드 작성 규칙:
1. PEP 8 준수
2. 타입 힌트 포함
3. Google 스타일 docstring 포함
4. 적절한 예외 처리
5. 단위 테스트 코드 포함

응답 구조:
1. 구현 접근 방식 2~3문장
2. 메인 코드
3. 사용 예시
4. 단위 테스트""",
        ),
        (
            "human",
            """다음 기능을 구현해주세요.
기능: {feature}
입력: {input_spec}
출력: {output_spec}
제약사항: {constraints}""",
        ),
    ]
)

chain = prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {
            "feature": "리스트에서 중복을 제거하면서 기존 순서를 유지",
            "input_spec": "정수 리스트",
            "output_spec": "중복이 제거된 정수 리스트",
            "constraints": "원본 순서 유지, 평균 O(n) 시간복잡도",
        }
    )
)
