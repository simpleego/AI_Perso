```python
import torch
import torch.nn as nn

# 1. 매개변수 설정
input_size = 80    # 입력 특징 차원 (예: Mel-spectrogram 차원)
hidden_size = 128  # 은닉 상태 차원 (이미지의 h_t 크기)
num_layers = 1     # 쌓을 LSTM 레이어 개수
batch_size = 4     # 한 번에 처리할 데이터 개수
seq_len = 50       # 시퀀스 길이 (시간축 프레임 개수)

# 2. LSTM 모델 정의
class LSTMReview(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMReview, self).__init__()
        # 이미지에 표현된 복잡한 구조가 nn.LSTM 안에 모두 구현되어 있음
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        
    def forward(self, x):
        # h0, c0: 초기 은닉 상태와 셀 상태 (지정하지 않으면 0으로 초기화)
        out, (hn, cn) = self.lstm(x)
        return out, (hn, cn)

# 3. 실습 수행
# 가상 데이터 생성: (Batch, Seq_len, Input_size)
sample_input = torch.randn(batch_size, seq_len, input_size)
model = LSTMReview(input_size, hidden_size, num_layers)

# 순전파
output, (h_n, c_n) = model(sample_input)

print("-" * 40)
print(f"입력 데이터 크기: {sample_input.shape}") # [4, 50, 80]
print(f"출력(모든 시점) 크기: {output.shape}")    # [4, 50, 128]
print(f"최종 셀 상태(cn) 크기: {c_n.shape}")      # [1, 4, 128]
print("-" * 40)

```
