# 거대 언어 모델을 활용한 자연어 생성

---

## 페이지 12 - Transformer 번역 모델 사용하기

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM 
import torch

model_id = "Helsinki-NLP/opus-mt-tc-big-en-ko"

tokenizer = AutoTokenizer.from_pretrained(model_id) 
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src_texts = [  
    "I watched a movie with my friend yesterday.",  
    "Transformers are the backbone of modern NLP.",  
    "Deep learning models are changing the job market." 
]

inputs = tokenizer(src_texts, return_tensors="pt", padding=True, truncation=True) 
with torch.no_grad(): 
    outputs = model.generate(**inputs, max_length=128, num_beams=4)

translated = tokenizer.batch_decode(outputs, skip_special_tokens=True) 
for en, ko in zip(src_texts, translated): 
    print(f"[EN] {en}\n[KO] {ko}\n")
```

---

## 페이지 24 - Hugging Face에서 LLaMA 불러오기

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# 모델과 토크나이저 불러오기 (예: LLaMA-1-7B) 
model_name = "huggyllama/llama-7b"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto"  # GPU/TPU 자동 할당
)
```

---

## 페이지 25 - 첫 번째 텍스트 생성 실습

```python
# 텍스트 생성 
inputs = tokenizer("오늘 날씨가 좋아서", return_tensors="pt").to("cuda") 
outputs = model.generate(**inputs, max_new_tokens=30) 
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 페이지 27 - LLaMA를 이용한 문서 요약

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "huggyllama/llama-7b" 
tokenizer = AutoTokenizer.from_pretrained(model_name) 
model = AutoModelForCausalLM.from_pretrained(model_name)

def summarize(text):
    prompt = f"다음 글을 2~3문장으로 요약:\n{text}\n요약:"
    x = tokenizer(prompt, return_tensors="pt")
    y = model.generate(**x, max_new_tokens=100)
    return tokenizer.decode(y[0], skip_special_tokens=True)
```

---

## 페이지 28 - LoRA 설정 (파인튜닝 준비)

```python
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model) 
peft_cfg = LoraConfig( 
    r=16, 
    lora_alpha=32, 
    lora_dropout=0.05, 
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]  # LLaMA 계열 핵심 프로젝션 
) 
model = get_peft_model(model, peft_cfg) 
model.print_trainable_parameters()
```
