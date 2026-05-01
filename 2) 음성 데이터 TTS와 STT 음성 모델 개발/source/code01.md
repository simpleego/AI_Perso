# 🎤 음성 데이터를 활용한 TTS와 STT 모델 개발
---

## ✅ 추출된 Python 소스 코드 모음

```python
# Google Colab에서 주요 NLP 라이브러리 설치
!pip install nltk konlpy spacy gensim
!pip install transformers
!pip install matplotlib seaborn

# NLTK 기본 데이터 다운로드
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# spaCy 영어 모델 다운로드
!python -m spacy download en_core_web_sm

# 설치 확인
import nltk
import konlpy
import spacy
import transformers

print("모든 라이브러리가 성공적으로 설치되었습니다!")
```

```python
# 다의어 "배"의 의미 분석하기
sentences = [
    "저는 어제 배를 먹었습니다.",  # 과일
    "우리는 배를 타고 섬으로 갔습니다.",  # 선박
    "운동 후에 배가 아팠습니다."  # 신체
]

from konlpy.tag import Okt
okt = Okt()

for i, sentence in enumerate(sentences):
    print(f"\n문장 {i+1}: {sentence}")
    print("형태소 분석 결과:")
    print(okt.pos(sentence))

    words = okt.morphs(sentence)
    if "배" in words:
        idx = words.index("배")
        context = words[max(0, idx-2):min(len(words), idx+3)]
        print(f"'배' 주변 문맥: {context}")
```

```python
# NLTK를 이용한 영어 불용어 제거
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

text = "The quick brown fox jumps over the lazy dog"
stop_words = set(stopwords.words('english'))

tokens = word_tokenize(text.lower())
filtered = [w for w in tokens if w not in stop_words]
print(filtered)  # ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']
```

```python
# 한국어 불용어 제거 예시
from konlpy.tag import Okt

okt = Okt()
text = "나는 오늘 학교에 갔습니다"
korean_stopwords = ["나는", "은", "는", "이", "가", "을", "를", "에", "에서"]

tokens = okt.morphs(text)
filtered = [w for w in tokens if w not in korean_stopwords]
print(filtered)  # ['오늘', '학교', '갔습니다']
```

```python
from nltk.stem import PorterStemmer
ps = PorterStemmer()
words = ["running", "runs", "ran", "easily", "fairly"]
[ps.stem(w) for w in words]
# ['run', 'run', 'ran', 'easili', 'fairli']
```

```python
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
words = ["running", "runs", "ran", "mice", "better"]
[lemmatizer.lemmatize(w) for w in words]
# ['running', 'run', 'ran', 'mouse', 'better']
```

```python
import re
from konlpy.tag import Okt

okt = Okt()
RE_PUNCT = re.compile(r"[^\w\s]", flags=re.UNICODE)
RE_NUM = re.compile(r"\d+")

def preprocess_korean_text(text, keep_num=False, num_token=" <NUM>"):
    text = text.lower()
    text = RE_PUNCT.sub(" ", text)
    if keep_num:
        text = RE_NUM.sub(num_token, text)
    else:
        text = RE_NUM.sub(" ", text)

    tokens = okt.morphs(text)
    stopwords = {"은", "는", "이", "가", "을", "를", "에", "의", "으로", "도", "에서"}
    tokens = [t for t in tokens if t not in stopwords and t.strip()]
    return tokens

sample_text = "오늘은 날씨가 좋아서 공원에서 산책을 했습니다. 사람들 200 명이 벚꽃을 구경했어요!"
processed = preprocess_korean_text(sample_text, keep_num=True)
print(processed)
```

```python
# 뉴스 데이터 전처리 예시
import pandas as pd
news_df = pd.read_csv('korean_news_sample.csv')
news_df['processed_content'] = news_df['content'].apply(preprocess_korean_text)
news_df.to_csv('preprocessed_news.csv', index=False)
```

```python
# NLTK word_tokenize 사용
from nltk.tokenize import word_tokenize
text = "Don't hesitate to ask questions!"
tokens = word_tokenize(text)
print(tokens)  # ['Do', "n't", 'hesitate', 'to', 'ask', 'questions', '!']
```

```python
# spaCy 토큰화
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
tokens = [token.text for token in doc]
print(tokens)  # ['Do', "n't", 'hesitate', 'to', 'ask', 'questions', '!']
```

```python
from konlpy.tag import Okt, Mecab, Komoran, Kkma
import time

text = "자연어처리는 인공지능의 중요한 분야 중 하나입니다."

okt = Okt()
# mecab = Mecab()  # 시스템에 mecab이 설치된 경우
komoran = Komoran()
kkma = Kkma()

print("OKT:", okt.morphs(text))
print("Komoran:", komoran.morphs(text))
print("Kkma:", kkma.morphs(text))

print("\nOKT 품사 태깅:", okt.pos(text))
print("Komoran 품사 태깅:", komoran.pos(text))
print("Kkma 품사 태깅:", kkma.pos(text))

# 속도 비교
times = {}
for name, analyzer in [("OKT", okt), ("Komoran", komoran), ("Kkma", kkma)]:
    start = time.time()
    for _ in range(100):
        analyzer.morphs(text)
    times[name] = time.time() - start
print("\n속도 비교 (100회 반복):")
for name, elapsed in times.items():
    print(f"{name}: {elapsed:.4f}초")
```

```python
# 문자 단위 토큰화
def char_tokenize(text):
    return list(text)

text = "Hello, NLP!"
char_tokens = char_tokenize(text)
print(char_tokens)
# ['H', 'e', 'l', 'l', 'o', ',', ' ', 'N', 'L', 'P', '!']
```

```python
# BPE 토크나이저 사용하기
# Hugging Face tokenizers 라이브러리 설치
!pip install tokenizers

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

corpus = [
    "안녕하세요 자연어처리를 배우고 있습니다",
    "자연어처리는 인공지능의 중요한 분야입니다",
    "토큰화는 자연어처리의 기본 과정입니다",
    "BPE는 자주 등장하는 문자열을 하나의 토큰으로 만듭니다"
]

tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"], vocab_size=1000)
tokenizer.pre_tokenizer = Whitespace()
tokenizer.train_from_iterator(corpus, trainer)

encoded = tokenizer.encode("자연어처리 모델을 학습해봅시다")
print(f"토큰 ID: {encoded.ids}")
print(f"토큰: {encoded.tokens}")

tokenizer.save("bpe_korean.json")
```

```python
# Hugging Face Transformers 토크나이저
from transformers import BertTokenizer, GPT2Tokenizer, RobertaTokenizer

text = "Transformers 모델의 토큰화 방식을 비교해 봅시다."

# BERT
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
bert_tokens = bert_tokenizer.tokenize(text)
print("BERT 토큰화 결과:", bert_tokens)

# GPT-2
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_tokens = gpt2_tokenizer.tokenize(text)
print("GPT-2 토큰화 결과:", gpt2_tokens)

# RoBERTa
roberta_tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
roberta_tokens = roberta_tokenizer.tokenize(text)
print("RoBERTa 토큰화 결과:", roberta_tokens)
```

```python
# 원-핫 인코딩 예시
vocabulary = ["자연어", "처리", "임베딩", "모델", "학습"]
word_to_idx = {word: i for i, word in enumerate(vocabulary)}

def one_hot_encode(word, vocab_size):
    vector = [0] * vocab_size
    vector[word_to_idx[word]] = 1
    return vector

embedding_vector = one_hot_encode("임베딩", len(vocabulary))
print(embedding_vector)  # [0, 0, 1, 0, 0]
```

```python
# TF-IDF 구현
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    "자연어 처리는 컴퓨터가 인간의 언어를 이해하는 분야입니다",
    "자연어 처리 기술은 검색, 번역, 감성 분석 등에 활용됩니다",
    "임베딩은 자연어 처리의 중요한 기술입니다"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)
print(vectorizer.get_feature_names_out())
print(X.toarray())
```

```python
# Gensim Word2Vec 학습
!pip install gensim

import gensim
from gensim.models import Word2Vec
from konlpy.tag import Okt

sentences = [
    "자연어 처리는 컴퓨터가 인간의 언어를 이해하는 분야입니다",
    "딥러닝을 활용한 자연어 처리 기술이 발전하고 있습니다",
    "워드 임베딩은 단어의 의미를 벡터로 표현하는 기술입니다",
    "한국어 처리를 위해서는 형태소 분석이 중요합니다",
    "딥러닝 모델은 대량의 데이터로 학습하는 것이 중요합니다"
]

okt = Okt()
tokenized_sentences = [okt.morphs(sentence) for sentence in sentences]

model = Word2Vec(
    sentences=tokenized_sentences,
    vector_size=100,
    window=3,
    min_count=1,
    sg=1,
    workers=4,
    epochs=20,
    seed=42
)

model.save("word2vec.model")
loaded_model = Word2Vec.load("word2vec.model")

similar_words = model.wv.most_similar("자연어", topn=5)
print("'자연어'와 가장 유사한 단어들:")
for word, similarity in similar_words:
    print(f"{word}: {similarity:.4f}")
```

```python
# FastText 모델 학습
from gensim.models import FastText

fasttext_model = FastText(
    sentences=tokenized_sentences,
    vector_size=100,
    window=3,
    min_count=1,
    sg=1,
    min_n=2,
    max_n=4
)

fasttext_model.save("fasttext.model")
similar_words = fasttext_model.wv.most_similar("자연어", topn=5)
print("'자연어'와 가장 유사한 단어들 (FastText):")
for word, similarity in similar_words:
    print(f"{word}: {similarity:.4f}")
```

```python
# 임베딩 시각화 (t-SNE)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def plot_embeddings(model, word_list, filename=None):
    word_vectors = np.array([model.wv[word] for word in word_list if word in model.wv])
    words = [word for word in word_list if word in model.wv]

    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(word_vectors)

    plt.figure(figsize=(12, 8))
    plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='steelblue', alpha=0.5)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(embeddings_2d[i, 0], embeddings_2d[i, 1]),
                     xytext=(5, 2), textcoords='offset points', fontsize=12)
    plt.title('Word Embeddings Visualization (t-SNE)')
    plt.grid(True)
    if filename:
        plt.savefig(filename)
    plt.show()

words_to_plot = ["자연어", "처리", "인공지능", "딥러닝", "컴퓨터", "모델", "학습", "데이터", "분석", "알고리즘"]
plot_embeddings(model, words_to_plot, "word2vec_viz.png")
```

```python
# Hugging Face BERT 사용하기
from transformers import BertModel, BertTokenizer
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertModel.from_pretrained('bert-base-multilingual-cased')

sentences = [
    "자연어 처리는 컴퓨터가 인간의 언어를 이해하는 분야입니다.",
    "배를 타고 여행을 떠났습니다.",
    "배가 너무 달아서 많이 먹었습니다."
]

for sentence in sentences:
    inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    sentence_embedding = outputs.last_hidden_state[:, 0, :].numpy()
```

```python
# KoBERT 사용 예시 (설치 필요)
# !pip install git+https://github.com/SKTBrain/KoBERT.git@master

import torch
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
from transformers import BertTokenizer

bertmodel, vocab = get_pytorch_kobert_model()
tokenizer = get_tokenizer()
token_indexer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')

def get_sentence_embedding(sentence):
    tokens = tokenizer(sentence)
    token_ids = token_indexer.convert_tokens_to_ids(tokens)
    token_tensor = torch.tensor([token_ids])
    with torch.no_grad():
        _, pooler = bertmodel(token_tensor)
    return pooler.numpy()
```

```python
# 음성 신호 처리 파이프라인 (Librosa)
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

y, sr = librosa.load("안녕하세요.wav", sr=16000)
print(f"샘플링레이트: {sr}, 길이: {len(y)/sr:.2f}초")

# 파형 시각화
plt.figure(figsize=(10, 3))
librosa.display.waveshow(y, sr=sr)
plt.title("'안녕하세요' 파형 (Waveform)")
plt.show()

# 스펙트로그램
D = librosa.stft(y, n_fft=512, hop_length=160, win_length=400)
S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
plt.figure(figsize=(10, 4))
librosa.display.specshow(S_db, sr=sr, x_axis="time", y_axis="hz")
plt.show()

# 멜스펙트로그램
mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=512, hop_length=160, n_mels=40)
mel_db = librosa.amplitude_to_db(mel_spec, ref=np.max)
plt.figure(figsize=(10, 4))
librosa.display.specshow(mel_db, x_axis="time", y_axis="mel", sr=sr)
plt.show()

# MFCC
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=512, hop_length=160)
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis="time", sr=sr)
plt.show()
```

```python
# Pre-emphasis 필터 구현
def pre_emphasis(signal, alpha=0.95):
    return np.append(signal[0], signal[1:] - alpha * signal[:-1])
```

```python
# Noise Gate 구현 (간단 버전)
def noise_gate(signal, threshold=0.01, beta=0):
    gated = np.copy(signal)
    mask = np.abs(signal) < threshold
    gated[mask] = beta * signal[mask]
    return gated
```

```python
# Silence Trimming (Librosa)
y_trimmed, index = librosa.effects.trim(y, top_db=20, frame_length=512, hop_length=128)
```

```python
# RNN-CTC 모델 인퍼런스 예시
import torch
import torchaudio
# from model import RNNCTC  # 사전 정의된 모델 클래스

# model = RNNCTC.load_from_checkpoint("pretrained/rnn_ctc.pt")
# model.eval()

# waveform, sample_rate = torchaudio.load("librispeech_sample.wav")
# features = torchaudio.transforms.MFCC(sample_rate=sample_rate, n_mfcc=40)(waveform)

# with torch.no_grad():
#     output = model(features)
#     decoded_text = model.decode(output)
# print(f"인식 결과: {decoded_text}")
```

```python
# HuggingFace Wav2Vec2 ASR
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch
import librosa

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

audio, rate = librosa.load("sample.wav", sr=16000)
input_values = processor(audio, return_tensors="pt", sampling_rate=rate).input_values

with torch.no_grad():
    logits = model(input_values).logits

predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]
print(f"인식 결과: {transcription}")
```

```python
# Whisper 설치 및 사용
# pip install openai-whisper torch
# pip install git+https://github.com/openai/whisper.git

import whisper

model = whisper.load_model("medium")
result = model.transcribe("안녕하세요.wav", language="ko")
print(result["text"])

for segment in result["segments"]:
    start = segment["start"]
    end = segment["end"]
    text = segment["text"]
    print(f"{start:.2f} → {end:.2f}: {text}")
```

---
