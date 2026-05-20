```python
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import scipy.fftpack as fftpack
import soundfile as sf

# ==========================================
# PART 1: MFCC 추출 실습 (6단계 과정)
# ==========================================

print("=== [PART 1] MFCC 추출 6단계 실습 시작 ===")

# 1. 오디오 파일 로드 및 전처리
y, sr = librosa.load('1_0000.wav', duration=3.0)
n_fft = 512
hop_length = 160
win_length = 400  # 25ms

# 사운드 출력
sf.write('nutcracker.wav', y, sr)

# 2. 프레임 분할 및 창 함수 적용
frames = librosa.util.frame(y, frame_length=win_length, hop_length=hop_length)
window = np.hanning(win_length)[:, np.newaxis]
windowed_frames = frames * window

# 3. FFT 및 파워 스펙트럼 계산
fft_frames = np.fft.rfft(windowed_frames, n_fft, axis=0)
power_spectrum = np.abs(fft_frames) ** 2

# 4. 멜 필터뱅크 적용
n_mels = 40
mel_basis = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels)
mel_spectrogram = np.dot(mel_basis, power_spectrum)

# 5. 로그 변환 및 DCT 적용
log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
n_mfcc = 13
mfcc_manual = fftpack.dct(log_mel_spectrogram, type=2, axis=0, norm='ortho')[:n_mfcc]

# 6. MFCC 시각화
plt.figure(figsize=(12, 10))
plt.subplot(3, 1, 1)
librosa.display.specshow(log_mel_spectrogram, sr=sr, hop_length=hop_length,
                         x_axis='time', y_axis='mel')
plt.title('Step 5 & 6: Log-Mel Spectrogram')
plt.colorbar(format='%+2.0f dB')

plt.subplot(3, 1, 2)
librosa.display.specshow(mfcc_manual, sr=sr, hop_length=hop_length, x_axis='time')
plt.title('Step 6: Final Extracted MFCC Coefficients')
plt.colorbar()
plt.show()

# ==========================================
# PART 2: VAD 적용 실습 (6단계 과정)
# ==========================================

print("\n=== [PART 2] VAD 적용 6단계 실습 시작 ===")

# 1. 에너지 기반 VAD
rms_energy = librosa.feature.rms(
    y=y, frame_length=win_length, hop_length=hop_length
)[0]
energy_threshold = np.mean(rms_energy) * 0.6
vad_energy = (rms_energy > energy_threshold).astype(int)

# 2. 스펙트럼 기반 VAD
spectral_centroids = librosa.feature.spectral_centroid(
    y=y, sr=sr, n_fft=n_fft, hop_length=hop_length, center=False
)[0]

# 3. WebRTC 유사 VAD
spectral_flatness = librosa.feature.spectral_flatness(
    y=y, n_fft=n_fft, hop_length=hop_length,
    win_length=win_length, center=False
)[0]

# ==========================================
# 🔧 1차 동기화: feature 길이 통일
# ==========================================
min_len = min(len(rms_energy), len(spectral_centroids), len(spectral_flatness))

rms_energy = rms_energy[:min_len]
spectral_centroids = spectral_centroids[:min_len]
spectral_flatness = spectral_flatness[:min_len]
vad_energy = vad_energy[:min_len]

# VAD 계산
centroid_threshold = np.median(spectral_centroids) * 0.7
vad_spectral = (spectral_centroids > centroid_threshold).astype(int)

vad_webrtc_sim = ((rms_energy > energy_threshold * 0.8) &
                  (spectral_flatness < np.mean(spectral_flatness) * 1.2)).astype(int)

# ==========================================
# 🔧 2차 동기화: frames.shape[1]에 맞추기
# ==========================================
frame_count = frames.shape[1]

def sync_to_frames(arr, frame_count):
    if len(arr) > frame_count:
        return arr[:frame_count]
    elif len(arr) < frame_count:
        pad = np.zeros(frame_count - len(arr), dtype=int)
        return np.concatenate([arr, pad])
    return arr

vad_energy = sync_to_frames(vad_energy, frame_count)
vad_spectral = sync_to_frames(vad_spectral, frame_count)
vad_webrtc_sim = sync_to_frames(vad_webrtc_sim, frame_count)

# ==========================================
# 4. 음성/비음성 구간 시각화
# ==========================================
times_wave = np.linspace(0, len(y) / sr, len(y))
times_frame = librosa.frames_to_time(np.arange(frame_count), sr=sr,
                                     hop_length=hop_length)

plt.subplot(3, 1, 3)
plt.plot(times_wave, y, label='Original Waveform', color='gray', alpha=0.6)
plt.plot(times_frame, vad_energy * np.max(y), label='Energy-VAD Mask',
         color='r', linestyle='--')
plt.plot(times_frame, vad_webrtc_sim * np.max(y) * 0.8,
         label='WebRTC-Sim Mask', color='b')
plt.title('Step 4: Voice Activity Detection (VAD) Overlay Visualization')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# ==========================================
# 5. 구간별 오디오 분리 저장
# ==========================================
voice_frames = frames[:, vad_energy == 1]
y_voice_only = voice_frames.flatten()[:len(y)]
print(f"-> 5. 구간별 오디오 분리 완료 (원본 샘플 수: {len(y)} -> 정제 후 샘플 수: {len(y_voice_only[y_voice_only != 0])})")

# ==========================================
# 6. VAD 성능 평가
# ==========================================
tp = np.sum((vad_spectral == 1) & (vad_energy == 1))
fp = np.sum((vad_spectral == 0) & (vad_energy == 1))
fn = np.sum((vad_spectral == 1) & (vad_energy == 0))

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
