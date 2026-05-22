#

```python
import gradio as ui
from TTS.api import TTS

# 1. 모델 로드 (최초 1회)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

# 2. 음성 합성 함수 정의
def generate_tts(text, audio_file):
    # 입력받은 오디오 파일(audio_file)을 speaker_wav 경로로 전달합니다.
    output_path = "output.wav"
    tts.tts_to_file(
        text=text, 
        speaker_wav=audio_file, 
        language="ko", 
        file_path=output_path
    )
    return output_path

# 3. Gradio 인터페이스 구성
with gradio.Blocks() as demo:
    gradio.Markdown("## 한국어 TTS 웹앱 (XTTS-v2)")
    
    with gradio.Row():
        text_input = gradio.Textbox(label="텍스트 입력", value="안녕하세요 한국어 공부중입니다.")
        # 사용자가 음성 파일을 업로드할 수 있는 컴포넌트 추가
        audio_input = gradio.Audio(label="참조할 목소리 파일 (.wav)", type="filepath")
        
    btn = gradio.Button("음성 생성")
    audio_output = gradio.Audio(label="생성된 음성")
    
    # 버튼 클릭 시 텍스트와 오디오 파일을 함수로 전달
    btn.click(fn=generate_tts, inputs=[text_input, audio_input], outputs=audio_output)

demo.launch(share=True)

```
