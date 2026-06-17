```python
# [1단계] 필요한 라이브러리 설치 (코랩에서는 주석을 해제하고 행)
# !pip install transformers torch accelerate

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

print("🚀 모델 로딩 중... (약 1~2분 소요)")

# [2단계] 모델 및 토크나이저 로드
# Qwen2.5-1.5B-Instruct: 15억 파라미터, 한국어 우수, 경량화
model_name = "Qwen/Qwen2.5-1.5B-Instruct"

# 메모리 절약을 위해 16비트 부동소수점 사용 (GPU 환경 권장, CPU면 float32로 자동 조정됨)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"  # 사용 가능한 GPU/CPU 자동 할당
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 파이프라인 생성 (텍스트 생성 전용)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

print("✅ 모델 로딩 완료! 이제 4가지 기능을 테스트합니다.\n")
print("="*50)

# [공통 함수] Qwen의 채팅 템플릿을 적용하여 프롬프트를 만드는 함수
def get_response(user_prompt, system_prompt="당신은 유용한 한국어 AI 어시스턴트입니다."):
    # 모델이 이해하기 쉬운 채팅 형식(System, User)으로 변환
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Qwen 모델에 맞는 텍스트 포맷팅
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 모델 추론 (생성)
    outputs = pipe(text, max_new_tokens=256, do_sample=True, temperature=0.7, top_p=0.9)
    
    # 생성된 결과만 추출
    generated_text = outputs[0]["generated_text"][len(text):]
    return generated_text.strip()

# ==========================================
# [기능 1] 자연어 생성 (콘텐츠 작성)
# ==========================================
print("\n✨ [1] 자연어 생성: 마케팅 카피 작성")
gen_prompt = "내일 오픈하는 '별빛 카페'라는 이름의 감성적인 루프탑 카페 인스타그램 게시글을 작성해줘. 이모지를 적절히 사용하고 해시태그 3개를 포함해줘."
print(f" 요청: {gen_prompt}")
print(f"🤖 AI 답변: {get_response(gen_prompt)}")

# ==========================================
# [기능 2] 문장 번역 (한국어 <-> 영어)
# ==========================================
print("\n [2] 문장 번역: 영한 번역")
trans_prompt = "다음 영어 문장을 자연스러운 한국어로 번역해줘:\n'Artificial intelligence is transforming the way we work and live, but we must also consider its ethical implications.'"
print(f"👤 요청: {trans_prompt}")
print(f"🤖 AI 답변: {get_response(trans_prompt)}")

# ==========================================
# [기능 3] 문서 요약 (핵심 추출)
# ==========================================
print("\n📝 [3] 문서 요약: 긴 글 핵심 요약")
long_text = """
인공지능(AI)은 인간의 지능을 모방하여 컴퓨터가 학습, 추론, 문제 해결 등을 수행할 수 있도록 하는 기술입니다. 
최근에는 딥러닝과 대규모 언어 모델(LLM)의 발전으로 ChatGPT와 같은 생성형 AI가 등장했으며, 
이는 텍스트 생성, 이미지 생성, 코드 작성 등 다양한 분야에서 혁신을 일으키고 있습니다. 
하지만 AI의 발전과 함께 데이터 프라이버시, 저작권, 편향성 등 해결해야 할 윤리적 문제들도 대두되고 있습니다.
"""
sum_prompt = f"다음 글을 3줄의 불릿 포인트로 핵심만 요약해줘:\n{long_text}"
print(f"👤 요청: {sum_prompt}")
print(f" AI 답변: {get_response(sum_prompt)}")

# ==========================================
# [기능 4] 대화 (챗봇 및 페르소나 부여)
# ==========================================
print("\n [4] 대화: 페르소나 부여 챗봇")
chat_prompt = "안녕! 나는 오늘 회사에서 프로젝트를 성공적으로 마쳤는데, 너무 기분이 좋아. 뭐 좋은 저녁 메뉴 추천해줄 수 있어?"
# system_prompt를 바꿔서 AI의 말투를 '까칠한 서울 아저씨'로 설정
print(f"👤 요청: {chat_prompt}")
print(f"🤖 AI 답변 (서울 아저씨): {get_response(chat_prompt, system_prompt='당신은 말은 좀 까칠하지만 속은 따뜻한 서울 아저씨입니다. 반말을 섞어서 답변하세요.')}")

print("\n" + "="*50)
print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
```
