# CUDA
>  Google Colab은 **CUDA를 지원하므로 PC에서 지원하지 않는 GPU기능을 사용할 수 있다.
> 참고로 CUDA(compute Unified Device Architecture)는 NVIDIA 그래픽 카드만 지원합니다.
### 🔹 Colab에서 CUDA 사용 방법
1. **GPU 활성화하기**  
   - 메뉴에서 `런타임 → 런타임 유형 변경 → 하드웨어 가속기 → GPU` 선택  
   - 저장 후 런타임을 다시 시작하면 GPU가 할당됩니다.

2. **CUDA 버전 확인하기**  
   ```python
   !nvidia-smi
   ```
   이 명령어로 현재 할당된 GPU 모델과 CUDA 드라이버 버전을 확인할 수 있습니다.

3. **PyTorch / TensorFlow에서 GPU 사용 확인**  
   - PyTorch:
     ```python
     import torch
     print(torch.cuda.is_available())
     print(torch.cuda.get_device_name(0))
     ```
   - TensorFlow:
     ```python
     import tensorflow as tf
     print(tf.config.list_physical_devices('GPU'))
     ```

4. **주의할 점**  
   - 무료 Colab은 GPU 사용 시간이 제한되어 있습니다.  
   - CUDA 버전은 Colab 환경 업데이트에 따라 달라질 수 있습니다.  
   - 특정 라이브러리와 CUDA 버전이 맞지 않으면 직접 설치해야 할 수도 있습니다.
