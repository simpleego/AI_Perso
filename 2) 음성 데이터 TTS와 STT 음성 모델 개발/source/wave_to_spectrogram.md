import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

# 1. 음성 파일 불러오기
y, sr = librosa.load(librosa.example('trumpet'))  # librosa 내장 샘플 사용

# 2. FFT 스펙트럼 계산
fft = np.fft.fft(y)
magnitude = np.abs(fft)
freq = np.linspace(0, sr, len(magnitude))

# 3. STFT 스펙트로그램
D = np.abs(librosa.stft(y))

# 4. 멜 스펙트로그램
S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
S_dB = librosa.amplitude_to_db(S, ref=np.max)

# 5. 서브플롯 구성 (세로 방향)
fig, axes = plt.subplots(4, 1, figsize=(12, 20))

# (a) 파형
librosa.display.waveshow(y, sr=sr, ax=axes[0])
axes[0].set_title("Waveform")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")

# (b) 스펙트럼
axes[1].plot(freq[:len(freq)//2], magnitude[:len(magnitude)//2])
axes[1].set_title("Spectrum (FFT)")
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("Magnitude")

# (c) 스펙트로그램
img1 = librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max),
                                sr=sr, x_axis='time', y_axis='log', ax=axes[2])
axes[2].set_title("Spectrogram (STFT)")
fig.colorbar(img1, ax=axes[2], format="%+2.0f dB")

# (d) 멜 스펙트로그램
img2 = librosa.display.specshow(S_dB, sr=sr, x_axis='time',
                                y_axis='mel', fmax=8000, ax=axes[3])
axes[3].set_title("Mel-Spectrogram")
fig.colorbar(img2, ax=axes[3], format="%+2.0f dB")

plt.tight_layout()
plt.show()
