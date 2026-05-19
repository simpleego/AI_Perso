```python
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# 1. 샘플 데이터 로드 (Librosa 제공 기본 음성 소스 사용)
# y: 오디오 시계열 데이터, sr: 샘플링 레이트 (기본값 22050Hz)
audio_path = librosa.example('nutcracker')
y, sr = librosa.load(audio_path, duration=5.0) # 앞부분 5초만 사용

# 2. STFT 하이퍼파라미터 설정
n_fft = 2048         # FFT 창 크기 (win_length의 기본값은 n_fft)
hop_length = 512     # 오버랩을 제외하고 이동할 거리 (Overlap = n_fft - hop_length)
window = 'hann'      # 창 함수 지정 (Hanning window)

# 3. STFT 수행 (Short-Time Fourier Transform)
# stft_result는 복소수(Complex형태) 행렬을 반환함
stft_result = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, window=window)

# 4. 진폭(Amplitude) 추출 및 데시벨(dB) 스케일 변환
amplitude = np.abs(stft_result)
spectrogram_db = librosa.amplitude_to_db(amplitude, ref=np.max)

# 5. 시각화
plt.figure(figsize=(12, 8))

# 파형(Waveform) 플롯
plt.subplot(2, 1, 1)
librosa.display.waveshow(y, sr=sr, color='blue')
plt.title('1. Waveform (Time Domain)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')

# 스펙트로그램(Spectrogram) 플롯
plt.subplot(2, 1, 2)
librosa.display.specshow(spectrogram_db, sr=sr, hop_length=hop_length, 
                         x_axis='time', y_axis='linear', cmap='magma')
plt.colorbar(format='%+2.0f dB')
plt.title('2. Spectrogram (Time-Frequency Domain)')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')

plt.tight_layout()
plt.show()

# 6. CNN 입력 형태로 확인 (Shape 체크)
print("--- 딥러닝 모델 입력 데이터 정보 ---")
print("Waveform shape (1D 데이터):", y.shape)
print("Spectrogram shape (2D 이미지 데이터):", spectrogram_db.shape)
print(f"=> 세로(Y축 주파수 빈 수): {spectrogram_db.shape[0]}, 가로(X축 시간 프레임 수): {spectrogram_db.shape[1]}")
```
