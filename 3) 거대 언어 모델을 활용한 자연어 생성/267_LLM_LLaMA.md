```python
# 2. 모델 로드

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)


# 3. LLaMA 계열 텍스트 생성 함수

def generate_llama(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant. Answer in Korean."},
        {"role": "user", "content": prompt}
    ]

    input_text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        repetition_penalty=1.1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id
    )

    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result
# 4. 실행 예제

prompt = "LLaMA 모델의 특징을 초보자도 이해할 수 있게 설명해줘."

answer = generate_llama(prompt)

print(answer)
# 5. 여러 입력 비교

prompts = [
    "LLaMA와 GPT의 공통점과 차이점을 설명해줘.",
    "Transformer 디코더 기반 모델이란 무엇인가?",
    "작은 LLaMA 모델이 연구용으로 유용한 이유는?"
]

for p in prompts:
    print("\n질문:", p)
    print("답변:")
    print(generate_llama(p))
    print("-" * 80)
```
