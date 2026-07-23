"""프롬프트 작성 체크리스트를 코드로 점검하는 간단한 보조 실습."""

prompt_text = """당신은 Python 강사입니다.
대상은 비전공 초보자입니다.
함수와 메서드의 차이를 정의, 예시, 요약 순서로 설명하세요.
전문 용어는 괄호로 풀이하고 500자 이내로 작성하세요.
"""

checks = {
    "역할이 정의되었는가": "당신은" in prompt_text,
    "대상 또는 컨텍스트가 있는가": any(
        word in prompt_text for word in ["대상", "배경", "컨텍스트"]
    ),
    "작업 지시가 구체적인가": any(
        word in prompt_text for word in ["설명", "작성", "분석", "생성"]
    ),
    "출력 형식이 지정되었는가": any(
        word in prompt_text for word in ["순서", "표", "JSON", "목록"]
    ),
    "제약 조건이 있는가": any(
        word in prompt_text for word in ["이내", "정확히", "금지", "제한"]
    ),
}

for item, passed in checks.items():
    print(f"{'✅' if passed else '❌'} {item}")
