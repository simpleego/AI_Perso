```python
import torch
import torch.nn as nn

class Tacotron2Encoder(nn.Module):
    """
    1. 인코더 (Encoder)
    텍스트 토큰을 입력받아 CNN과 LSTM을 거쳐 특징 벡터(Memory)를 추출
    """
    def __init__(self, vocab_size, embedding_dim=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # 3개의 1D Convolution 층 (텍스트의 국소적 문맥 파악)
        self.convolutions = nn.Sequential(
            nn.Conv1d(embedding_dim, embedding_dim, kernel_size=5, padding=2),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU(),
            nn.Conv1d(embedding_dim, embedding_dim, kernel_size=5, padding=2),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU(),
            nn.Conv1d(embedding_dim, embedding_dim, kernel_size=5, padding=2),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU()
        )
        # 양방향 LSTM (문장 전체의 전역적 문맥 파악)
        self.lstm = nn.LSTM(embedding_dim, embedding_dim // 2, 
                            num_layers=1, bidirectional=True, batch_first=True)

    def forward(self, text_tokens):
        # text_tokens 차원: [Batch, Length]
        x = self.embedding(text_tokens).transpose(1, 2) # [Batch, Embedding_dim, Length]
        x = self.convolutions(x).transpose(1, 2)        # [Batch, Length, Embedding_dim]
        
        encoder_outputs, _ = self.lstm(x)               # [Batch, Length, Embedding_dim]
        return encoder_outputs


class PostNet(nn.Module):
    """
    2. 포스트넷 (Post-net)
    디코더가 생성한 초기 멜-스펙트로그램을 보정하여 품질 향상
    """
    def __init__(self, n_mel_channels=80):
        super().__init__()
        # 5개의 1D Convolution 층으로 구성
        self.convolutions = nn.Sequential(
            nn.Conv1d(n_mel_channels, 512, kernel_size=5, padding=2),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Conv1d(512, 512, kernel_size=5, padding=2),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Conv1d(512, 512, kernel_size=5, padding=2),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Conv1d(512, 512, kernel_size=5, padding=2),
            nn.BatchNorm1d(512),
            nn.Tanh(),
            nn.Conv1d(512, n_mel_channels, kernel_size=5, padding=2),
            nn.BatchNorm1d(n_mel_channels)
        )

    def forward(self, mel_output):
        # mel_output 차원: [Batch, n_mel_channels, Frames]
        residual = self.convolutions(mel_output)
        return mel_output + residual # 잔차 연결(Residual Connection)을 통해 디테일 보정


class Tacotron2ToyPipeline(nn.Module):
    """
    Tacotron2의 전체적인 흐름을 시뮬레이션하는 토이 파이프라인
    """
    def __init__(self, vocab_size=50, n_mel_channels=80):
        super().__init__()
        self.encoder = Tacotron2Encoder(vocab_size)
        self.postnet = PostNet(n_mel_channels)
        
        # 디코더의 맛보기 형태 (실제로는 자기회귀 루프와 Attention 메커니즘이 포함됨)
        self.toy_decoder_projection = nn.Linear(512, n_mel_channels)
        self.stop_token_projection = nn.Linear(512, 1)

    def forward(self, text_tokens, target_frames=100):
        batch_size = text_tokens.size(0)
        
        # 1. 인코더 통과
        encoder_outputs = self.encoder(text_tokens)
        print(f" 인코더 출력 차원: {encoder_outputs.shape} (Batch, Length, Hidden)")

        # 2. 디코더 가상 시뮬레이션 (원래는 루프를 돌며 가변 길이 생성)
        # 여기서는 설명을 위해 target_frames 단위로 일괄 매핑하는 형태로 시뮬레이션합니다.
        # 실제 디코더는 매 스텝마다 Stop Token 가중치를 예측합니다.
        context_vector = torch.mean(encoder_outputs, dim=1, keepdim=True)
        decoder_hidden = context_vector.expand(-1, target_frames, -1)
        
        # 초기 멜-스펙트로그램 및 Stop token 예측
        mel_outputs_linear = self.toy_decoder_projection(decoder_hidden).transpose(1, 2)
        stop_tokens = self.stop_token_projection(decoder_hidden).squeeze(-1)
        
        print(f" 디코더 초기 멜 생성 차원: {mel_outputs_linear.shape} (Batch, Mel_channels, Frames)")
        print(f" 스톱 토큰 예측 차원: {stop_tokens.shape} (Batch, Frames)")

        # 3. 포스트넷을 통한 디테일 개선
        mel_outputs_postnet = self.postnet(mel_outputs_linear)
        print(f" 포스트넷 최종 보정 차원: {mel_outputs_postnet.shape} (Batch, Mel_channels, Frames)")
        
        return mel_outputs_linear, mel_outputs_postnet, stop_tokens


# --- 실행 및 검증 ---
if __name__ == "__main__":
    # 가상의 환경 설정 (배치 사이즈 2, 문장 길이 15자)
    dummy_text_input = torch.randint(low=1, high=49, size=(2, 15)) 
    
    print("=== Tacotron2 아키텍처 데이터 흐름 시뮬레이션 ===")
    model = Tacotron2ToyPipeline()
    mel_init, mel_final, stops = model(dummy_text_input)
    print("==================================================")

```
