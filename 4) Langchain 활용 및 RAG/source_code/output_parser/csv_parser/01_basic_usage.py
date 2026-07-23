"""
1-5-1. CSV Parser - 기본 사용법
파서 생성, 포맷 지시사항 확인, 직접 파싱 (LLM 호출 없이 동작)
"""
from langchain_core.output_parsers import CommaSeparatedListOutputParser


def main():
    # 파서 인스턴스 생성
    output_parser = CommaSeparatedListOutputParser()

    # 포맷 지시사항 확인 (LLM에게 전달할 출력 형식 안내문)
    format_instructions = output_parser.get_format_instructions()
    print("=== 포맷 지시사항 ===")
    print(format_instructions)
    # 출력 예: Your response should be a list of comma separated values, eg: `foo, bar, baz`

    # 쉼표로 구분된 텍스트 직접 파싱
    text = "Python, JavaScript, Java, C++, Go"
    result = output_parser.parse(text)

    print("\n=== 직접 파싱 결과 ===")
    print(result)          # ['Python', 'JavaScript', 'Java', 'C++', 'Go']
    print(type(result))    # <class 'list'>


if __name__ == "__main__":
    main()
