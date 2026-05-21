```python
import os
import re
import torch
from transformers import VitsModel, AutoTokenizer
from scipy.io.wavfile import write
from IPython.display import Audio, display
# 컴파일 에러가 없는 가벼운 한글 자모 분리 패키지 활용
from espnet_tts_frontend. those_tok import Jamotizer 

print("=== 실습: Tacotron2와 HiFi-GAN 활용 파이프라인 시뮬레이션 ===")

# ==========================================
# # 사전학습 모델 로드 
# ==========================================
# 의사코드의 Tacotron2(Text→Mel)와 HiFi-GAN(Mel→Wave) 메커니즘을 
# 가중치가 완벽히 학습된 엔드투엔드 가량인 MMS-TTS 모델을 통해 시뮬레이션합니다.
MODEL_NAME = "facebook/mms-tts-kor"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = VitsModel.from_pretrained(MODEL_NAME)
jamotizer = Jamotizer()

# ==========================================
# # 입력 문장 준비 (문장 유형 다양화)
# ==========================================
texts = [
    "안녕하세요, 오늘은 8월 17일 일요일입니다.",
    "회의는 오전 10시에 시작합니다.",
    "속도를 빠르게 읽어볼게요!",
    "감정을 밝게 표현해 주세요."
]

# ==========================================
# # 텍스트 전처리(NLU/NLP)
# ==========================================
def normalize_text(txt):
    """ 숫자/단위 표기 정규화 및 특수기호 정리 """
    # 의사코드의 number_norm 역할: 숫자를 한글 발음대로 변경
    num_dict = {'0':'영', '1':'일', '2':'이', '3':'삼', '4':'사', '5':'오', '6':'육', '7':'칠', '8':'팔', '9':'구'}
    for n, k in num_dict.items():
        txt = txt.replace(n, k)
        
    # 의사코드의 punctuation_clean 역할: 한글, 공백, 주요 문장부호 제외하고 제거
    txt = re.sub(f"[^가-힣ㄱ-ㅎㅏ-ㅣa-zA-Z0-9\s.,!?]", "", txt)
    return txt

def to_pronunciation(txt):
    """ 한글 -> 발음/음소/자모 시퀀스 변환 (G2P 및 음소 분해) """
    # 의사코드의 g2p(txt) 역할: 한국어 모델 학습의 핵심인 '자모 단위(Phoneme)' 분리를 수행합니다.
    # 예: "안녕하세요" -> "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ" 형태로 변환되어 모델에 입력됩니다.
    jamo_text = jamotizer.get_jamo(txt)
    return jamo_text

# ==========================================
# # Text -> Mel (Tacotron2 시뮬레이션)
# ==========================================
def text_to_mel(txt, speed_tag="normal", style_token=None):
    """ 텍스트를 입력받아 내부 음향 모델을 통해 멜-스펙트로그램 특징을 추출하는 단계를 시뮬레이션합니다. """
    n_txt = normalize_text(txt)
    phon = to_pronunciation(n_txt)
    
    # 토크나이저를 통해 음소 시퀀스를 텐서 인덱스로 변환
    inputs = tokenizer(phon, return_tensors="pt")
    return inputs, phon

# ==========================================
# # Mel -> Wave (HiFi-GAN 보코더 시뮬레이션)
# ==========================================
def mel_to_wav(mel_inputs):
    """ 추출된 멜 특징 평면을 보코더를 통해 시간 축 오디오 파형(Waveform)으로 복원합니다. """
    with torch.no_grad():
        output = model(**mel_inputs)
        
    # 호환성 패치 (transformers 버전별 속성명 안전장치)
    if hasattr(output, "waveform"):
        wav = output.waveform[0].numpy()
    else:
        wav = output.audio[0].numpy()
        
    # 의사코드의 peak_normalize(wav, peak=0.98) 구현
    # 오디오가 찢어지거나 깨지는 것을 방지하기 위해 최대 볼륨을 0.98로 고정
    max_val = max(abs(wav))
    if max_val > 0:
        wav = wav / max_val * 0.98
        
    return wav

def slugify(text):
    """ 파일명 저장을 위해 안전한 문자열로 가공하는 함수 """
    clean = re.sub(r'[^가-힣a-zA-Z0-9]', '_', text)
    return clean[:10] # 너무 길면 10자까지만 자름

# ==========================================
# # 파라미터 조절 실습 및 루프 돌리기
# ==========================================
SR = model.config.sampling_rate # 모델 고유 샘플레이트 (16000Hz)

for txt in texts:
    print(f"\n[원문 처리 중] {txt}")
    
    # 1단계: Text -> Mel 변환 단계 진행 (내부적으로 전처리 및 자모 음소 변환 포함)
    mel, final_phonemes = text_to_mel(txt, speed_tag="normal", style_token=None)
    print(f" └ 전처리 완료된 음소 스트링: {final_phonemes}")
    
    # 2단계: Mel -> Wave 보코더 복원 및 피크 정규화 진행
    wav = mel_to_wav(mel)
    
    # 3단계: 파일 저장 (save_wav 구현)
    safe_filename = f"tts_{slugify(txt)}.wav"
    write(safe_filename, SR, wav)
    print(f" └ 보코더 기반 오디오 합성 완료 -> 파일 저장: {safe_filename}")
    
    # 코랩 환경에서 소리를 즉시 들을 수 있도록 플레이어 정렬 출력
    display(Audio(safe_filename, rate=SR))

print("\n==================================================")
print("모든 가상 문장의 TTS 파이프라인 합성 실습이 완료되었습니다.")
print("==================================================")

```
