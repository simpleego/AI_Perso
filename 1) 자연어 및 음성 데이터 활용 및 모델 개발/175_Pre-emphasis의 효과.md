
## 2. 통합 실습 및 시각화 코드

이미지에 제시된 파이썬 구현 예시를 바탕으로, 실제로 음성 신호가 어떻게 변하는지 그래프로 확인할 수 있는 코드를 작성했습니다.

```python
import numpy as np
import matplotlib.pyplot as plt

def pre_emphasis(signal, alpha=0.95):
    """
    이미지(image_804add.png)에 제시된 구현 방식
    """
    return np.append(signal[0], signal[1:] - alpha * signal[:-1])

# 1. 가상의 음성 신호 생성 (저주파 성분이 강한 신호)
fs = 16000
t = np.linspace(0, 0.5, fs // 2)
# 저주파(500Hz)와 고주파(5000Hz)가 섞인 신호 (고주파는 에너지가 작음)
signal = np.sin(2 * np.pi * 500 * t) + 0.1 * np.sin(2 * np.pi * 5000 * t)

# 2. Pre-emphasis 적용
emphasized_signal = pre_emphasis(signal, alpha=0.95)

# 3. 시각화 (효과 확인)
plt.figure(figsize=(12, 6))

# 원본 신호 스펙트럼
plt.subplot(1, 2, 1)
plt.magnitude_spectrum(signal, Fs=fs, color='C1')
plt.title("Original Spectrum (Before)")
plt.ylim(0, 0.6)

# Pre-emphasis 적용 후 스펙트럼
plt.subplot(1, 2, 2)
plt.magnitude_spectrum(emphasized_signal, Fs=fs, color='C2')
plt.title("Emphasized Spectrum (After)")
plt.ylim(0, 0.6)

plt.tight_layout()
plt.show()

print("이미지 설명대로 고주파 대역의 에너지가 보상되어 스펙트럼이 평탄화되었습니다.")

```