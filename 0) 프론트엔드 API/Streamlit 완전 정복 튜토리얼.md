# 📘 Streamlit 완전 정복 튜토리얼

> 데이터 앱을 빠르게 구축하는 Python 라이브러리, Streamlit

---

## 📂 섹션 1: Streamlit 소개 및 환경 설정

### 1.1 Streamlit이란? (15분)
- 데이터 과학자를 위한 가장 빠른 웹 앱 프레임워크
- 장점: Python만 알면 OK, 반응형, 코드 변경 시 자동 리로드

### 1.2 설치 및 첫 앱 실행 

```bash
# 가상환경 생성 (권장)
python -m venv streamlit_env
source streamlit_env/bin/activate  # Mac/Linux
streamlit_env\Scripts\activate     # Windows

# Streamlit 설치
pip install streamlit

# 버전 확인
streamlit --version
```

### 1.3 첫 번째 앱 만들기 

**app.py** 작성:
```python
import streamlit as st

st.title("나의 첫 Streamlit 앱 🎈")
st.write("안녕하세요, Streamlit 세계에 오신 것을 환영합니다!")

name = st.text_input("이름을 입력하세요:")
if name:
    st.success(f"반갑습니다, {name}님!")
```

실행:
```bash
streamlit run app.py
```

---

## 📂 섹션 2: 기본 위젯과 레이아웃 

### 2.1 텍스트 표시 함수

```python
import streamlit as st

st.title("대제목")
st.header("중간 제목")
st.subheader("소제목")
st.markdown("**마크다운** *지원*")
st.caption("작은 설명글")
st.code("print('Hello')", language="python")
st.divider()
st.latex(r"E = mc^2")
```

### 2.2 기본 입력 위젯

```python
import streamlit as st
from datetime import time, date

# 버튼
if st.button("클릭하세요"):
    st.write("버튼이 클릭되었습니다!")

# 체크박스
agree = st.checkbox("동의합니다")
if agree:
    st.write("감사합니다!")

# 라디오 버튼
option = st.radio("선호하는 색상:", ["빨강", "파랑", "초록"])

# 셀렉트 박스
choice = st.selectbox("과목 선택:", ["Python", "Streamlit", "Data Science"])

# 멀티셀렉트
subjects = st.multiselect("좋아하는 과목:", ["수학", "과학", "역사"])

# 슬라이더
age = st.slider("나이 선택:", 0, 100, 25)
value = st.slider("값 선택:", 0.0, 100.0, 50.0, step=0.5)

# 텍스트 입력
text = st.text_input("메시지를 입력하세요:", placeholder="여기에 입력...")

# 숫자 입력
number = st.number_input("숫자 입력:", min_value=0, max_value=100)

# 날짜/시간
date_val = st.date_input("날짜 선택:", date.today())
time_val = st.time_input("시간 선택:", time(9, 0))
```

### 2.3 레이아웃 구성 

```python
import streamlit as st

# 사이드바
with st.sidebar:
    st.header("설정")
    option = st.selectbox("테마 선택", ["라이트", "다크"])
    st.slider("볼륨", 0, 100, 50)

# 2컬럼 레이아웃
col1, col2 = st.columns(2)
with col1:
    st.metric("온도", "22°C", "1.2°C")
with col2:
    st.metric("습도", "55%", "-5%")

# 3컬럼
col1, col2, col3 = st.columns([1, 2, 1])  # 비율 지정
col1.button("버튼1")
col2.button("버튼2")
col3.button("버튼3")

# 탭
tab1, tab2, tab3 = st.tabs(["차트", "데이터", "설정"])
with tab1:
    st.line_chart([1, 2, 3, 4])
with tab2:
    st.dataframe({"A": [1, 2, 3], "B": [4, 5, 6]})
with tab3:
    st.checkbox("옵션 표시")

# 확장 가능 섹션
with st.expander("자세히 보기"):
    st.write("이 내용은 접었다 펼 수 있습니다.")
```

### 2.4 실습 미니 과제 (연습)
- 자기소개 페이지 만들기 (사이드바에 프로필 정보, 메인에 자기소개)

---

## 📂 섹션 3: 데이터 시각화 및 표시 

### 3.1 데이터프레임 표시 

```python
import streamlit as st
import pandas as pd
import numpy as np

# 데이터 생성
df = pd.DataFrame({
    '이름': ['Alice', 'Bob', 'Charlie'],
    '나이': [25, 30, 35],
    '도시': ['서울', '부산', '대구']
})

# 표시 방법 비교
st.dataframe(df)              # 인터랙티브
st.table(df)                  # 정적 테이블
st.metric("평균 나이", df['나이'].mean())

# 대용량 데이터 (1000행)
big_df = pd.DataFrame(np.random.randn(1000, 5), columns=['A', 'B', 'C', 'D', 'E'])
st.dataframe(big_df, use_container_width=True)

# 스타일링
styled_df = df.style.highlight_max(axis=0)
st.dataframe(styled_df)
```

### 3.2 차트 그리기 

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 샘플 데이터
df = pd.DataFrame({
    '날짜': pd.date_range('2024-01-01', periods=100),
    '값': np.random.randn(100).cumsum(),
    '카테고리': np.random.choice(['A', 'B', 'C'], 100)
})

# 기본 차트
st.line_chart(df, x='날짜', y='값')
st.area_chart(df, x='날짜', y='값')
st.bar_chart(df.groupby('카테고리')['값'].sum())

# 산점도
st.scatter_chart(df, x='날짜', y='값', color='카테고리')

# Matplotlib
fig, ax = plt.subplots()
ax.plot(df['날짜'], df['값'])
ax.set_title("Matplotlib 예제")
st.pyplot(fig)

# Seaborn
fig, ax = plt.subplots()
sns.histplot(df['값'], kde=True, ax=ax)
st.pyplot(fig)

# Plotly (인터랙티브)
fig = px.line(df, x='날짜', y='값', title='Plotly 차트')
st.plotly_chart(fig)

# Vega-Lite
vega_data = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 20, 30, 40]
})
st.vega_lite_chart(vega_data, {
    'mark': 'bar',
    'encoding': {
        'x': {'field': 'x', 'type': 'quantitative'},
        'y': {'field': 'y', 'type': 'quantitative'}
    }
})
```

### 3.3 지도 시각화 

```python
import streamlit as st
import pandas as pd
import pydeck as pdk

# 지도 데이터
map_data = pd.DataFrame({
    'lat': [37.5665, 37.5660, 37.5670],
    'lon': [126.9780, 126.9775, 126.9785],
    'size': [100, 200, 300]
})

st.map(map_data, latitude='lat', longitude='lon', size='size')

# PyDeck (고급)
layer = pdk.Layer(
    'ScatterplotLayer',
    data=map_data,
    get_position='[lon, lat]',
    get_radius='size',
    get_fill_color='[200, 30, 0, 160]'
)

view_state = pdk.ViewState(
    latitude=37.5665,
    longitude=126.9780,
    zoom=12
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
```

### 3.4 실습 (데이터 대시보드)
- 타이타닉 데이터셋을 불러와 탐색적 대시보드 만들기

---

## 📂 섹션 4: 고급 위젯 및 상태 관리 

### 4.1 세션 상태 (Session State)

```python
import streamlit as st

# 기본 상태 저장
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment():
    st.session_state.count += 1

st.write(f"카운트: {st.session_state.count}")
st.button("증가", on_click=increment)

# 폼 상태 유지
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

with st.form("user_form"):
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=0)
    submitted = st.form_submit_button("저장")
    
    if submitted:
        st.session_state.form_data['name'] = name
        st.session_state.form_data['age'] = age
        st.success("저장되었습니다!")

# 위젯 콜백
def update_value():
    st.session_state.slider_value = st.session_state.slider

st.slider(
    "값 선택", 
    0, 100, 
    key="slider",
    on_change=update_value
)
```

### 4.2 고급 위젯

```python
import streamlit as st

# 색상 선택기
color = st.color_picker("색상 선택", "#00f900")
st.write(f"선택한 색상: {color}")

# 파일 업로더 (기본)
file = st.file_uploader("파일 업로드", type=['csv', 'txt', 'json'])

# 프로그레스 바
import time
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

# 상태 메시지
with st.spinner("로딩 중..."):
    time.sleep(2)
st.success("완료!")
st.error("에러 발생")
st.warning("경고")
st.info("정보")

# 폼 (여러 입력 한번에 제출)
with st.form("my_form"):
    st.write("폼 내부")
    name = st.text_input("이름")
    age = st.number_input("나이")
    submit = st.form_submit_button("제출")
    if submit:
        st.write(f"{name}, {age}세")

# 팝오버
with st.popover("클릭하세요"):
    st.write("팝오버 내용")

# 1. 상태 컨테이너 생성 (접힌 상태로 시작)
with st.status("데이터를 분석하고 있습니다...", expanded=False) as status:
    st.write("데이터 로드 중...")
    time.sleep(2)
    st.write("복잡한 계산 수행 중...")
    time.sleep(2)
    st.write("결과 정리 중...")
    
    # 2. 작업 완료 시 상태 업데이트
    status.update(label="분석 완료!", state="complete", expanded=False)

st.button("다시 실행")
```

### 4.3 페이지 구성 및 네비게이션

```python
# pages/01_데이터_분석.py
import streamlit as st

st.set_page_config(
    page_title="데이터 분석",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 여러 페이지 앱 구조
# 프로젝트 폴더/
#   app.py (홈)
#   pages/
#       01_분석.py
#       02_시각화.py
#       03_설정.py
```

### 4.4 실습 (쇼핑 카트 앱)
- 세션 상태로 카트 아이템 추가/삭제 기능 구현

---

## 📂 섹션 5: 미디어, 파일 업로드, 캐싱

### 5.1 미디어 표시

```python
import streamlit as st
from PIL import Image
import io

# 이미지
image = Image.open("sample.jpg")  # 또는 URL
st.image(image, caption="샘플 이미지", width=300)

# 비디오
video_file = open("sample.mp4", "rb")
video_bytes = video_file.read()
st.video(video_bytes)

# 오디오
audio_file = open("sample.mp3", "rb")
audio_bytes = audio_file.read()
st.audio(audio_bytes)

# HTML/iframe
st.components.v1.html(
    "<iframe width='560' height='315' src='https://www.youtube.com/embed/...'></iframe>",
    height=315
)
```

### 5.2 파일 업로드 및 처리

```python
import streamlit as st
import pandas as pd
import json

# CSV 업로드
uploaded_file = st.file_uploader("CSV 업로드", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
    
    # 다운로드 버튼
    csv = df.to_csv(index=False)
    st.download_button(
        label="CSV 다운로드",
        data=csv,
        file_name="output.csv",
        mime="text/csv"
    )

# 여러 파일
files = st.file_uploader("여러 파일 선택", accept_multiple_files=True)
for file in files:
    st.write(file.name)

# 이미지 업로드
img_file = st.file_uploader("이미지 업로드", type=['png', 'jpg', 'jpeg'])
if img_file:
    image = Image.open(img_file)
    st.image(image, caption="업로드된 이미지")
```

### 5.3 캐싱

```python
import streamlit as st
import pandas as pd
import time

# 기본 캐시
@st.cache_data
def load_data():
    # 무거운 연산 (DB 조회, 파일 로드 등)
    time.sleep(2)  # 시뮬레이션
    return pd.DataFrame({'A': range(100), 'B': range(100)})

df = load_data()  # 첫 실행만 느림, 이후는 캐시
st.dataframe(df)

# 캐시 무효화
@st.cache_data(ttl=3600)  # 1시간 후 만료
def get_dynamic_data():
    return pd.DataFrame(...)

# 리소스 캐싱
@st.cache_resource
def init_model():
    # 머신러닝 모델 로드 등
    return "모델 객체"

# 캐시 초기화 버튼
if st.button("캐시 초기화"):
    st.cache_data.clear()
    st.success("캐시가 초기화되었습니다!")

# 부분 캐싱
@st.cache_data
def expensive_computation(x, y):
    time.sleep(1)
    return x + y

result = expensive_computation(10, 20)
```

### 5.4 실습 (이미지 필터 앱)
- 이미지 업로드 → 필터 적용 (흑백, 블러 등) → 결과 다운로드

---

## 📂 섹션 6: 실전 프로젝트

### 프로젝트 1: 날씨 대시보드

```python
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="날씨 대시보드", layout="wide")

st.title("🌤️ 실시간 날씨 대시보드")

# 사이드바
with st.sidebar:
    st.header("설정")
    city = st.text_input("도시 이름 (영문)", "Seoul")
    api_key = st.text_input("OpenWeatherMap API 키", type="password")
    
    if st.button("날씨 정보 가져오기"):
        if api_key and city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🌡️ 온도", f"{data['main']['temp']}°C")
                with col2:
                    st.metric("💧 습도", f"{data['main']['humidity']}%")
                with col3:
                    st.metric("💨 풍속", f"{data['wind']['speed']} m/s")
                
                st.subheader(f"{city}의 날씨")
                st.write(f"상태: {data['weather'][0]['description']}")
                st.image(f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
            else:
                st.error("도시를 찾을 수 없습니다.")
```

### 프로젝트 2: CSV 분석기

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

st.title("📊 CSV 데이터 분석기")

uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 기본 정보 탭
    tab1, tab2, tab3, tab4 = st.tabs(["데이터 미리보기", "통계", "시각화", "프로파일링"])
    
    with tab1:
        st.dataframe(df.head(100))
        st.write(f"행: {df.shape[0]}, 열: {df.shape[1]}")
    
    with tab2:
        st.dataframe(df.describe())
        
        # 결측치
        missing = df.isnull().sum()
        st.bar_chart(missing[missing > 0])
    
    with tab3:
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        x_axis = st.selectbox("X축", numeric_cols)
        y_axis = st.selectbox("Y축", numeric_cols)
        
        fig = px.scatter(df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)
    
    with tab4:
        # 프로파일링 리포트
        profile = ProfileReport(df, explorative=True)
        st_profile_report(profile)
```

### 프로젝트 3: 간단한 ML 앱

```python
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.title("🤖 머신러닝 분류기")

# 데이터 생성 또는 업로드
option = st.radio("데이터 소스", ["샘플 데이터", "CSV 업로드"])

if option == "샘플 데이터":
    from sklearn.datasets import load_iris
    data = load_iris()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data.target
    target_names = data.target_names
else:
    uploaded = st.file_uploader("CSV 업로드", type=['csv'])
    if uploaded:
        df = pd.read_csv(uploaded)
        target_col = st.selectbox("타겟 열 선택", df.columns)
        target_names = df[target_col].unique()

if 'df' in locals():
    # 특성 선택
    feature_cols = st.multiselect("특성 선택", [c for c in df.columns if c != 'target'])
    
    if feature_cols:
        X = df[feature_cols]
        y = df['target']
        
        # 학습 파라미터
        test_size = st.slider("테스트 비율", 0.1, 0.4, 0.2)
        n_estimators = st.slider("트리 개수", 10, 200, 100)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        
        model = RandomForestClassifier(n_estimators=n_estimators)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        st.metric("정확도", f"{acc:.2%}")
        
        # 예측 섹션
        st.subheader("새로운 데이터 예측")
        input_data = []
        for col in feature_cols:
            val = st.number_input(f"{col}", value=float(X[col].mean()))
            input_data.append(val)
        
        if st.button("예측"):
            pred = model.predict([input_data])[0]
            st.success(f"예측 결과: {target_names[pred]}")
```

---

## 📚 추가 학습 자료

### 공식 문서
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Gallery](https://streamlit.io/gallery) - 실제 앱 예제
- [Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)

### 추천 확장 기능
```bash
pip install streamlit-aggrid      # 고급 테이블
pip install streamlit-option-menu # 메뉴 컴포넌트
pip install streamlit-lottie      # 애니메이션
pip install streamlit-authenticator # 로그인
```

### 배포 방법
```bash
# Streamlit Cloud (무료)
1. GitHub에 코드 업로드
2. share.streamlit.io 에서 연결

# Docker
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

