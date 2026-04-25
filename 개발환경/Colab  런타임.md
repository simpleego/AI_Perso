# Colab에서 선택 가능한 런타임 환경
> **Colab에서는 기본적으로 CPU, GPU(T4, L4, A100), TPU 런타임을 선택할 수 있으며, 런타임 버전은 최신 Python 및 주요 ML 프레임워크(PyTorch, TensorFlow, JAX 등)가 포함된 이미지로 제공됩니다.   
>  또한 과거 런타임 버전(예: 2026.04, 2026.01 등)을 선택해 호환성을 유지할 수도 있습니다. 

---

## 🔹 Colab에서 선택 가능한 런타임 유형
- **CPU (기본값)**  
  - 데이터 처리, 시각화, 소규모 ML 작업에 적합  
  - Pandas, NumPy, Matplotlib 등 CPU 기반 라이브러리 활용 시 충분

- **GPU**  
  - **T4 GPU**: 중간 규모 딥러닝/ML 작업에 적합  
  - **L4 GPU**: 복잡한 모델, 대규모 이미지 처리에 적합  
  - **A100 GPU**: 가장 강력, 대규모 딥러닝 모델 학습에 최적화  [drlee.io](https://drlee.io/choosing-the-right-colab-runtime-a-guide-for-data-scientists-and-analysts-57ee7b7c9638)

- **TPU**  
  - TensorFlow/JAX 기반 대규모 모델 학습에 최적화  
  - TPU 전용 런타임에서 TensorFlow 일부 기능 제한 있음

---

## 🔹 Colab 런타임 버전 (2026 기준)
Colab은 주기적으로 런타임 이미지를 업데이트하며, 과거 버전도 선택 가능:

| 버전 | OS | Python | 주요 라이브러리 |
|------|----|--------|----------------|
| **2026.04** | Ubuntu 22.04.5 LTS | Python 3.12.13 | NumPy 2.0.2, PyTorch 2.10.0, JAX 0.7.2, TensorFlow 2.19.0, R 4.5.3, Julia 1.11.5 |
| **2026.01** | Ubuntu 22.04.5 LTS | Python 3.12.12 | PyTorch 2.9.0, JAX 0.7.2, TensorFlow 2.19.0, R 4.5.2, Julia 1.11.5 |
| **2025.10** | Ubuntu 22.04.4 LTS | Python 3.12.12 | PyTorch 2.8.0, JAX 0.5.3, TensorFlow 2.19.0, R 4.5.1, Julia 1.11.5 |
| **2025.07** | Ubuntu 22.04.4 LTS | Python 3.11.13 | PyTorch 2.6.0, JAX 0.5.2, TensorFlow 2.18.0, R 4.5.1, Julia 1.10.9  [research.google.com](https://research.google.com/colaboratory/runtime-version-faq.html)

---

## 🔹 선택 시 고려사항
- **최신 버전 사용 권장**: 최신 라이브러리와 보안 업데이트 포함  
- **과거 버전 고정(pinning)**: 강의/워크숍 등에서 환경 안정성을 위해 사용 가능 (최대 1년간 유지)  
- **GPU/TPU 선택**: 딥러닝, 대규모 연산 시 GPU/TPU 활용 → 속도 크게 향상  
- **CPU 선택**: 데이터 전처리, 시각화 등에서는 GPU/TPU 불필요

---

👉 정리하면, Colab에서는 **CPU / GPU(T4, L4, A100) / TPU 런타임**을 선택할 수 있고, **런타임 버전은 최신(2026.04) 또는 과거 버전(2026.01, 2025.10 등)을 고정**할 수 있습니다.  
