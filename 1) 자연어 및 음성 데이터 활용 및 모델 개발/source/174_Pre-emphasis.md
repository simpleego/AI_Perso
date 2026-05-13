### 2. 통합 실습 코드

이 코드에서는 **Pre-emphasis 전처리**를 적용하고, 전처리 전후의 지연시간(Latency)을 측정하며, 분류 모델의 평가 지표(F1-score)를 산출하는 과정을 실습합니다.

```python
import numpy as np
import time
from sklearn.metrics import classification_report, f1_score

# 1. Pre-emphasis 필터 구현 (image_80afdc.png 내용)
def pre_emphasis(signal, alpha=0.97):
    """
    고주파 성분을 강조하여 스펙트럼을 평탄화함
    """
    return np.append(signal[0], signal[1:] - alpha * signal[:-1])

# 2. 성능 및 지연시간 측정 실습 (image_80b7a2.png 내용)
def practical_evaluation_demo():
    # 가상의 음성 데이터 생성 (1초, 16kHz)
    sr = 16000
    sample_signal = np.random.uniform(-1, 1, sr)
    
    # 전처리 지연시간 측정
    start_time = time.time()
    emphasized_signal = pre_emphasis(sample_signal)
    end_time = time.time()
    
    latency_ms = (end_time - start_time) * 1000
    print(f"--- 전처리 단계 평가 ---")
    print(f"Pre-emphasis 실행 시간: {latency_ms:.4f} ms")
    
    # 3. 모델 평가 지표 산출 (image_80bfd9.png 내용)
    # 가상의 정답(y_true)과 예측값(y_pred) - 감정 분석 예시
    y_true = [0, 1, 2, 0, 1, 2] # 0:중립, 1:긍정, 2:부정
    y_pred = [0, 2, 2, 0, 1, 1]
    
    print("\n--- 모델 성능 평가 (분류/감정 분석) ---")
    # 단순 정확도 외 F1-Score 등 다각적 지표 확인
    report = classification_report(y_true, y_pred, 
                                   target_names=['Neutral', 'Positive', 'Negative'])
    print(report)
    
    f1 = f1_score(y_true, y_pred, average='weighted')
    print(f"최종 가중치 F1 점수: {f1:.4f}")

# 실습 실행
if __name__ == "__main__":
    practical_evaluation_demo()

```
