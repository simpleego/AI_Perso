```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def main():
    # 모델 ID (영어 → 한국어 번역)
    model_id = "Helsinki-NLP/opus-mt-tc-big-en-ko"

    # 디바이스 설정 (GPU 사용 가능 시 자동 선택)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 토크나이저 & 모델 로드
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device)

    # 번역할 문장들
    src_texts = [
        "I watched a movie with my friend yesterday.",
        "Transformers are the backbone of modern NLP.",
        "Deep learning models are changing the job market."
    ]

    # 토큰화
    inputs = tokenizer(
        src_texts,
        return_tensors="pt",
        padding=True,
        truncation=True
    ).to(device)

    # 번역 생성
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=128,
            num_beams=4,
            early_stopping=True
        )

    # 디코딩
    translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    # 결과 출력
    for en, ko in zip(src_texts, translated):
        print(f"[EN] {en}")
        print(f"[KO] {ko}")
        print("-" * 50)


if __name__ == "__main__":
    main()
```
