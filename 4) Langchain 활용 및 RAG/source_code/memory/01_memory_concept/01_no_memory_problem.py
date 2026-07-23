"""
1-6-1. 메모리의 필요성과 개념 - (1) 메모리가 없는 대화의 문제점
LLM은 상태(state)를 저장하지 않으므로 각 invoke() 호출은 완전히 독립적이다.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _common import get_llm


def main():
    llm = get_llm()  # Gemini 모델 (무료 API 키)

    # 첫 번째 질문: 이름을 알려줌
    response1 = llm.invoke("안녕하세요, 제 이름은 민수입니다.")
    print("응답 1:", response1.content)

    # 두 번째 질문: 이전 호출과 "완전히 별개"의 요청이므로 이름을 기억하지 못함
    response2 = llm.invoke("제 이름이 뭐였죠?")
    print("응답 2:", response2.content)
    # → "이전 대화 내용을 알 수 없습니다"류의 답변이 나오는 것이 정상 (메모리 부재 확인)


if __name__ == "__main__":
    main()
