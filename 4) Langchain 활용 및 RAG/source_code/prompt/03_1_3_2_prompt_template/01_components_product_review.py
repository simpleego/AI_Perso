"""PromptTemplate 구성 요소: 지시, 예시, 맥락, 질문을 하나로 조합."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

prompt = PromptTemplate.from_template(
    """[지시]
아래 제공된 제품 리뷰를 요약해주세요.

[예시]
리뷰: 이 제품은 사용하기 편리하고 배터리 수명이 길다.
요약: 사용 편리성과 긴 배터리 수명이 특징이다.

[맥락]
리뷰 대상은 스마트워치이며 사용자 경험에 초점을 맞춥니다.

[리뷰]
{review}

[질문]
이 리뷰를 바탕으로 스마트워치의 주요 장점을 2~3문장으로 요약해주세요."""
)

chain = prompt | get_llm() | StrOutputParser()
print(
    chain.invoke(
        {
            "review": "화면이 선명하고 운동 기록이 편리합니다. 이틀 정도 충전 없이 사용할 수 있지만 앱 실행 속도는 가끔 느립니다."
        }
    )
)
