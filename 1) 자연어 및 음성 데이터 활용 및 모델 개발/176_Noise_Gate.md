## 2. 실습 코드 (Python)

`image_8046a3.png`의 작동 원리를 파이썬으로 구현하여, 특정 크기 이하의 잡음을 제거하는 과정을 확인해 보겠습니다.

```python
import numpy as np
import matplotlib.pyplot as plt

def apply_noise_gate(signal, threshold, beta=0.0):
    """
    노이즈 게이트 알고리즘 구현 (image_8046a3.png 수식 기반)
    """
    output_signal = np.where(np.abs(signal) >= threshold, 
                             signal, 
                             beta * signal)
    return output_signal

# 1. 테스트용 신호 생성 (음성 신호 + 작은 잡음 가정)
fs = 1000
t = np.linspace(0, 1, fs)
# 음성 구간(큰 신호)과 잡음 구간(작은 신호)이 섞인 형태
voice = np.where(np.sin(2 * np.pi * 5 * t) > 0.5, 0.8 * np.sin(2 * np.pi * 50 * t), 0)
noise = 0.1 * np.random.normal(0, 1, fs)
signal = voice + noise

# 2. 노이즈 게이트 적용
threshold_val = 0.25 # 잡음보다 크고 음성보다 작은 임계값 설정
processed_signal = apply_noise_gate(signal, threshold=threshold_val, beta=0.0)

# 3. 결과 시각화
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, signal, color='gray', alpha=0.5, label='Original (Signal + Noise)')
plt.axhline(y=threshold_val, color='r', linestyle='--', label='Threshold')
plt.axhline(y=-threshold_val, color='r', linestyle='--')
plt.title("Before Noise Gate")
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, processed_signal, color='blue', label='After Noise Gate')
plt.title("After Noise Gate (Noise Suppressed)")
plt.legend()

plt.tight_layout()
plt.show()

```