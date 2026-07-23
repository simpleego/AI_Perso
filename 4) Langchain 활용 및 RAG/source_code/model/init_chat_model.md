```py
"""
LangChain 통합 예제 모음
- init_chat_model
- 직접 파라미터 전달
- bind 메서드
- Claude (Anthropic)
- Gemini (Google)

실행 방법:
    python langchain_examples.py
    -> 실행할 예제 번호를 선택합니다.
"""

import os
import sys
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ============================================================
# 1. 통합 모델 초기화 (init_chat_model)
# ============================================================
def example_1_init_chat_model():
    print("\n=== 1. 통합 모델 초기화 (init_chat_model) ===")
    from langchain.chat_models import init_chat_model

    model = init_chat_model("gpt-4.1")
    response = model.invoke("안녕하세요, 한국의 수도는 어디인가요?")
    print(f"응답: {response.content}")


# ============================================================
# 2. 모델 생성 및 호출 시 파라미터 직접 전달
# ============================================================
def example_2_direct_params():
    print("\n=== 2. 모델에 직접 파라미터 전달 ===")
    from langchain_openai import ChatOpenAI

    params = {
        "temperature": 0.7,
        "max_tokens": 100,
    }
    kwargs = {
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5,
        "stop": ["\n"],
    }

    model = ChatOpenAI(model="gpt-4o-mini", **params, model_kwargs=kwargs)
    response = model.invoke("태양계에서 가장 큰 행성은 무엇인가요?")
    print(f"응답: {response.content}")


# ============================================================
# 3. bind 메서드로 파라미터 추가 바인딩
# ============================================================
def example_3_bind_method():
    print("\n=== 3. bind 메서드로 파라미터 추가 ===")
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_openai import ChatOpenAI

    prompt = ChatPromptTemplate.from_messages([
        ("system", "이 시스템은 천문학 질문에 답변할 수 있습니다."),
        ("user", "{user_input}"),
    ])

    model = ChatOpenAI(model="gpt-4o-mini", max_tokens=100)

    # bind로 max_tokens를 10으로 제한
    chain = prompt | model.bind(max_tokens=10)
    response = chain.invoke({"user_input": "태양계에서 가장 큰 행성은 무엇인가요?"})
    print(f"응답 (10토큰 제한): {response.content}")


# ============================================================
# 4. Claude (Anthropic)
# ============================================================
def example_4_claude():
    print("\n=== 4. Claude (Anthropic) ===")
    from langchain_anthropic import ChatAnthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️ ANTHROPIC_API_KEY가 .env에 설정되지 않았습니다.")
        return

    llm = ChatAnthropic(
        model="claude-haiku-4-5-20251001",
        temperature=0,
        max_tokens=200,
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "LLM은 어떤 원리로 작동하나요? 100자 이내로 설명해주세요."},
    ]

    response = llm.invoke(messages)
    print(f"응답: {response.content}")


# ============================================================
# 5. Gemini (Google)
# ============================================================
def example_5_gemini():
    print("\n=== 5. Gemini (Google) ===")
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️ GOOGLE_API_KEY가 .env에 설정되지 않았습니다.")
        return

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_output_tokens=200,
        google_api_key=api_key,
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "LLM은 어떤 원리로 작동하나요? 100자 이내로 설명해주세요."},
    ]

    response = llm.invoke(messages)
    print(f"응답: {response.content}")


# ============================================================
# 실행 메뉴
# ============================================================
def main():
    examples = {
        "1": ("통합 모델 초기화 (init_chat_model)", example_1_init_chat_model),
        "2": ("모델에 직접 파라미터 전달", example_2_direct_params),
        "3": ("bind 메서드로 파라미터 추가", example_3_bind_method),
        "4": ("Claude (Anthropic)", example_4_claude),
        "5": ("Gemini (Google)", example_5_gemini),
        "a": ("모든 예제 실행", None),
    }

    print("\n" + "=" * 50)
    print("LangChain 통합 예제 실행기")
    print("=" * 50)
    for key, (desc, _) in examples.items():
        if key == "a":
            print(f"  {key}: {desc}")
        else:
            print(f"  {key}: {desc}")

    choice = input("\n실행할 예제 번호를 입력하세요 (1-5, a=전체): ").strip().lower()

    if choice == "a":
        for key, (desc, func) in examples.items():
            if key != "a" and func:
                func()
    elif choice in examples:
        _, func = examples[choice]
        if func:
            func()
        else:
            print("잘못된 선택입니다.")
    else:
        print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
```    
