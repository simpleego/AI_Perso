```python
import torch
import torch.nn as nn
import torchaudio

# -----------------------------
# 1) Encoder (BiLSTM)
# -----------------------------
class Encoder(nn.Module):
    def __init__(self, input_dim=80, hidden_dim=256, num_layers=3):
        super().__init__()
        self.lstm = nn.LSTM(
            input_dim, hidden_dim, num_layers=num_layers,
            batch_first=True, bidirectional=True
        )

    def forward(self, x):
        outputs, _ = self.lstm(x)
        return outputs  # (B, T, 2H)


# -----------------------------
# 2) Attention
# -----------------------------
class Attention(nn.Module):
    def __init__(self, enc_dim, dec_dim):
        super().__init__()
        self.energy = nn.Linear(enc_dim + dec_dim, 1)

    def forward(self, decoder_state, encoder_outputs):
        T = encoder_outputs.size(1)
        decoder_state = decoder_state.unsqueeze(1).repeat(1, T, 1)
        energy = self.energy(torch.cat([decoder_state, encoder_outputs], dim=-1))
        attn_weights = torch.softmax(energy.squeeze(-1), dim=-1)
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs)
        return context.squeeze(1), attn_weights


# -----------------------------
# 3) Decoder (LSTM)
# -----------------------------
class Decoder(nn.Module):
    def __init__(self, vocab_size, enc_dim=512, dec_dim=256):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, dec_dim)
        self.lstm = nn.LSTMCell(dec_dim + enc_dim, dec_dim)
        self.attention = Attention(enc_dim, dec_dim)
        self.fc = nn.Linear(dec_dim + enc_dim, vocab_size)

    def forward(self, encoder_outputs, targets):
        B, T, _ = encoder_outputs.size()
        outputs = []

        h, c = torch.zeros(B, 256), torch.zeros(B, 256)
        y = torch.zeros(B, dtype=torch.long)  # <sos>

        for t in range(targets.size(1)):
            emb = self.embedding(y)
            context, _ = self.attention(h, encoder_outputs)
            h, c = self.lstm(torch.cat([emb, context], dim=-1), (h, c))
            logits = self.fc(torch.cat([h, context], dim=-1))
            outputs.append(logits)
            y = targets[:, t]  # Teacher Forcing

        return torch.stack(outputs, dim=1)


# -----------------------------
# 4) 전체 LAS 모델
# -----------------------------
class LAS(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.encoder = Encoder()
        self.decoder = Decoder(vocab_size)

    def forward(self, features, targets):
        enc_out = self.encoder(features)
        dec_out = self.decoder(enc_out, targets)
        return dec_out
```