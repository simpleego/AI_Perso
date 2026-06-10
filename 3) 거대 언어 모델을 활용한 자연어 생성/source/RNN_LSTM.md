```python

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# 1. 간단한 LSTM 모델 정의
class SimpleLSTM(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(SimpleLSTM, self).__init__()
        # batch_first=True 설정으로 입력 형태를 (batch, seq, feature)로 맞춤
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # 전체 시퀀스 처리
        out, (hn, cn) = self.lstm(x)
        # 마지막 타임스텝(단어)의 은닉 상태(hidden state)만 사용하여 최종 결과 예측
        last_out = out[:, -1, :]
        pred = self.fc(last_out)
        return pred

# 2. 하이퍼파라미터 및 문장 길이 설정
seq_len = 50        # 문장의 길이 (예: 50개의 단어로 이루어진 긴 문장)
input_size = 10     # 각 단어를 표현하는 임베딩 벡터의 차원 수
hidden_size = 20    # LSTM 내부의 은닉 상태 차원 수

model = SimpleLSTM(input_size, hidden_size)

# 3. 실험용 더미 데이터 생성
# requires_grad=True를 설정하여 입력(단어들)에 대한 기울기(Gradient)를 추적합니다.
# 기울기가 크면 최종 결과에 미치는 영향이 크고, 0에 가까우면 영향력이 소실된 것입니다.
inputs = torch.randn(1, seq_len, input_size, requires_grad=True)
target = torch.tensor([[1.0]]) # 임의의 예측 타겟

# 4. 순전파(Forward) 및 손실(Loss) 계산
output = model(inputs)
criterion = nn.MSELoss()
loss = criterion(output, target)

# 5. 역전파(Backward) 실행
model.zero_grad()
loss.backward()

# 6. 타임스텝(단어 위치)별 입력 데이터의 기울기 절대값 평균 계산
# inputs.grad 차원: (1, 50, 10) -> 단어별로 10개 피처의 기울기 평균을 구함
gradients = inputs.grad.abs().squeeze(0).mean(dim=1).numpy()

# 7. 이론 확인 (초반 단어 vs 후반 단어의 영향력 비교)
print("=== 단어 위치별 최종 결과에 미치는 영향력(Gradient) ===")
# 인덱스 5를 "졸업했다", 인덱스 48을 "교사로" 라고 가정
print(f"문장 초반 ('졸업했다', t=5)의 기울기 크기  : {gradients[5]:.8f}")
print(f"문장 후반 ('교사로', t=48)의 기울기 크기  : {gradients[48]:.8f}")

# 8. 시각화를 통한 직관적 확인
plt.figure(figsize=(10, 5))
plt.plot(gradients, marker='o', color='b')
plt.title("Vanishing Gradient in LSTM over Time Steps")
plt.xlabel("Time Step (Word Position in Sentence)")
plt.ylabel("Gradient Magnitude (Influence on Final Output)")
plt.grid(True)
plt.show()


```
