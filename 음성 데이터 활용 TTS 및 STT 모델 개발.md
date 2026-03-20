# 음성 데이터 활용 TTS 및 STT 모델 개발

##  TTS 및 STT 간단한 실습

TTS/STT를 **최대한 간단하게 실습 수준으로 구현**하려면, 한국어 성능이 좋은 검증된 라이브러리를 쓰는 게 핵심입니다.
여기서는 다음 조합이 가장 간단하면서도 실용적입니다:

* STT: OpenAI Whisper (한국어 인식 매우 우수)
* TTS: gTTS (간단하고 한국어 자연스러움)

---

# 1️⃣ 사전 설치

```bash
pip install openai-whisper gTTS sounddevice scipy
```

※ Whisper는 내부적으로 ffmpeg 필요
👉 Windows: ffmpeg 설치 후 PATH 추가

---

# 2️⃣ STT (음성 → 텍스트)

마이크 입력을 받아 한국어로 변환

```python
import whisper
import sounddevice as sd
from scipy.io.wavfile import write

# 1. 음성 녹음
duration = 5  # 녹음 시간 (초)
fs = 16000

print("녹음 시작...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
write("input.wav", fs, recording)
print("녹음 완료")

# 2. Whisper 모델 로드
model = whisper.load_model("base")  # small, medium도 가능

# 3. 음성 → 텍스트
result = model.transcribe("input.wav", language="ko")

print("인식 결과:", result["text"])
```

✔ 특징

* 한국어 인식 정확도 높음
* 별도 API 없이 로컬 실행 가능

---

# 3️⃣ TTS (텍스트 → 음성)

```python
from gtts import gTTS
import os

text = "안녕하세요. TTS 테스트입니다."

# 1. TTS 생성
tts = gTTS(text=text, lang='ko')

# 2. 파일 저장
tts.save("output.mp3")

# 3. 재생 (Windows)
os.system("start output.mp3")
```

✔ 특징

* 코드 매우 간단
* 한국어 자연스러움 준수

---

# 4️⃣ STT + TTS 통합 (간단 데모)

```python
import whisper
from gtts import gTTS
import sounddevice as sd
from scipy.io.wavfile import write
import os

# 녹음
fs = 16000
duration = 5

print("말해주세요...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
write("input.wav", fs, recording)

# STT
model = whisper.load_model("base")
result = model.transcribe("input.wav", language="ko")
text = result["text"]

print("인식된 텍스트:", text)

# TTS
tts = gTTS(text=text, lang='ko')
tts.save("output.mp3")

# 재생
os.system("start output.mp3")
```

---

# 5️⃣ 실습 포인트 (교육용 핵심)

이 코드는 다음 개념을 학습시키기에 적합합니다:

* 음성 데이터 수집 (Sampling, WAV 저장)
* STT 파이프라인 (Audio → Text)
* TTS 파이프라인 (Text → Audio)
* end-to-end 음성 인터페이스

---

# 6️⃣ 한계 및 확장 방향

간단 구현이기 때문에:

* Whisper → GPU 사용 시 속도 개선 가능
* gTTS → 커스터마이징 제한
* 실시간 처리 → 스트리밍 구조 필요

👉 확장 추천:

* STT: Whisper streaming / Vosk
* TTS: Tacotron2, FastSpeech, VITS

---

원하면 다음 단계로
👉 “실시간 음성 챗봇 (마이크 → GPT → 음성 출력)” 구조까지 확장 코드도 만들어줄게.
