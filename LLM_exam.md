# 거대언어 모델 활용
```html

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PERSO AI</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&display=swap');

  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #c8a96e;
    --accent2: #7c6aff;
    --text: #e8e6f0;
    --muted: #6b6880;
    --user-bg: #1a1828;
    --ai-bg: #12110e;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Mono', monospace;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Header */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 28px;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
    flex-shrink: 0;
  }

  .logo {
    font-family: 'DM Serif Display', serif;
    font-size: 1.4rem;
    letter-spacing: 0.05em;
    color: var(--accent);
  }

  .logo span {
    color: var(--muted);
    font-size: 0.7rem;
    display: block;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.2em;
    margin-top: -2px;
  }

  .status {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.7rem;
    color: var(--muted);
    letter-spacing: 0.1em;
  }

  .dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px #4ade80;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
  }

  /* Chat area */
  #chat {
    flex: 1;
    overflow-y: auto;
    padding: 28px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
  }

  .msg {
    display: flex;
    gap: 14px;
    max-width: 820px;
    animation: fadeUp 0.3s ease;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .msg.user { align-self: flex-end; flex-direction: row-reverse; }

  .avatar {
    width: 32px; height: 32px;
    border-radius: 8px;
    flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.05em;
  }

  .msg.user .avatar {
    background: linear-gradient(135deg, var(--accent2), #a855f7);
    color: #fff;
  }

  .msg.ai .avatar {
    background: linear-gradient(135deg, var(--accent), #e8c99a);
    color: #1a1200;
  }

  .bubble {
    padding: 13px 17px;
    border-radius: 12px;
    font-size: 0.82rem;
    line-height: 1.7;
    max-width: 680px;
  }

  .msg.user .bubble {
    background: var(--user-bg);
    border: 1px solid #2a2640;
    border-top-right-radius: 2px;
    color: #d4d0e8;
  }

  .msg.ai .bubble {
    background: var(--ai-bg);
    border: 1px solid #1e1c14;
    border-top-left-radius: 2px;
    color: var(--text);
  }

  .bubble p { margin-bottom: 8px; }
  .bubble p:last-child { margin-bottom: 0; }

  /* Typing indicator */
  .typing {
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 13px 17px;
  }

  .typing span {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: bounce 1.2s infinite;
  }

  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }

  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
    40% { transform: translateY(-6px); opacity: 1; }
  }

  /* Welcome */
  .welcome {
    margin: auto;
    text-align: center;
    padding: 40px 20px;
  }

  .welcome h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: var(--accent);
    margin-bottom: 10px;
  }

  .welcome p {
    color: var(--muted);
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    margin-bottom: 30px;
  }

  .suggestions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
    max-width: 500px;
  }

  .suggestion {
    padding: 9px 16px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 0.75rem;
    color: var(--muted);
    cursor: pointer;
    transition: all 0.2s;
    background: var(--surface);
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.03em;
  }

  .suggestion:hover {
    border-color: var(--accent);
    color: var(--accent);
    background: #1a1200;
  }

  /* Input area */
  footer {
    padding: 18px 28px 22px;
    border-top: 1px solid var(--border);
    background: var(--surface);
    flex-shrink: 0;
  }

  .input-wrap {
    display: flex;
    gap: 12px;
    align-items: flex-end;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 14px;
    transition: border-color 0.2s;
  }

  .input-wrap:focus-within {
    border-color: var(--accent);
  }

  #input {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    resize: none;
    line-height: 1.5;
    max-height: 120px;
    min-height: 22px;
  }

  #input::placeholder { color: var(--muted); }

  #send {
    width: 36px; height: 36px;
    border-radius: 8px;
    border: none;
    background: var(--accent);
    color: #1a1200;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    transition: all 0.2s;
    flex-shrink: 0;
  }

  #send:hover { background: #e8c99a; transform: scale(1.05); }
  #send:disabled { opacity: 0.3; cursor: not-allowed; transform: none; }

  #send svg { width: 16px; height: 16px; }

  .hint {
    margin-top: 8px;
    font-size: 0.65rem;
    color: var(--muted);
    text-align: center;
    letter-spacing: 0.08em;
  }
</style>
</head>
<body>

<header>
  <div class="logo">
    PERSO AI
    <span>PERSONAL INTELLIGENCE</span>
  </div>
  <div class="status">
    <div class="dot"></div>
    LLM CONNECTED
  </div>
</header>

<div id="chat">
  <div class="welcome" id="welcome">
    <h2>안녕하세요</h2>
    <p>PERSO AI — 거대 언어 모델 기반 개인 AI 어시스턴트</p>
    <div class="suggestions">
      <div class="suggestion" onclick="suggest(this)">AI란 무엇인가요?</div>
      <div class="suggestion" onclick="suggest(this)">LLM 작동 원리를 설명해줘</div>
      <div class="suggestion" onclick="suggest(this)">오늘 할 일 정리를 도와줘</div>
      <div class="suggestion" onclick="suggest(this)">파이썬 코드 작성 도움</div>
    </div>
  </div>
</div>

<footer>
  <div class="input-wrap">
    <textarea id="input" placeholder="메시지를 입력하세요..." rows="1"></textarea>
    <button id="send" onclick="sendMessage()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <line x1="22" y1="2" x2="11" y2="13"></line>
        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
      </svg>
    </button>
  </div>
  <div class="hint">Enter 전송 · Shift+Enter 줄바꿈 · Claude Sonnet 4 구동</div>
</footer>

<script>
const chat = document.getElementById('chat');
const input = document.getElementById('input');
const sendBtn = document.getElementById('send');
let history = [];

// Auto-resize textarea
input.addEventListener('input', () => {
  input.style.height = 'auto';
  input.style.height = Math.min(input.scrollHeight, 120) + 'px';
});

input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

function suggest(el) {
  input.value = el.textContent;
  input.dispatchEvent(new Event('input'));
  sendMessage();
}

function addMsg(role, text) {
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = role === 'user' ? 'YOU' : 'AI';

  const bubble = document.createElement('div');
  bubble.className = 'bubble';

  if (role === 'ai') {
    // Render simple markdown-like paragraphs
    bubble.innerHTML = text
      .split('\n\n').map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`).join('');
  } else {
    bubble.textContent = text;
  }

  div.appendChild(avatar);
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
  return bubble;
}

function addTyping() {
  const welcome = document.getElementById('welcome');
  if (welcome) welcome.remove();

  const div = document.createElement('div');
  div.className = 'msg ai';
  div.id = 'typing-indicator';

  const avatar = document.createElement('div');
  avatar.className = 'avatar';
  avatar.textContent = 'AI';

  const bubble = document.createElement('div');
  bubble.className = 'bubble typing';
  bubble.innerHTML = '<span></span><span></span><span></span>';

  div.appendChild(avatar);
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typing-indicator');
  if (t) t.remove();
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  sendBtn.disabled = true;
  input.value = '';
  input.style.height = 'auto';

  addMsg('user', text);
  history.push({ role: 'user', content: text });

  addTyping();

  try {
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'claude-sonnet-4-20250514',
        max_tokens: 1000,
        system: 'You are PERSO AI, a helpful personal AI assistant. Answer in the same language as the user (Korean if they write in Korean). Be concise and helpful.',
        messages: history
      })
    });

    const data = await res.json();
    removeTyping();

    const reply = data.content?.[0]?.text || '응답을 받을 수 없습니다.';
    addMsg('ai', reply);
    history.push({ role: 'assistant', content: reply });

  } catch (err) {
    removeTyping();
    addMsg('ai', '오류가 발생했습니다. 다시 시도해 주세요.\n\n`' + err.message + '`');
  }

  sendBtn.disabled = false;
  input.focus();
}
</script>
</body>
</html>

```
