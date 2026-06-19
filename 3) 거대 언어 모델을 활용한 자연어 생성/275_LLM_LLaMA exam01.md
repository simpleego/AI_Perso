```python
!pip install -U bitsandbytes

import csv

# 테스트용 학생 성적 데이터 데이터
data = [
    ["학생 이름", "국어", "영어", "수학"],
    ["김철수", 85, 90, 78],
    ["이영희", 92, 88, 95],
    ["박민수", 70, 65, 80],
    ["최지우", 88, 72, 90]
]

# 코랩 환경에 CSV 파일로 저장
with open('students.csv', mode='w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("students.csv 파일이 성공적으로 생성되었습니다!")

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto"
)

def generate_python_code(task):
    messages = [
        {
            "role": "system",
            "content": "You are an expert Python developer. Write clean, beginner-friendly Python code with comments."
        },
        {
            "role": "user",
            "content": f"""
다음 요구사항을 만족하는 Python 코드를 작성해줘.

요구사항:
{task}

조건:
- 코드만 출력
- 초보자도 이해할 수 있게 주석 포함
- 실행 가능한 완성 코드로 작성
"""
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=800,
            temperature=0.2,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.05,
            pad_token_id=tokenizer.eos_token_id
        )

    result = outputs[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(result, skip_special_tokens=True).strip()


task = """
CSV 파일을 읽어서 학생 이름, 국어, 영어, 수학 점수를 출력하고,
각 학생의 평균 점수와 전체 평균을 계산하는 프로그램
"""

code = generate_python_code(task)
print(code)
```
