"""
다중 모델 앙상블 예제

사용 모델
1. OpenAI GPT-5 mini
2. Anthropic Claude Sonnet 5

처리 과정
1. 두 모델을 병렬로 호출
2. 각각의 응답을 출력
3. OpenAI 모델이 두 응답을 비교·분석
4. 최종 종합 답변 생성
"""

import os
import sys
from typing import Any, Dict

# Windows 콘솔 UTF-8 출력 설정
if os.name == "nt":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel


def setup_environment() -> None:
    """
    .env 파일을 불러오고 API 키를 확인합니다.
    """

    load_dotenv()

    required_keys = [
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
    ]

    missing_keys = [
        key for key in required_keys
        if not os.getenv(key)
    ]

    if missing_keys:
        raise ValueError(
            "다음 환경 변수가 설정되지 않았습니다: "
            + ", ".join(missing_keys)
            + "\n.env 파일에 API 키를 등록하세요."
        )


def create_models() -> Dict[str, BaseChatModel]:
    """
    OpenAI 모델과 Anthropic Claude 모델을 초기화합니다.

    Returns:
        모델 이름과 모델 객체가 저장된 딕셔너리
    """

    openai_model_name = os.getenv(
        "OPENAI_MODEL",
        "gpt-5-mini",
    )

    anthropic_model_name = os.getenv(
        "ANTHROPIC_MODEL",
        "claude-sonnet-5",
    )

    models: Dict[str, BaseChatModel] = {
        "OpenAI": ChatOpenAI(
            model=openai_model_name,
            timeout=60,
            max_retries=2,
        ),

        "Claude": ChatAnthropic(
            model=anthropic_model_name,
            max_tokens=2048,
            timeout=60,
            max_retries=2,
        ),
    }

    return models


def create_ensemble_chain(
    models: Dict[str, BaseChatModel],
) -> RunnableParallel:
    """
    두 모델을 병렬로 실행하는 앙상블 체인을 생성합니다.

    Args:
        models:
            모델 이름과 모델 객체가 저장된 딕셔너리

    Returns:
        RunnableParallel 체인
    """

    answer_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
당신은 전문적인 AI 조언자입니다.

다음 원칙에 따라 답변하세요.

1. 질문의 핵심을 정확히 파악하세요.
2. 사실과 의견을 구분하세요.
3. 근거가 부족한 내용은 단정하지 마세요.
4. 이해하기 쉬운 한국어로 답변하세요.
5. 필요한 경우 예시를 포함하세요.
                """.strip(),
            ),
            (
                "human",
                "{question}",
            ),
        ]
    )

    model_chains = {}

    for model_name, model in models.items():
        model_chains[model_name] = (
            answer_prompt
            | model
            | StrOutputParser()
        )

    return RunnableParallel(**model_chains)


def create_synthesis_chain(
    synthesis_model: BaseChatModel,
) -> Any:
    """
    OpenAI와 Claude의 응답을 비교하고
    최종 답변을 생성하는 체인을 만듭니다.

    Args:
        synthesis_model:
            최종 답변을 생성할 모델

    Returns:
        응답 종합 체인
    """

    synthesis_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
당신은 여러 AI 모델의 답변을 평가하는 수석 검토자입니다.

두 모델의 응답을 다음 기준으로 분석하세요.

1. 정확성
2. 질문과의 관련성
3. 논리적 완성도
4. 설명의 명확성
5. 실용성
6. 누락된 내용
7. 서로 충돌하는 내용

두 응답을 단순히 연결하지 마세요.

잘못되었거나 근거가 부족한 내용은 제외하고,
각 응답의 장점을 결합하여 하나의 완성된 답변을 작성하세요.

두 응답이 서로 충돌한다면 더 논리적이고 신뢰할 수 있는
내용을 선택하고, 필요한 경우 불확실성을 명시하세요.

최종 결과는 자연스러운 한국어로 작성하세요.
                """.strip(),
            ),
            (
                "human",
                """
[사용자 질문]

{question}


[OpenAI 응답]

{openai_response}


[Claude 응답]

{claude_response}


위 두 응답을 비교·분석하여 최종 종합 답변을 작성하세요.
                """.strip(),
            ),
        ]
    )

    return (
        synthesis_prompt
        | synthesis_model
        | StrOutputParser()
    )


def run_ensemble(
    question: str,
    ensemble_chain: RunnableParallel,
    synthesis_chain: Any,
) -> Dict[str, Any]:
    """
    두 모델의 응답을 병렬로 생성한 후
    최종 종합 답변을 생성합니다.

    Args:
        question:
            사용자 질문

        ensemble_chain:
            두 모델을 병렬 호출하는 체인

        synthesis_chain:
            응답을 비교·종합하는 체인

    Returns:
        개별 응답과 최종 답변
    """

    # 1단계: OpenAI와 Claude 병렬 호출
    individual_responses = ensemble_chain.invoke(
        {
            "question": question,
        }
    )

    openai_response = individual_responses.get(
        "OpenAI",
        "OpenAI 응답이 없습니다.",
    )

    claude_response = individual_responses.get(
        "Claude",
        "Claude 응답이 없습니다.",
    )

    # 2단계: 두 응답 비교 및 종합
    final_answer = synthesis_chain.invoke(
        {
            "question": question,
            "openai_response": openai_response,
            "claude_response": claude_response,
        }
    )

    return {
        "question": question,
        "individual_responses": individual_responses,
        "final_answer": final_answer,
    }


def print_result(result: Dict[str, Any]) -> None:
    """
    앙상블 실행 결과를 콘솔에 출력합니다.
    """

    question = result["question"]
    responses = result["individual_responses"]
    final_answer = result["final_answer"]

    print("\n" + "=" * 80)
    print("[사용자 질문]")
    print("=" * 80)
    print(question)

    print("\n" + "-" * 80)
    print("[OpenAI 응답]")
    print("-" * 80)
    print(responses.get("OpenAI", "응답 없음"))

    print("\n" + "-" * 80)
    print("[Claude 응답]")
    print("-" * 80)
    print(responses.get("Claude", "응답 없음"))

    print("\n" + "=" * 80)
    print("[최종 종합 답변]")
    print("=" * 80)
    print(final_answer)

    print("\n" + "=" * 80)


def main() -> None:
    """
    프로그램 메인 함수
    """

    try:
        # 1. 환경 변수 확인
        setup_environment()
        print("[OK] API 키 확인 완료")

        # 2. 모델 생성
        models = create_models()

        print("[OK] 모델 초기화 완료")

        openai_model_name = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini",
        )

        anthropic_model_name = os.getenv(
            "ANTHROPIC_MODEL",
            "claude-sonnet-5",
        )

        print(f"     OpenAI : {openai_model_name}")
        print(f"     Claude : {anthropic_model_name}")

        # 3. 두 모델 병렬 호출 체인
        ensemble_chain = create_ensemble_chain(models)
        print("[OK] 병렬 앙상블 체인 생성 완료")

        # 4. OpenAI 모델을 최종 종합 모델로 사용
        synthesis_model = models["OpenAI"]

        synthesis_chain = create_synthesis_chain(
            synthesis_model
        )

        print("[OK] 종합 체인 생성 완료")

        # 테스트 질문
        test_cases = [
            "효과적인 학습 방법 3가지를 알려주세요.",
            "소프트웨어 개발자에게 가장 중요한 역량은 무엇인가요?",
            "생성형 AI가 교육에 미치는 장점과 위험을 설명해주세요.",
        ]

        # 각 질문 실행
        for index, question in enumerate(test_cases, start=1):
            print(f"\n[테스트 {index}]")
            print("OpenAI와 Claude가 병렬로 응답을 생성합니다.")

            try:
                result = run_ensemble(
                    question=question,
                    ensemble_chain=ensemble_chain,
                    synthesis_chain=synthesis_chain,
                )

                print_result(result)

            except Exception as error:
                print(
                    f"[ERROR] 테스트 {index} 실행 실패: "
                    f"{error}"
                )

        print("\n[OK] 모든 테스트가 완료되었습니다.")

    except ValueError as error:
        print(f"[설정 오류] {error}")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INFO] 사용자가 프로그램을 중단했습니다.")
        sys.exit(0)

    except Exception as error:
        print(f"[예상하지 못한 오류] {error}")

        import traceback
        traceback.print_exc()

        sys.exit(1)


if __name__ == "__main__":
    main()