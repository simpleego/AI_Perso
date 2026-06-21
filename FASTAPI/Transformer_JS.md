# Transformer JS
> 빠르고 가벼운 음성 인식 모델인 **Moonshine**과 **Transformers.js**를 활용해
> 브라우저에서 100% 로컬로 돌아가는 간단한 Speech-to-Text(STT) 웹 앱 구현 방법

이 앱은 사용자가 오디오 파일(.wav, .mp3 등)을 업로드하면, 브라우저 내부에서 서버 전송 없이 
Moonshine 모델을 통해 텍스트로 변환해 주는 직관적인 뼈대 코드

---

### 1. 프로젝트 초기화 및 패키지 설치

최신 `transformers.js` (v3 이상)를 환경 설정 문제 없이 제대로 구동하려면 모듈 번들러인 **Vite**를 사용하는 것이 가장 깔끔합니다. 터미널을 열고 다음 명령어를 순서대로 실행하세요.

```bash
# Vite를 사용해 바닐라 JS 프로젝트 생성
npm create vite@latest moonshine-app -- --template vanilla
cd moonshine-app

# transformers.js 최신 버전 설치
npm install @huggingface/transformers

# 개발 서버 실행
npm run dev

```

### 2. UI 구성 (`index.html`)

앱의 화면을 구성합니다. 파일 업로드 버튼과 현재 진행 상태 메시지, 그리고 변환된 텍스트를 보여줄 공간을 만듭니다.

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Moonshine ASR Web App</title>
    <style>
      body { font-family: sans-serif; max-width: 600px; margin: 40px auto; line-height: 1.6; }
      #status { color: #555; font-style: italic; }
      .box { padding: 15px; border: 1px solid #ddd; border-radius: 8px; margin-top: 20px; min-height: 50px; }
    </style>
  </head>
  <body>
    <h1>로컬 음성 인식 (Moonshine + Transformers.js)</h1>
    <p>오디오 파일을 선택하면 서버 전송 없이 브라우저에서 텍스트를 추출합니다.</p>
    
    <input type="file" id="audio-file" accept="audio/*" disabled />
    <p id="status">모델을 다운로드하고 초기화하는 중입니다... (잠시만 기다려주세요)</p>
    
    <div class="box">
      <strong>인식 결과:</strong>
      <p id="result"></p>
    </div>

    <script type="module" src="/main.js"></script>
  </body>
</html>

```

### 3. 핵심 로직 구현 (`main.js`)

`Transformers.js`의 `pipeline` API를 사용하면 파이썬의 Hugging Face 코드를 작성하는 것과 거의 동일한 방식으로 브라우저에서 모델을 불러오고 실행할 수 있습니다.

```javascript
import { pipeline } from '@huggingface/transformers';

const statusEl = document.getElementById('status');
const resultEl = document.getElementById('result');
const fileInput = document.getElementById('audio-file');

let transcriber;

// 1. Moonshine 모델 로드
async function loadModel() {
  try {
    // 'onnx-community/moonshine-tiny-ONNX'는 매우 작고 빠른 Moonshine 모델입니다.
    // 더 높은 정확도를 원한다면 'onnx-community/moonshine-base-ONNX'를 사용할 수 있습니다.
    transcriber = await pipeline(
      'automatic-speech-recognition', 
      'onnx-community/moonshine-tiny-ONNX'
    );
    
    statusEl.innerText = "모델 로딩 완료! 오디오 파일을 업로드해보세요.";
    fileInput.disabled = false; // 파일 입력 활성화
  } catch (error) {
    statusEl.innerText = "모델을 불러오는 중 오류가 발생했습니다.";
    console.error("Model load error:", error);
  }
}

// 2. 오디오 파일 처리 및 추론
fileInput.addEventListener('change', async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  statusEl.innerText = "오디오 분석 중... ⏳";
  resultEl.innerText = "";

  // 파일을 브라우저 임시 URL로 변환
  const audioUrl = URL.createObjectURL(file);

  try {
    // 모델에 오디오 전달하여 텍스트 추출
    const output = await transcriber(audioUrl);
    
    // 결과 출력
    resultEl.innerText = output.text;
    statusEl.innerText = "분석 완료! ✨";
  } catch (error) {
    statusEl.innerText = "분석 중 오류가 발생했습니다.";
    console.error("Transcription error:", error);
  }
});

// 앱 시작 시 모델 로드 함수 호출
loadModel();

```

---

### 💡 추가 개발을 위한 팁

* **첫 로딩 시간의 비밀:** 앱을 처음 실행할 때 약 30MB 안팎의 ONNX 모델을 브라우저 캐시에 다운로드하기 때문에 약간의 시간이 걸립니다.
* 하지만 한 번 다운로드된 이후부터는 캐시에서 불러오므로 즉시 실행됩니다.
* **WebGPU 가속 활용:** 사용자의 디바이스 환경에 따라 속도를 극적으로 끌어올리고 싶다면,
*  모델 로드 시 파이프라인 생성 옵션에 `{ device: 'webgpu' }`를 추가해 GPU 가속을 적용할 수 있습니다
*  (단, 일부 구형 브라우저에서는 호환성 확인이 필요합니다).

위 코드가 문제없이 돌아간다면, 다음 단계로는 `navigator.mediaDevices.getUserMedia`를 활용하여   
마이크 입력을 실시간으로 받아 처리하는 기능으로도 충분히 확장해 보실 수 있습니다.
