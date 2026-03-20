## 1. TTS (Text-to-Speech) 구현
글자를 음성으로 변환하는 실습입니다. Google의 `gTTS` 라이브러리를 사용하면 매우 간단하게 구현할 수 있습니다.

**필요 라이브러리 설치:**
```bash
pip install gTTS playsound
```

**Python 코드:**
```python
from gtts import gTTS
import os

def text_to_speech(text, lang='ko'):
    # TTS 객체 생성 (한국어 설정)
    tts = gTTS(text=text, lang=lang)
    
    # 음성 파일 저장
    filename = "announcement.mp3"
    tts.save(filename)
    
    print(f"음성 파일이 '{filename}'으로 저장되었습니다.")
    # 실행 환경이 윈도우라면 파일을 바로 재생할 수 있습니다.
    # os.system(f"start {filename}") 

text_to_speech("안녕하세요, AI 휴먼 과정 TTS 실습 중입니다.")
```

---

## 2. STT (Speech-to-Text) 구현
음성을 인식하여 텍스트로 변환하는 실습입니다. `SpeechRecognition` 라이브러리를 활용하며, 마이크 입력이나 오디오 파일을 텍스트로 바꿀 수 있습니다.

**필요 라이브러리 설치:**
```bash
pip install SpeechRecognition PyAudio
```

**Python 코드:**
```python
import speech_recognition as sr

def speech_to_text():
    # 인식기 객체 생성
    recognizer = sr.Recognizer()
    
    # 마이크로부터 음성 듣기
    with sr.Microphone() as source:
        print("말씀해 주세요... (인식 중)")
        audio = recognizer.listen(source)
        
    try:
        # Google Web Speech API를 사용하여 텍스트로 변환
        text = recognizer.recognize_google(audio, language='ko-KR')
        print("인식된 내용: " + text)
    except sr.UnknownValueError:
        print("음성을 인식하지 못했습니다.")
    except sr.RequestError as e:
        print(f"서비스 에러; {e}")

# 실행 시 마이크 권한이 필요합니다.
# speech_to_text()
```

---

## 💡 실습 팁
* [cite_start]**TTS 심화:** 9주차 '나만의 음성 모델 만들기' 단계에서는 단순 변환을 넘어 특정 화자의 목소리 톤을 학습시키는 **FastSpeech2**나 **VITS** 같은 딥러닝 모델을 다루게 될 가능성이 높습니다[cite: 18].
* **STT 심화:** 최근 현업에서는 OpenAI의 **Whisper** 모델이 한국어 인식률이 매우 뛰어나 자주 활용되니, 실습 시 참고해 보세요.

[cite_start]이 외에 시간표 상의 특정 모듈(예: Langchain 활용하기 [cite: 26])과 연동하는 방법이 궁금하시면 말씀해 주세요!
