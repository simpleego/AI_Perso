```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# 1. 간단한 E2E 모델 정의 (RNN 기반)
class SimpleE2EModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleE2EModel, self).__init__()
        self.rnn = nn.LSTM(input_dim, hidden_dim, batch_first=True, bidirectional=True)
        # 출력 차원은 문자 집합 크기 + 1 (CTC용 blank 토큰 포함)
        self.fc = nn.Linear(hidden_dim * 2, output_dim + 1)

    def forward(self, x):
        x, _ = self.rnn(x)
        logits = self.fc(x)
        # CTC 손실 함수는 log_softmax 형태의 확률값을 입력으로 받음
        return F.log_softmax(logits, dim=2)

# 2. 데이터 및 매개변수 설정
batch_size = 2
input_dim = 80       # 멜 스펙트로그램 특징 차원
hidden_dim = 128
char_classes = 26    # 알파벳 개수 가정
input_lengths = torch.full(size=(batch_size,), fill_value=100, dtype=torch.long) # 음성 프레임 길이
target_lengths = torch.randint(low=10, high=20, size=(batch_size,), dtype=torch.long) # 실제 텍스트 길이

# 가상 데이터 생성
inputs = torch.randn(batch_size, 100, input_dim) # [Batch, Time, Feature]
targets = torch.randint(low=1, high=char_classes, size=(batch_size, 20), dtype=torch.long)

# 3. 모델 및 손실 함수 선언
model = SimpleE2EModel(input_dim, hidden_dim, char_classes)
ctc_loss = nn.CTCLoss(blank=0) # 0번 인덱스를 CTC blank 토큰으로 지정

# 4. 순전파 및 손실 계산
# [Time, Batch, Class] 형태로 차원 변경 (PyTorch CTCLoss 기본 사양)
log_probs = model(inputs).transpose(0, 1)

loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)

print(f"CTC Loss: {loss.item():.4f}")
loss.backward()
print("역전파 완료: E2E 신경망이 전체 파이프라인을 동시에 학습합니다.")

```
