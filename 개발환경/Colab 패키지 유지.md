#  Colab 패키지 유지
> Colab은 세션이 종료되면 설치했던 패키지가 모두 사라지기 때문에, **추가로 설치한 패키지를 지속적으로 유지하려면 몇 가지 방법을 써야 합니다.**

## 🔹 Colab에서 패키지 유지하는 방법
1. **노트북 시작 시 자동 설치 코드 추가**  
   - 필요한 패키지를 `!pip install` 명령어로 설치하는 셀을 맨 위에 두세요.  
   - 예:
     ```python
     !pip install transformers datasets sentencepiece
     ```
   - 이렇게 하면 런타임이 새로 시작될 때마다 자동으로 설치됩니다.

2. **requirements.txt 활용**  
   - 필요한 패키지를 `requirements.txt` 파일에 정리해두고, Colab에서 업로드 후 설치:
     ```python
     !pip install -r requirements.txt
     ```
   - 여러 패키지를 한 번에 관리할 수 있어 편리합니다.

3. **Google Drive 연동**  
   - 패키지 설치 스크립트나 requirements.txt를 Google Drive에 저장해두고, Colab에서 Drive를 마운트해 불러올 수 있습니다.
   - 예:
     ```python
     from google.colab import drive
     drive.mount('/content/drive')
     !pip install -r /content/drive/MyDrive/requirements.txt
     ```

4. **커스텀 Colab 환경 이미지 사용 (고급)**  
   - Colab Pro+에서는 Docker 기반 커스텀 환경을 만들 수 있습니다.  
   - 하지만 일반 사용자라면 위의 방법(설치 셀 추가, requirements.txt 관리)이 가장 실용적입니다.

---

👉 정리하면, Colab은 세션이 초기화되므로 **패키지를 영구적으로 유지할 수는 없고**, 대신 **노트북 시작 시 자동 설치 코드나 requirements.txt를 활용해 매번 설치하는 방식**으로 관리하는 것이 일반적입니다.  

혹시 원하시는 게, 제가 **자연어 처리용 기본 패키지 세트(Transformers, Datasets, SentencePiece 등)를 자동 설치하는 셀 예시**를 만들어드리는 걸까요?
