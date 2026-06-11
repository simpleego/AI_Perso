
```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# 모델 ID (영어 → 한국어 번역)
# model_id = "Helsinki-NLP/opus-mt-tc-big-en-ko"
# model_id = "Helsinki-NLP/opus-mt-en-ko"

# 모델 ID (Meta의 NLLB 600M 모델)
model_id = "facebook/nllb-200-distilled-600M"

# 디바이스 설정 (GPU 사용 가능 시 자동 선택)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# 토크나이저 & 모델 로드
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device)

# 번역할 문장들
src_texts = [
    " I watched a movie with my friend yesterday.",
    " Transformers are the backbone of modern NLP.",
    " Deep learning models are changing the job market."
]

# 토큰화
inputs = tokenizer(
        src_texts,
        return_tensors="pt",
        padding=True,
        truncation=True
).to(device)

print(inputs)

# 번역 생성 (타겟 언어: 한국어 지정)
# 번역 생성 (타겟 언어: 한국어 지정)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("kor_Hang"),
        max_length=128,
        num_beams=4,
        early_stopping=True
    )

최신 버전의 transformers 라이브러리에서 NllbTokenizer의 내부 구조가 변경되면서 발생한 에러입니다. 기존에 타겟 언어의 토큰 ID를 가져올 때 사용하던 lang_code_to_id 속성이 제거되었기 때문에 해당 오류(AttributeError)가 출력되었습니다.

이를 해결하려면 텍스트 형태의 언어 코드를 토큰 ID로 변환해 주는 표준 메서드인 convert_tokens_to_ids를 사용하시면 됩니다.

# ---
1. 파라미터별 상세 설명
inputs

의미: 앞서 토크나이저를 통해 인코딩된 입력 문장 데이터(input_ids, attention_mask 등)를 딕셔너리 형태로 풀어헤쳐() 모델에 전달합니다. 모델이 '무엇을 바탕으로 번역해야 하는지' 알려주는 필수 데이터입니다.

forced_bos_token_id

의미: 생성될 문장의 첫 번째 토큰(BOS: Beginning of Sequence)을 강제로 특정 토큰으로 지정합니다. NLLB 모델 같은 다국어 번역 모델에서는 이 첫 토큰을 타겟 언어 코드(예: 한국어의 경우 kor_Hang)로 지정하여 모델이 어떤 언어로 번역해야 하는지 결정합니다.

max_length

의미: 생성할 최대 토큰 길이를 제한합니다. 여기서는 번역된 한국어 문장이 최대 128토큰을 넘지 않도록 제한하고 있습니다.

num_beams

의미: 텍스트 생성 알고리즘 중 하나인 빔 서치(Beam Search)의 빔 개수를 설정합니다. 값을 4로 지정하면 매 순간 가장 확률이 높은 상위 4개의 문장 후보군을 유지하며 최적의 번역 결과를 찾습니다. (값이 클수록 품질이 좋아질 수 있으나 연산량이 늘어납니다.)

early_stopping

의미: 빔 서치 진행 중, 더 이상 현재 후보군보다 더 나은 문장이 나올 가능성이 없다고 판단되면 설정한 max_length에 도달하기 전이라도 생성을 조기에 종료하여 속도를 높입니다.

# 디코딩
translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)

print(type(translated))

# 결과 출력
for en, ko in zip(src_texts, translated):
    print(f"[EN] {en}")
    print(f"[KO] {ko}")
    print("-" * 50)
```
