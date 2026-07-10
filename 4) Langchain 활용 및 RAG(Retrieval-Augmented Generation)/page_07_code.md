```bash
# 가상환경 생성 (conda 사용 시)
conda create -n langchain python=3.10
conda activate langchain


# 또는 venv 사용 시
python -m venv langchain_env

# macOS / Linux
source langchain_env/bin/activate

# Windows
langchain_env\Scripts\activate


# 필수 라이브러리 설치
pip install langchain openai chromadb faiss-cpu
```
