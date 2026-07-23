"""원칙 4: Gemini의 네이티브 JSON Schema 구조화 출력."""

import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm


class CodeReview(BaseModel):
    """코드 리뷰 결과 스키마."""

    summary: str = Field(description="코드 기능 요약")
    score: int = Field(ge=1, le=10, description="1~10점 품질 점수")
    issues: list[str] = Field(description="발견된 문제점 목록")
    suggestions: list[str] = Field(description="개선 제안 목록")


structured_llm = get_llm().with_structured_output(
    schema=CodeReview.model_json_schema(),
    method="json_schema",
)

result = structured_llm.invoke(
    """다음 Python 코드를 리뷰해주세요.

def calc(x):
    return x*2+1
"""
)

print(json.dumps(result, ensure_ascii=False, indent=2))
print(f"점수: {result['score']}/10")
