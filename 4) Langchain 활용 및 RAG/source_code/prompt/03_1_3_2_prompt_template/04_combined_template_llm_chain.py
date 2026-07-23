"""결합된 PromptTemplate을 Gemini 및 StrOutputParser와 연결."""

import sys
from pathlib import Path

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from common import get_llm

profile_prompt = PromptTemplate.from_template(
    "안녕하세요, 제 이름은 {name}이고 나이는 {age}살입니다."
)
combined_prompt = (
    profile_prompt
    + PromptTemplate.from_template("\n아버지를 아버지라 부를 수 없습니다.")
    + "\n위 문장을 {language}로 번역하고 번역문만 출력하세요."
)

chain = combined_prompt | get_llm() | StrOutputParser()
print(chain.invoke({"name": "홍길동", "age": 30, "language": "영어"}))
