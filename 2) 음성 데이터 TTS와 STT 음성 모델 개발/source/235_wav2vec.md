```python

# 필수 라이브러리 설치 가이드
# pip install torch transformers librosa soundfile

import torch
import librosa
from transformers import AutoModelForCTC, Wav2Vec2Processor

# ==========================================
# STEP 1 & 2 & 3. 라이브러리 및 한국어 모델/프로세서 로드
# ==========================================
print("=== [STEP 1, 2, 3] Hugging Face 한국어 Wav2Vec2 모델 및 프로세서 초기화 ===")

# 한국어 음성 인식에 최적화된 Meta의 프리트레인 모델 ID 지정
model_id = "kresnik/wav2vec2-large-xlsr-korean"

# 음성 전처리 및 텍스트 디코딩을 통합 담당하는 Processor 로드
processor = Wav2Vec2Processor.from_pretrained(model_id)

# CTC 손실 함수 계층이 상단에 결합된 Wav2Vec2 모델 로드
model = AutoModelForCTC.from_pretrained(model_id)

# 연산 장치 설정 (GPU 사용이 가능하면 CUDA, 아니면 CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval() # 추론 모드로 전환 (Dropout, BatchNorm 비활성화)

print(f"-> 모델이 {device} 장치에 성공적으로 로드되었습니다.\n")


# ==========================================
# STEP 4. 오디오 파일 로드 및 전처리
# ==========================================
print("=== [STEP 4] 오디오 데이터 로드 및 16kHz 리샘플링 ===")

# 실제 마이크 녹음본이나 파일 대신, 테스트를 위해 librosa 내장 오디오 사용
# Wav2Vec2는 반드시 16000Hz 음원만 인식하므로 sr=16000 강제 지정
audio_path = librosa.example('libri1') 
speech_array, sampling_rate = librosa.load(audio_path, sr=16000)

print(f"-> 오디오 로드 완료. 샘플 수: {len(speech_array)} | 샘플링 레이트: {sampling_rate}Hz")
print(f"-> 총 오디오 재생 시간: {len(speech_array) / sampling_rate:.2f} 초\n")


# ==========================================
# STEP 5. 입력 데이터 텐서 변환 및 인공지능 추론 (Forward Pass)
# ==========================================
print("=== [STEP 5] 오디오 텐서 변환 및 Wav2Vec2 인코더 추론 ===")

# 오디오 배열 정규화 및 PyTorch Tensor 변환
inputs = processor(speech_array, sampling_rate=16000, return_tensors="pt", padding=True)
input_values = inputs.input_values.to(device)

# 그라디언트 계산을 제외하여 메모리 소모 방지
with torch.no_grad():
    # 모델에 입력하여 각 프레임별 자모음/음소 확률 분포(Logits) 획득
    logits = model(input_values).logits

print(f"-> 모델 출력 로짓(Logits) Shape: {logits.shape}")
print(f"   => [배치 크기: {logits.shape[0]}, 주파수 프레임 수: {logits.shape[1]}, 토큰 사전 크기: {logits.shape[2]}]\n")


# ==========================================
# STEP 6. 출력 후처리 및 최종 한국어 텍스트 변환 (CTC Decoding)
# ==========================================
print("=== [STEP 6] CTC Greedy Decoding 및 최종 텍스트 변환 ===")

# 1. 각 프레임 축(dim=-1)에서 가장 확률이 높은 토큰 인덱스 추출 (Greedy 최적 경로 구하기)
predicted_ids = torch.argmax(logits, dim=-1)

# 2. 프로세서의 토크나이저를 이용하여 중복 제거 및 블랭크 토큰 제거 후 문자열 복원
predicted_sentences = processor.batch_decode(predicted_ids)

print("\n" + "="*50)
print(" [Wav2Vec 2.0 한국어 음성 인식 최종 결과] ")
print("="*50)
print(f"▣ 음성 인식 예측 문장: \"{predicted_sentences[0]}\"")
print("="*50)

```

