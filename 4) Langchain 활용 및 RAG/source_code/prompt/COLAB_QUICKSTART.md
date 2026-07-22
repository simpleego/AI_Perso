# Google Colab 빠른 실행

## 방법 1: ZIP 파일 업로드

1. Colab 왼쪽의 파일 아이콘을 누릅니다.
2. `langchain_prompt_gemini_practice.zip`을 업로드합니다.
3. 다음 셀을 실행합니다.

```python
!unzip -q langchain_prompt_gemini_practice.zip
%cd langchain_prompt_gemini_practice
!pip install -q -r requirements.txt
```

## API 키 설정

Colab의 비밀 키 기능을 사용하는 방법이 안전합니다.

1. 왼쪽 메뉴에서 열쇠 아이콘을 선택합니다.
2. 이름을 `GOOGLE_API_KEY`로 지정합니다.
3. Gemini API 키를 값으로 저장합니다.
4. 노트북 액세스를 허용합니다.

```python
from google.colab import userdata
import os

os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL"] = "gemini-2.5-flash-lite"
os.environ["GEMINI_EMBEDDING_MODEL"] = "gemini-embedding-001"
```

## 실행

```python
!python 00_environment_check.py
!python 01_1_3_0_prompt_overview/01_prompt_template_basic.py
!python 01_1_3_0_prompt_overview/02_chat_prompt_chain.py
```

Few-shot 동적 선택 예제:

```python
!python 05_1_3_4_few_shot_prompt/04_semantic_example_selector.py
!python 05_1_3_4_few_shot_prompt/06_dynamic_few_shot_chat.py
```

## 학습 권장 순서

각 폴더를 `01 → 02 → 03 → 04 → 05 → 06` 순서로 진행합니다. 각 폴더 안에서도 파일 번호 순서대로 실행합니다.
