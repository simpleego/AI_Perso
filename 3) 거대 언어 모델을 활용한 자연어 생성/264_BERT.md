아래 코드는 **BERT의 MLM([MASK] 예측)** 과 **문장 분류용 BERT**를 가장 간단히 실습하는 예제입니다. Hugging Face `pipeline`은 MLM, 감정분석 등 여러 NLP 작업을 쉽게 실행하게 해줍니다. ([Hugging Face][1])

```python
# 1. 설치
!pip install -q transformers torch
```

```python
# 2. BERT MLM 실습: [MASK] 단어 예측
from transformers import pipeline

mlm = pipeline(
    "fill-mask",
    model="bert-base-multilingual-cased"
)

text = "나는 [MASK]에서 밥을 먹었다."

results = mlm(text)

for r in results[:5]:
    print(f"예측 단어: {r['token_str']}, 점수: {r['score']:.4f}")
```

BERT는 `[MASK]` 위치의 단어를 좌우 문맥을 함께 보고 예측하는 MLM 방식으로 학습됩니다. ([Hugging Face][2])

```python
# 3. 문맥 차이에 따른 예측 비교

sentences = [
    "나는 [MASK]에서 공부를 했다.",
    "나는 [MASK]에서 밥을 먹었다.",
    "나는 [MASK]에서 영화를 봤다."
]

for s in sentences:
    print("\n입력:", s)
    results = mlm(s)
    for r in results[:3]:
        print(f"  {r['token_str']} / {r['score']:.4f}")
```

```python
# 4. BERT 기반 문장 분류 실습
# 영어 감정분석 예제

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

texts = [
    "I love this movie.",
    "This food is terrible."
]

for t in texts:
    print(t, "=>", classifier(t))
```

핵심은 이렇습니다.

```text
MLM 실습        : 문장 안의 [MASK] 단어 예측
문장 분류 실습 : 문장 전체를 보고 긍정/부정 등 분류
BERT 특징      : 왼쪽 문맥과 오른쪽 문맥을 동시에 사용
```

[1]: https://huggingface.co/docs/transformers/en/main_classes/pipelines?utm_source=chatgpt.com "Pipelines"
[2]: https://huggingface.co/docs/transformers/en/tasks/masked_language_modeling?utm_source=chatgpt.com "Masked language modeling"
