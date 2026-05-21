```python
import torch
import torch.nn as nn

class LengthRegulator(nn.Module):
    """
    FastSpeech의 핵심: 길이 조절기 (Length Regulator)
    텍스트 인코더의 출력 벡터를 예측된 음소 길이(Duration)만큼 복사하여 
    멜-스펙트로그램 프레임 길이로 확장하는 모듈입니다.
    """
    def __init__(self):
        super().__init__()

    def forward(self, encoder_outputs, durations):
        """
        Args:
            encoder_outputs (Tensor): 인코더를 거쳐 나온 텍스트 특징 벡터 
                                      차원: [Batch, Length, Hidden_Dim]
            durations (Tensor): 각 글자(음소)가 소리 날 시간(프레임 수) 데이터 
                                차원: [Batch, Length] (정수형 정렬 배열)
        """
        batch_size = encoder_outputs.size(0)
        hidden_dim = encoder_outputs.size(2)
        
        # 1. 배치 내에서 최종적으로 생성될 오디오의 총 프레임 길이 계산
        # 각 배치의 duration 합 중 가장 큰 값을 기준으로 타깃 길이를 잡습니다.
        max_mel_len = torch.max(torch.sum(durations, dim=1)).item()
        
        # 확장된 출력을 담을 그릇 준비 [Batch, Max_Mel_Frames, Hidden_Dim]
        output = torch.zeros(batch_size, max_mel_len, hidden_dim).to(encoder_outputs.device)
        
        # 2. 각 배치(문장)별로 루프를 돌며 정렬 확장 진행 (이해하기 쉬운 구조 표현)
        for i in range(batch_size):
            current_idx = 0
            # 문장 내부의 글자(토큰) 단위로 탐색
            for j in range(encoder_outputs.size(1)):
                duration_j = durations[i, j].item() # j번째 글자가 지속될 프레임 수
                if duration_j == 0:
                    continue
                
                # j번째 글자의 인코더 특징 벡터를 추출
                token_vector = encoder_outputs[i, j, :] # [Hidden_Dim]
                
                # 해당 특징 벡터를 duration_j만큼 반복하여 채워 넣음 (리피팅 효과)
                output[i, current_idx : current_idx + duration_j, :] = token_vector.expand(duration_j, -1)
                current_idx += duration_j
                
        return output

# --- 변동성 예측기 및 전체 흐름 시뮬레이션 ---
if __name__ == "__main__":
    print("=== FastSpeech 길이 조절기(Length Regulator) 데이터 흐름 테스트 ===")
    
    # 1. 가상의 입력 설정 (배치 크기=1, 문장 글자 수=3자, 은닉층 차원=4)
    # 문장 예시: "a b c"
    batch_size = 1
    seq_len = 3
    hidden_dim = 4
    
    # 가상의 인코더 출력 벡터 생성
    fake_encoder_outputs = torch.randn(batch_size, seq_len, hidden_dim)
    
    # Duration Predictor가 예측했다고 가정하는 각 글자의 발화 길이 (프레임 수)
    # 첫 번째 글자는 2프레임, 두 번째 글자는 4프레임, 세 번째 글자는 3프레임 동안 발음됨 의미
    fake_durations = torch.tensor([[2, 4, 3]], dtype=torch.long) 
    
    print(f"입력 데이터 (인코더 출력 차원): {fake_encoder_outputs.shape} (Batch, 글자수, Hidden)")
    print(f"예측된 글자별 발음 길이 (Duration): {fake_durations.tolist()[0]}")
    print(f" -> 예상되는 총 오디오 프레임 수: {sum(fake_durations.tolist()[0])} 프레임\n")
    
    # 2. 길이 조절기 작동
    lr = LengthRegulator()
    expanded_outputs = lr(fake_encoder_outputs, fake_durations)
    
    print("--------------------------------------------------")
    print(f"최종 확장된 디코더 입력 차원: {expanded_outputs.shape} (Batch, 오디오프레임수, Hidden)")
    print("--------------------------------------------------")
    print("비자기회귀 모델은 이 변환된 차원을 기반으로")
    print("트랜스포머 디코더를 거쳐 전체 멜-스펙트로그램을 단 '한 번에' 출력합니다.")
```
