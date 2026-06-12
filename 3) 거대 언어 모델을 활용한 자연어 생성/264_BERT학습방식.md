# BERT 학습 방식 코드 정리: MLM & NSP

> **출처**: 주요 언어 모델 비교 — BERT (Bidirectional Encoder Representations from Transformers, 2018, Google AI)

---

## 개요

BERT는 Transformer의 **Encoder**만 활용한 양방향 모델로, 두 가지 방식으로 사전 학습됩니다.

| 학습 방식 | 영문명 | 목적 |
|-----------|--------|------|
| MLM | Masked Language Modeling | 가려진 단어를 문맥으로 예측 |
| NSP | Next Sentence Prediction | 두 문장의 연속성 여부 예측 |

---

## 1. 기초 구현 (순수 Python)

외부 라이브러리 없이 개념을 명확히 이해할 수 있는 순수 Python 구현입니다.

### 1-1. MLM — Masked Language Modeling

```python
import random

def simple_mlm(sentence: str, mask_ratio: float = 0.15) -> tuple:
    """
    문장에서 15%의 토큰을 [MASK]로 치환.
    반환: (마스킹된 문장, 원본 레이블 딕셔너리)
    """
    tokens = sentence.split()
    labels = {}
    masked_tokens = tokens.copy()

    n_mask = max(1, int(len(tokens) * mask_ratio))
    mask_indices = random.sample(range(len(tokens)), n_mask)

    for idx in mask_indices:
        labels[idx] = tokens[idx]   # 원본 단어 저장
        r = random.random()
        if r < 0.80:
            masked_tokens[idx] = "[MASK]"           # 80%: 마스킹
        elif r < 0.90:
            masked_tokens[idx] = random.choice(tokens)  # 10%: 랜덤 치환
        # 나머지 10%: 그대로 유지 (labels에만 기록)

    return " ".join(masked_tokens), labels


# 실행 예시
sentence = "나는 학교에서 밥을 먹었다"
masked, labels = simple_mlm(sentence)
print(f"원문  : {sentence}")
print(f"마스킹: {masked}")
print(f"레이블: {labels}")

# 예시 출력
# 원문  : 나는 학교에서 밥을 먹었다
# 마스킹: 나는 [MASK] 밥을 먹었다
# 레이블: {2: '학교에서'}
```

**MLM 마스킹 전략 (BERT 논문 기준)**

- **80%** → `[MASK]`로 치환
- **10%** → 랜덤 단어로 치환
- **10%** → 원본 유지 (레이블만 기록)

---

### 1-2. NSP — Next Sentence Prediction

```python
def create_nsp_pairs(corpus: list[str], n_samples: int = 4) -> list:
    """
    corpus에서 IsNext / NotNext 쌍을 생성.
    반환: [(문장A, 문장B, is_next), ...]
    """
    pairs = []
    for i in range(n_samples):
        a_idx = random.randint(0, len(corpus) - 2)
        if random.random() < 0.5:
            # IsNext: 실제 다음 문장
            pairs.append((corpus[a_idx], corpus[a_idx + 1], True))
        else:
            # NotNext: 무작위 문장
            b_idx = random.randint(0, len(corpus) - 1)
            while b_idx == a_idx + 1:
                b_idx = random.randint(0, len(corpus) - 1)
            pairs.append((corpus[a_idx], corpus[b_idx], False))
    return pairs


# 실행 예시
corpus = [
    "나는 어제 영화를 봤다.",
    "표를 미리 예매했다.",
    "영화관은 사람이 많았다.",
    "고양이가 창밖을 봤다.",
    "날씨가 맑은 오후였다.",
]

for a, b, label in create_nsp_pairs(corpus):
    tag = "✅ IsNext" if label else "❌ NotNext"
    print(f"{tag}")
    print(f"  A: {a}")
    print(f"  B: {b}")
```

---

## 2. PyTorch 구현

실제 훈련 루프와 손실 함수까지 포함한 구현입니다.

### 2-1. MLM 손실 계산

```python
import torch
import torch.nn as nn

def mlm_loss_example():
    vocab_size = 30522   # BERT 기본 어휘 크기
    seq_len    = 10
    batch_size = 2

    # 모델 출력 (logits): [batch, seq_len, vocab_size]
    logits = torch.randn(batch_size, seq_len, vocab_size)

    # 레이블: 마스킹된 위치만 실제 토큰 ID, 나머지는 -100
    # -100 은 CrossEntropyLoss가 해당 위치를 무시하도록 하는 관례
    labels = torch.full((batch_size, seq_len), fill_value=-100)
    labels[0, 3] = 2154    # 배치 0, 위치 3: '학교'의 토큰 ID
    labels[1, 1] = 8765    # 배치 1, 위치 1: '밥'의 토큰 ID

    loss_fn = nn.CrossEntropyLoss(ignore_index=-100)
    loss = loss_fn(logits.view(-1, vocab_size), labels.view(-1))

    print(f"MLM Loss: {loss.item():.4f}")
    return loss

mlm_loss = mlm_loss_example()
```

---

### 2-2. NSP 손실 계산

```python
def nsp_loss_example():
    batch_size = 4

    # NSP 헤드 출력: [batch, 2]  (0=NotNext, 1=IsNext)
    nsp_logits = torch.tensor([
        [ 0.8, -0.3],   # IsNext 아님
        [-0.2,  1.1],   # IsNext 맞음
        [ 1.5, -0.9],   # IsNext 아님
        [-0.4,  0.7],   # IsNext 맞음
    ])

    # 레이블: 0=NotNext, 1=IsNext
    nsp_labels = torch.tensor([0, 1, 0, 1])

    loss_fn = nn.CrossEntropyLoss()
    loss = loss_fn(nsp_logits, nsp_labels)

    probs = torch.softmax(nsp_logits, dim=-1)
    print(f"NSP Loss: {loss.item():.4f}")
    print("예측 확률 (NotNext / IsNext):")
    for i, p in enumerate(probs):
        print(f"  샘플 {i}: NotNext={p[0]:.2%}, IsNext={p[1]:.2%}")
    return loss

nsp_loss = nsp_loss_example()
```

---

### 2-3. 결합 손실 (BERT 실제 학습)

```python
def combined_bert_loss(mlm_loss, nsp_loss, alpha=1.0, beta=1.0):
    """
    BERT 논문: 두 손실을 단순 합산 (equal weight)
    alpha, beta로 비율 조정 가능
    """
    total = alpha * mlm_loss + beta * nsp_loss
    print(f"MLM: {mlm_loss:.4f} | NSP: {nsp_loss:.4f} | Total: {total:.4f}")
    return total
```

> BERT 논문에서는 두 손실을 동일 가중치(1:1)로 합산합니다.  
> `Total Loss = MLM Loss + NSP Loss`

---

## 3. HuggingFace 🤗 활용

실전에서 바로 쓸 수 있는 코드입니다.

### 3-1. MLM 추론 (Fill-mask 파이프라인)

```python
from transformers import pipeline

# 한국어 BERT (klue/bert-base)
fill_mask = pipeline(
    "fill-mask",
    model="klue/bert-base",
)

examples = [
    "나는 [MASK]에서 밥을 먹었다.",
    "오늘 [MASK]가 정말 맑다.",
    "딥러닝은 [MASK] 학습 기반 기술이다.",
]

for text in examples:
    results = fill_mask(text)
    print(f"\n입력: {text}")
    for r in results[:3]:
        print(f"  {r['token_str']:10s} | 확률: {r['score']:.4f}")
```

---

### 3-2. NSP 추론 (직접 모델 호출)

```python
from transformers import BertTokenizer, BertForNextSentencePrediction
import torch

tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model     = BertForNextSentencePrediction.from_pretrained(
                "bert-base-multilingual-cased")
model.eval()

def predict_nsp(sent_a: str, sent_b: str) -> str:
    inputs = tokenizer(sent_a, sent_b, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits          # shape: [1, 2]
    prob_next = torch.softmax(logits, dim=1)[0, 0].item()
    label     = "IsNext ✅" if prob_next > 0.5 else "NotNext ❌"
    return f"{label}  (IsNext 확률: {prob_next:.2%})"


# 실행 예시
pairs = [
    ("나는 어제 영화를 봤다.", "표를 미리 예매했다."),
    ("나는 어제 영화를 봤다.", "고양이가 창밖을 봤다."),
]
for a, b in pairs:
    print(f"A: {a}")
    print(f"B: {b}")
    print(f"→ {predict_nsp(a, b)}\n")
```

---

### 3-3. 파인튜닝 (DataCollator 활용)

```python
from transformers import (
    BertTokenizer,
    BertForMaskedLM,
    DataCollatorForLanguageModeling,
    Trainer, TrainingArguments,
)
from datasets import Dataset

texts = [
    "자연어 처리는 컴퓨터가 언어를 이해하는 기술이다.",
    "BERT는 트랜스포머 인코더 구조를 사용한다.",
    "마스킹 언어 모델은 문맥을 양방향으로 학습한다.",
]

tokenizer = BertTokenizer.from_pretrained("klue/bert-base")
model     = BertForMaskedLM.from_pretrained("klue/bert-base")

# 토크나이징
tokenized = Dataset.from_dict({"text": texts}).map(
    lambda x: tokenizer(x["text"], truncation=True, max_length=64),
    batched=True, remove_columns=["text"]
)

# DataCollator가 자동으로 15% 마스킹 처리
collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=True,
    mlm_probability=0.15,
)

trainer = Trainer(
    model=model,
    args=TrainingArguments(
        output_dir="./bert-finetuned",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        logging_steps=10,
    ),
    train_dataset=tokenized,
    data_collator=collator,
)
trainer.train()
```

---

## 4. 핵심 개념 요약

### MLM (Masked Language Modeling)

| 항목 | 내용 |
|------|------|
| 마스킹 비율 | 전체 토큰의 15% |
| [MASK] 치환 | 마스킹 대상의 80% |
| 랜덤 치환 | 마스킹 대상의 10% |
| 원본 유지 | 마스킹 대상의 10% |
| 손실 함수 | `CrossEntropyLoss(ignore_index=-100)` |
| 예측 대상 | 마스킹된 위치의 원본 토큰 ID |

### NSP (Next Sentence Prediction)

| 항목 | 내용 |
|------|------|
| 입력 형식 | `[CLS] 문장A [SEP] 문장B [SEP]` |
| 레이블 | 0 = NotNext, 1 = IsNext |
| 데이터 비율 | IsNext 50% / NotNext 50% |
| 손실 함수 | `CrossEntropyLoss` (이진 분류) |
| 예측 위치 | `[CLS]` 토큰의 풀링 출력 |

### BERT 최종 학습 손실

```
Total Loss = MLM Loss + NSP Loss
```

---

## 5. 추천 모델 (한국어)

| 모델 | 출처 | 특징 |
|------|------|------|
| `klue/bert-base` | KLUE | 한국어 특화, 범용 |
| `snunlp/KR-ELECTRA-discriminator` | SNU NLP | 경량·고성능 |
| `bert-base-multilingual-cased` | Google | 104개 언어 지원 |

---

*참고: BERT 원논문 — Devlin et al., 2018, "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"*
