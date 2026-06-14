const API_URL = "http://localhost:8000";

async function sendMessage() {
  const input = document.getElementById("messageInput");
  const message = input.value.trim();

  if (!message) {
    alert("메시지를 입력하세요.");
    return;
  }

  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",
    credentials: "include", // 쿠키 기반 세션 유지 핵심
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const data = await response.json();

  renderHistory(data.history);
  input.value = "";
}

async function loadHistory() {
  const response = await fetch(`${API_URL}/history`, {
    method: "GET",
    credentials: "include"
  });

  const data = await response.json();
  renderHistory(data.history);
}

async function resetSession() {
  const response = await fetch(`${API_URL}/reset`, {
    method: "POST",
    credentials: "include"
  });

  const data = await response.json();
  alert(data.message);

  renderHistory([]);
}

function renderHistory(history) {
  const chatBox = document.getElementById("chatBox");
  chatBox.innerHTML = "";

  history.forEach(item => {
    const div = document.createElement("div");

    if (item.role === "user") {
      div.innerHTML = `<b>사용자:</b> ${item.content}`;
    } else {
      div.innerHTML = `<b>AI:</b> ${item.content}`;
    }

    chatBox.appendChild(div);
  });
}

loadHistory();