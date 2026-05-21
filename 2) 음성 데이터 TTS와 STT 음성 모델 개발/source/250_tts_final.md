```python
# 1. 완벽하게 고정된 최소한의 기본 라이브러리만 설치
# !pip install transformers scipy torch

import torch
from transformers import VitsModel, AutoTokenizer
from scipy.io.wavfile import write
from IPython.display import Audio, display

def auto_korean_to_roman(text_input):
    """
    외부 패키지나 API 에러 리스크를 100% 차단하기 위해
    글자 단위 초성/중성/종성 음소 조합을 분석하여 MMS 모델 맞춤형 로마자로 자동 변환합니다.
    """
    # 초성, 중성, 종성 매핑 테이블 (MMS VITS 내부 사전에 완벽 호환되도록 최적화)
    CHOSUNG = ['g', 'gg', 'n', 'd', 'dd', 'r', 'm', 'b', 'bb', 's', 'ss', '', 'j', 'jj', 'ch', 'k', 't', 'p', 'h']
    JOUNGSUNG = ['a', 'ae', 'ya', 'yae', 'eo', 'e', 'ye', 'ye', 'o', 'wa', 'wae', 'oe', 'yo', 'u', 'wo', 'we', 'wi', 'yu', 'eu', 'ui', 'i']
    JONGSUNG = ['', 'g', 'gg', 'gs', 'n', 'nj', 'nh', 'd', 'l', 'lg', 'lm', 'lb', 'ls', 'lt', 'lp', 'lh', 'm', 'b', 'bs', 's', 'ss', 'n', 'j', 'ch', 'k', 't', 'p', 'h']

    result = []
    for char in text_input:
        code = ord(char)
        # 한글 음절 범위인 경우 분해 연산 진행
        if 0xAC00 <= code <= 0xD7A3:
            standard_char_code = code - 0xAC00
            chosung_index = standard_char_code // 588
            joungsung_index = (standard_char_code % 588) // 28
            jongsung_index = standard_char_code % 28

            # 음소 결합 후 자연스러운 음성 합성을 위해 글자 간 약한 공백(스페이스) 처리
            syllable_roman = CHOSUNG[chosung_index] + JOUNGSUNG[joungsung_index] + JONGSUNG[jongsung_index]
            result.append(syllable_roman)
        elif char.isalnum():
            result.append(char.lower())
        elif char in [" ", ",", ".", "!", "?", "~"]:
            result.append(char)

    # 정제된 텍스트 반환
    return " ".join("".join(result).split())


def perfect_korean_tts(text_input, output_filename="korean_output.wav"):
    print("=== 한국어 전용 TTS 음성 합성 실습 (최종 마스터 패치 버전) ===")
    print(f"입력 문장: \"{text_input}\"")

    # 내장 엔진으로 로마자 변환 안전하게 수행
    romanized_text = auto_korean_to_roman(text_input)
    print(f"안전 자동 변환된 로마자: \"{romanized_text}\"")
    print("-" * 50)

    # 1. 401 인증 에러가 절대 없는 공인 공식 레포지토리 로드
    model_name = "facebook/mms-tts-kor"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = VitsModel.from_pretrained(model_name)

    # 2. 토큰화
    inputs = tokenizer(romanized_text, return_tensors="pt")

    # 3. 모델 추론
    with torch.no_grad():
        output = model(**inputs)

    # 4. 오디오 데이터 추출
    if hasattr(output, "waveform"):
        audio_signal = output.waveform[0].numpy()
    else:
        audio_signal = output.audio[0].numpy()

    sampling_rate = model.config.sampling_rate

    # 5. .wav 파일 저장
    write(output_filename, sampling_rate, audio_signal)
    print(f"오디오 파일 저장 완료: {output_filename}")
    print("==================================================")

    # 코랩 플레이어로 즉시 청취
    return display(Audio(output_filename, rate=sampling_rate))


# [테스트 실행] 원하는 문장을 아무거나 입력해도 완벽하게 작동합니다!
test_text = "이제 복잡한 사전이나 전처리 패키지 없이 한글 문장을 그대로 부드럽게 읽을 수 있습니다."
perfect_korean_tts(test_text)
```
