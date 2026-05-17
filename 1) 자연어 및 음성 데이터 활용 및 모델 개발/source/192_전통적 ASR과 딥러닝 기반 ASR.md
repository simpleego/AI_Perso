```python
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import librosa

# 1. 사전 학습된 모델과 프로세서 로드 (Hugging Face 제공)
# facebook의 wav2vec2-base-960h 모델은 신경망이 자동으로 특징을 학습한 모델입니다.
model_name = "facebook/wav2vec2-base-960h"
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name)

# 2. 음성 데이터 로드
# SR은 모델 학습 시 사용된 16,000Hz로 맞추는 것이 중요합니다.
audio_path = "your_speech_sample.wav" # 실습용 파일 경로
speech, sr = librosa.load(audio_path, sr=16000)

# 3. 입력 데이터 전처리 (신경망 입력용 텐서 변환)
input_values = processor(speech, return_tensors="pt", sampling_rate=sr).input_values

# 4. 모델 추론 (Logits 추출)
with torch.no_grad():
    logits = model(input_values).logits

# 5. CTC 디코딩 (가장 확률이 높은 토큰 선택 및 텍스트 변환)
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]

print("-" * 30)
print(f"인식 결과: {transcription}")
print("-" * 30)

```