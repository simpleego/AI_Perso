const API_BASE_URL = "http://127.0.0.1:8000";

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

/**
 * 공통 API 요청 함수
 * 백엔드가 SessionMiddleware 기반이므로 credentials: "include"가 핵심이다.
 */
async function apiRequest(path, options = {}) {
  const config = {
    method: options.method || "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  };

  if (options.body) {
    config.body = JSON.stringify(options.body);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config);

  let data = null;

  // DELETE /todos/{id}는 204 No Content를 반환하므로 JSON 파싱하면 에러가 난다.
  if (response.status !== 204) {
    try {
      data = await response.json();
    } catch (error) {
      data = null;
    }
  }

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      `요청 실패: ${response.status}`;

    throw new Error(errorMessage);
  }

  return data;
}

function showMessage(target, message, type = "success") {
  target.className = `message ${type}`;
  target.textContent = message;
}

function clearMessage(target) {
  target.className = "";
  target.textContent = "";
}

function showTodoPage() {
  authSection.classList.add("hidden");
  todoSection.classList.remove("hidden");
}

function showAuthPage() {
  todoSection.classList.add("hidden");
  authSection.classList.remove("hidden");
}

function setLoggedIn(value) {
  sessionStorage.setItem("todo_logged_in", value ? "true" : "false");
}

function isLoggedIn() {
  return sessionStorage.getItem("todo_logged_in") === "true";
}

/**
 * 회원가입
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
 * 백엔드는 로그인 성공 시 request.session["user_id"]에 사용자 ID를 저장한다.
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

    setLoggedIn(true);
    showMessage(loginMessage, result.message || "로그인 성공", "success");

    showTodoPage();
    await loadTodos();
  } catch (error) {
    setLoggedIn(false);
    showMessage(loginMessage, error.message, "error");
  }
});

/**
 * 할 일 목록 조회
 * GET /todos
 */
async function loadTodos() {
  clearMessage(todoMessage);

  try {
    const todos = await apiRequest("/todos");
    renderTodos(todos);
  } catch (error) {
    showMessage(todoMessage, error.message, "error");
  }
}

/**
 * 할 일 목록 렌더링
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
 * 할 일 추가
 * POST /todos
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
 * 할 일 수정
 * PATCH /todos/{todo_id}
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
 * 할 일 삭제
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
 * 현재 백엔드에는 로그아웃 API가 없으므로
 * 여기서는 프론트엔드 화면 상태만 초기화한다.
 */
logoutBtn.addEventListener("click", () => {
  setLoggedIn(false);
  todoList.innerHTML = "";
  showAuthPage();

  showMessage(
    loginMessage,
    "프론트 화면에서만 로그아웃되었습니다. 서버 세션을 완전히 제거하려면 백엔드 로그아웃 API가 필요합니다.",
    "success"
  );
});

/**
 * 새로고침 시 프론트 상태 복원
 */
window.addEventListener("DOMContentLoaded", async () => {
  if (isLoggedIn()) {
    showTodoPage();
    await loadTodos();
  } else {
    showAuthPage();
  }
});