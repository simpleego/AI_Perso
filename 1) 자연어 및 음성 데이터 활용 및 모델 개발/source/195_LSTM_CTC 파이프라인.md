
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SpeechRecognitionModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_classes):
        super(SpeechRecognitionModel, self).__init__()
        
        # 1. LSTM 인코딩 단계 (이미지의 2번째 단계)
        # 양방향(bidirectional=True) 설정을 통해 시간적 특성 포착 극대화
        self.lstm = nn.LSTM(
            input_size=input_dim, 
            hidden_size=hidden_dim, 
            num_layers=2, 
            batch_first=True, 
            bidirectional=True
        )
        
        # 2. 전결합층 단계 (이미지의 3번째 단계)
        # 양방향이므로 hidden_size * 2의 차원을 가짐
        self.fc = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, x):
        # x: [Batch, Time, Feature] (1단계에서 추출된 특징값)
        
        # LSTM 통과
        x, _ = self.lstm(x)
        
        # 각 타임스텝별 문자 확률 예측
        logits = self.fc(x)
        
        # CTC 손실 함수 사용을 위한 log_softmax 처리
        return F.log_softmax(logits, dim=2)

# --- 실습 시나리오 ---
input_feature_dim = 80  # 멜 스펙트로그램 차원
hidden_size = 128
num_characters = 28    # 알파벳 + Blank + Space

model = SpeechRecognitionModel(input_feature_dim, hidden_size, num_characters)

# 가상 음성 특징 데이터 (Batch: 1, Time: 100, Feature: 80)
dummy_input = torch.randn(1, 100, input_feature_dim)

# 모델 예측 결과 (각 타임스텝별 문자 확률 시퀀스)
prediction = model(dummy_input)

print(f"출력 크기: {prediction.shape}") # [1, 100, 28]
print("이 확률 시퀀스가 CTC 디코딩 단계(4단계)로 전달되어 최종 텍스트가 됩니다.")

```
