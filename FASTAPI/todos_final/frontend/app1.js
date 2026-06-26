const API_BASE_URL = "http://127.0.0.1:8000";

const TOKEN_KEY = "todo_access_token";

const authSection = document.getElementById("auth-section");
const todoSection = document.getElementById("todo-section");

const signupForm = document.getElementById("signup-form");
const loginForm = document.getElementById("login-form");
const todoForm = document.getElementById("todo-form");

const signupMessage = document.getElementById("signup-message");
const loginMessage = document.getElementById("login-message");
const todoMessage = document.getElementById("todo-message");

const todoList = document.getElementById("todo-list");
const todoTitleInput = document.getElementById("todo-title");
const logoutBtn = document.getElementById("logout-btn");
const tokenView = document.getElementById("token-view");

/**
 * JWT 저장
 */
function saveToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * JWT 조회
 */
function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * JWT 삭제
 */
function removeToken() {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * 로그인 여부 확인
 */
function isLoggedIn() {
  return !!getToken();
}

/**
 * 메시지 출력
 */
function showMessage(target, message, type = "success") {
  target.className = `message ${type}`;
  target.textContent = message;
}

/**
 * 메시지 초기화
 */
function clearMessage(target) {
  target.className = "";
  target.textContent = "";
}

/**
 * 인증 화면 표시
 */
function showAuthPage() {
  authSection.classList.remove("hidden");
  todoSection.classList.add("hidden");
  tokenView.classList.add("hidden");
  tokenView.textContent = "";
}

/**
 * Todo 화면 표시
 */
function showTodoPage() {
  authSection.classList.add("hidden");
  todoSection.classList.remove("hidden");

  const token = getToken();

  if (token) {
    tokenView.classList.remove("hidden");
    tokenView.textContent = `현재 저장된 JWT: ${token}`;
  }
}

/**
 * JWT 토큰을 Authorization 헤더에 포함하는 공통 API 함수
 */
async function apiRequest(path, options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const config = {
    method: options.method || "GET",
    headers,
  };

  if (options.body) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config);

  let data = null;

  if (response.status !== 204) {
    try {
      data = await response.json();
    } catch (error) {
      data = null;
    }
  }

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      removeToken();
      showAuthPage();
    }

    const errorMessage =
      data?.detail ||
      data?.message ||
      `요청 실패: ${response.status}`;

    throw new Error(errorMessage);
  }

  return data;
}

/**
 * 회원가입
 *
 * 백엔드 요청 형식:
 * {
 *   email: string,
 *   password: string
 * }
 */
signupForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  clearMessage(signupMessage);

  const email = document.getElementById("signup-email").value.trim();
  const password = document.getElementById("signup-password").value.trim();

  try {
    const result = await apiRequest("/users/signup", {
      method: "POST",
      body: {
        email,
        password,
      },
    });

    showMessage(
      signupMessage,
      `회원가입 성공: ${result.email}. 이제 로그인하세요.`,
      "success"
    );

    document.getElementById("login-email").value = email;
    document.getElementById("login-password").value = "";

    signupForm.reset();
  } catch (error) {
    showMessage(signupMessage, error.message, "error");
  }
});

/**
 * 로그인
 *
 * JWT 방식에서는 로그인 성공 시 백엔드가 토큰을 반환해야 한다.
 *
 * 권장 응답 형식:
 * {
 *   "access_token": "...",
 *   "token_type": "bearer"
 * }
 */
loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  clearMessage(loginMessage);

  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();

  try {
    const result = await apiRequest("/users/login", {
      method: "POST",
      body: {
        email,
        password,
      },
    });

    /**
     * 백엔드 응답 필드명이 access_token이면 그대로 사용.
     * 만약 백엔드에서 token이라는 이름으로 반환한다면 result.token 사용.
     */
    const accessToken = result.access_token || result.token;

    if (!accessToken) {
      throw new Error(
        "로그인 응답에 JWT 토큰이 없습니다. 백엔드에서 access_token 또는 token을 반환해야 합니다."
      );
    }

    saveToken(accessToken);

    showMessage(loginMessage, "로그인 성공", "success");

    loginForm.reset();

    showTodoPage();
    await loadTodos();
  } catch (error) {
    removeToken();
    showMessage(loginMessage, error.message, "error");
  }
});

/**
 * Todo 목록 조회
 *
 * GET /todos
 *
 * Authorization: Bearer <token>
 */
async function loadTodos() {
  clearMessage(todoMessage);

  try {
    const todos = await apiRequest("/todos", {
      method: "GET",
    });

    renderTodos(todos);
  } catch (error) {
    showMessage(todoMessage, error.message, "error");
  }
}

/**
 * Todo 목록 화면 출력
 */
function renderTodos(todos) {
  todoList.innerHTML = "";

  if (!todos || todos.length === 0) {
    const emptyItem = document.createElement("li");
    emptyItem.className = "todo-item";
    emptyItem.textContent = "등록된 할 일이 없습니다.";
    todoList.appendChild(emptyItem);
    return;
  }

  todos.forEach((todo) => {
    const li = document.createElement("li");
    li.className = "todo-item";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = todo.is_done;

    checkbox.addEventListener("change", async () => {
      await updateTodo(todo.id, {
        is_done: checkbox.checked,
      });
    });

    const titleSpan = document.createElement("span");
    titleSpan.className = todo.is_done ? "todo-title done" : "todo-title";
    titleSpan.textContent = todo.title;

    const editButton = document.createElement("button");
    editButton.textContent = "수정";
    editButton.className = "secondary";

    editButton.addEventListener("click", async () => {
      const newTitle = prompt("수정할 내용을 입력하세요.", todo.title);

      if (newTitle === null) {
        return;
      }

      const trimmedTitle = newTitle.trim();

      if (!trimmedTitle) {
        alert("할 일 내용은 비워둘 수 없습니다.");
        return;
      }

      await updateTodo(todo.id, {
        title: trimmedTitle,
      });
    });

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "삭제";
    deleteButton.className = "danger";

    deleteButton.addEventListener("click", async () => {
      const ok = confirm(`"${todo.title}" 항목을 삭제할까요?`);

      if (!ok) {
        return;
      }

      await deleteTodo(todo.id);
    });

    li.appendChild(checkbox);
    li.appendChild(titleSpan);
    li.appendChild(editButton);
    li.appendChild(deleteButton);

    todoList.appendChild(li);
  });
}

/**
 * Todo 생성
 *
 * POST /todos
 *
 * 요청 body:
 * {
 *   title: string,
 *   is_done: boolean
 * }
 */
todoForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  clearMessage(todoMessage);

  const title = todoTitleInput.value.trim();

  if (!title) {
    showMessage(todoMessage, "할 일 내용을 입력하세요.", "error");
    return;
  }

  try {
    await apiRequest("/todos", {
      method: "POST",
      body: {
        title,
        is_done: false,
      },
    });

    todoTitleInput.value = "";

    showMessage(todoMessage, "할 일이 추가되었습니다.", "success");

    await loadTodos();
  } catch (error) {
    showMessage(todoMessage, error.message, "error");
  }
});

/**
 * Todo 수정
 *
 * PATCH /todos/{todo_id}
 *
 * 요청 body 예:
 * {
 *   title: "수정된 제목"
 * }
 *
 * 또는
 *
 * {
 *   is_done: true
 * }
 */
async function updateTodo(todoId, updateData) {
  clearMessage(todoMessage);

  try {
    await apiRequest(`/todos/${todoId}`, {
      method: "PATCH",
      body: updateData,
    });

    showMessage(todoMessage, "할 일이 수정되었습니다.", "success");

    await loadTodos();
  } catch (error) {
    showMessage(todoMessage, error.message, "error");
    await loadTodos();
  }
}

/**
 * Todo 삭제
 *
 * DELETE /todos/{todo_id}
 */
async function deleteTodo(todoId) {
  clearMessage(todoMessage);

  try {
    await apiRequest(`/todos/${todoId}`, {
      method: "DELETE",
    });

    showMessage(todoMessage, "할 일이 삭제되었습니다.", "success");

    await loadTodos();
  } catch (error) {
    showMessage(todoMessage, error.message, "error");
  }
}

/**
 * JWT 방식 로그아웃
 *
 * 서버 세션을 제거하는 방식이 아니라
 * 브라우저에 저장된 access_token을 삭제한다.
 */
logoutBtn.addEventListener("click", () => {
  removeToken();

  todoList.innerHTML = "";
  todoTitleInput.value = "";

  showAuthPage();

  showMessage(loginMessage, "로그아웃되었습니다.", "success");
});

/**
 * 새로고침 시 토큰이 있으면 Todo 목록 조회
 */
window.addEventListener("DOMContentLoaded", async () => {
  if (isLoggedIn()) {
    showTodoPage();
    await loadTodos();
  } else {
    showAuthPage();
  }
});