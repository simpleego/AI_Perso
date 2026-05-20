```python
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import scipy.fftpack as fftpack

# ==========================================
# PART 1: MFCC 추출 실습 (6단계 과정)
# ==========================================

print("=== [PART 1] MFCC 추출 6단계 실습 시작 ===")

# 1. 오디오 파일 로드 및 전처리
y, sr = librosa.load(librosa.example('nutcracker'), duration=3.0)
n_fft = 512
hop_length = 160
win_length = 400  # 25ms 프레임 크기 (16kHz 기준 대략적인 표준 규격 설정)

# 2. 프레임 분할 및 창 함수 적용
# librosa.util.frame을 통해 수동 분할 후 Hann 윈도우 적용 시뮬레이션
frames = librosa.util.frame(y, frame_length=win_length, hop_length=hop_length)
window = np.hanning(win_length)[:, np.newaxis]
windowed_frames = frames * window

# 3. FFT 및 파워 스펙트럼 계산
# 각 프레임별 FFT 수행 후 제곱하여 파워 스펙트럼 도출
fft_frames = np.fft.rfft(windowed_frames, n_fft, axis=0)
power_spectrum = np.abs(fft_frames) ** 2

# 4. 멜 필터뱅크 적용
# 주파수 축을 멜 스케일 공간으로 매핑하기 위한 행렬 곱 연산
n_mels = 40
mel_basis = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels)
mel_spectrogram = np.dot(mel_basis, power_spectrum)

# 5. 로그 변환 및 DCT 적용
# 인간의 대수적 소리 크기 인지 반영 및 성분 간 상관관계 제거(De-correlation)
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
n_mfcc = 13
mfcc_manual = fftpack.dct(log_mel_spectrogram, type=2, axis=0, norm='ortho')[:n_mfcc]

# 6. MFCC 추출 및 시각화 (도출된 최종 결과값 검증 플롯)
plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
librosa.display.specshow(log_mel_spectrogram, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
plt.title('Step 5 & 6: Log-Mel Spectrogram')
plt.colorbar(format='%+2.0f dB')

plt.subplot(3, 1, 2)
librosa.display.specshow(mfcc_manual, sr=sr, hop_length=hop_length, x_axis='time')
plt.title('Step 6: Final Extracted MFCC Coefficients')
plt.colorbar()


# ==========================================
# PART 2: VAD 적용 실습 (6단계 과정)
# ==========================================

print("\n=== [PART 2] VAD 적용 6단계 실습 시작 ===")

# 1. 에너지 기반 VAD 구현
# 각 프레임별 RMS(Root Mean Square) 에너지를 계산하여 임계값 기준으로 1과 0 판정
rms_energy = librosa.feature.rms(y=y, frame_length=win_length, hop_length=hop_length)[0]
energy_threshold = np.mean(rms_energy) * 0.6
vad_energy = (rms_energy > energy_threshold).astype(int)

# 2. 스펙트럼 기반 VAD 구현
# 스펙트럼 센트로이드(중심주파수)의 변동성을 추적하여 유효 성분 판정 시뮬레이션
spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)[0]
centroid_threshold = np.median(spectral_centroids) * 0.7
vad_spectral = (spectral_centroids > centroid_threshold).astype(int)

# 3. WebRTC VAD 라이브러리 활용 관점의 의사 구현 (통계적 무음 판정 대체)
# 외부 바이너리 종속성 배제를 위해 스펙트럼 서브밴드 에너지를 다변수 조건으로 결합한 통계적 로직으로 대체 구현
spectral_flatness = librosa.feature.spectral_flatness(y=y, n_fft=n_fft, hop_length=hop_length)[0]
vad_webrtc_sim = ((rms_energy > energy_threshold * 0.8) & (spectral_flatness < np.mean(spectral_flatness) * 1.2)).astype(int)

# 4. 음성/비음성 구간 시각화
# 오디오의 시간축 공간과 해상도를 일치시켜 프레임 단위 마스크를 시간 스탬프로 맵핑
times_wave = np.linspace(0, len(y) / sr, len(y))
times_frame = librosa.frames_to_time(np.arange(len(vad_energy)), sr=sr, hop_length=hop_length)

plt.subplot(3, 1, 3)
plt.plot(times_wave, y, label='Original Waveform', color='gray', alpha=0.6)
plt.plot(times_frame, vad_energy * np.max(y), label='Energy-VAD Mask', color='r', linestyle='--')
plt.plot(times_frame, vad_webrtc_sim * np.max(y) * 0.8, label='WebRTC-Sim Mask', color='b')
plt.title('Step 4: Voice Activity Detection (VAD) Overlay Visualization')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# 5. 구간별 오디오 분리 저장
# VAD 마스크가 1인 프레임만 추려내어 유효 음성 신호로 병합 복원
voice_frames = frames[:, vad_energy == 1]
# 분할되었던 프레임을 다시 하나의 연속된 시계열 신호로 복원 (Overlap-Add 처리 방식 적용)
y_voice_only = voice_frames.flatten()[:len(y)] # 시뮬레이션을 위한 선형 병합 처리
print(f"-> 5. 구간별 오디오 분리 완료 (원본 샘플 수: {len(y)} -> 정제 후 샘플 수: {len(y_voice_only[y_voice_only != 0])})")

# 6. VAD 성능 평가
# 임의의 기준 마스크(스펙트럼 VAD)를 정답(Ground Truth)으로 가정하고 에너지 VAD와의 일치도 지표 산출
ground_truth = vad_spectral
prediction = vad_energy

tp = np.sum((ground_truth == 1) & (prediction == 1))
fp = np.sum((ground_truth == 0) & (prediction == 1))
fn = np.sum((ground_truth == 1) & (prediction == 0))

precision = tp / (tp + fp + 1e-10)
recall = tp / (tp + fn + 1e-10)
f1_score = 2 * (precision * recall) / (precision + recall + 1e-10)

print("\n" + "="*50)
print(" [VAD 알고리즘 성능 평가 지표 (Step 6)] ")
print("="*50)
print(f"▣ 정밀도 (Precision) : {precision:.4f}")
print(f"▣ 재현율 (Recall)    : {recall:.4f}")
print(f"▣ F1-Score           : {f1_score:.4f}")
print("="*50)

```
