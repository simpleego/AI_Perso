JSONPlaceholder에서 제공하는 무료 REST API를 활용하여 바닐라 자바스크립트로 **To-Do List**를 만드는 과정을 단계별로 안내해 드리겠습니다. 수강생들이 HTTP 통신(GET, POST, PUT, DELETE)의 개념을 실습을 통해 익힐 수 있도록 구성했습니다.

---

### 1단계: HTML 구조 잡기
데이터를 입력할 input창, 추가 버튼, 그리고 목록이 표시될 영역을 만듭니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Vanilla JS To-Do List (JSONPlaceholder)</title>
    <style>
        .todo-item { display: flex; align-items: center; margin-bottom: 5px; }
        .completed { text-decoration: line-through; color: gray; }
        button { margin-left: 10px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>My To-Do List</h1>
    <div>
        <input type="text" id="todo-input" placeholder="할 일을 입력하세요">
        <button id="add-btn">추가</button>
    </div>
    <ul id="todo-list"></ul>

    <script src="app.js"></script>
</body>
</html>
```

---

### 2단계: API 연동 및 데이터 불러오기 (GET)
페이지가 로드될 때 API 서버에서 기존 데이터를 가져와 화면에 그리는 과정입니다.

```javascript
// app.js
const API_URL = 'https://jsonplaceholder.typicode.com/todos';
const todoList = document.getElementById('todo-list');
const todoInput = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');

// 1. 초기 데이터 로드 (READ)
async function fetchTodos() {
    try {
        // 실제 운영 시에는 모든 데이터를 가져오면 너무 많으므로 10개만 제한해서 가져옵니다.
        const response = await fetch(`${API_URL}?_limit=10`);
        const data = await response.json();
        data.forEach(todo => renderTodo(todo));
    } catch (error) {
        console.error('데이터 로드 실패:', error);
    }
}

// 화면에 리스트 아이템을 그리는 함수
function renderTodo(todo) {
    const li = document.createElement('li');
    li.className = 'todo-item';
    li.dataset.id = todo.id;
    li.innerHTML = `
        <span class="${todo.completed ? 'completed' : ''}">${todo.title}</span>
        <button class="toggle-btn">${todo.completed ? '취소' : '완료'}</button>
        <button class="delete-btn">삭제</button>
    `;
    todoList.appendChild(li);
}

window.onload = fetchTodos;
```

---

### 3단계: 할 일 추가하기 (CREATE)
사용자가 입력한 내용을 서버에 보내고(POST), 성공 응답을 받으면 화면에 추가합니다.

```javascript
// 2. 할 일 추가 (CREATE)
addBtn.addEventListener('click', async () => {
    const title = todoInput.value;
    if (!title) return;

    const newTodo = {
        title: title,
        completed: false,
        userId: 1
    };

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            body: JSON.stringify(newTodo),
            headers: { 'Content-type': 'application/json; charset=UTF-8' }
        });
        const data = await response.json();
        renderTodo(data); // 서버에서 받은 데이터(ID 포함)로 화면 갱신
        todoInput.value = '';
    } catch (error) {
        console.error('추가 실패:', error);
    }
});
```

---

### 4단계: 완료 상태 변경 및 삭제 (UPDATE & DELETE)
이벤트 위임을 활용하여 각 버튼의 기능을 구현합니다.



```javascript
// 3. 수정(UPDATE) 및 삭제(DELETE)
todoList.addEventListener('click', async (e) => {
    const li = e.target.closest('li');
    const id = li.dataset.id;
    const span = li.querySelector('span');

    // 삭제 처리
    if (e.target.classList.contains('delete-btn')) {
        try {
            await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            li.remove(); // 서버 응답 성공 시 DOM에서 제거
        } catch (error) {
            console.error('삭제 실패:', error);
        }
    }

    // 상태 변경 (완료/취소)
    if (e.target.classList.contains('toggle-btn')) {
        const isCompleted = span.classList.contains('completed');
        try {
            const response = await fetch(`${API_URL}/${id}`, {
                method: 'PATCH', // 일부 데이터만 수정할 때는 PATCH 사용
                body: JSON.stringify({ completed: !isCompleted }),
                headers: { 'Content-type': 'application/json; charset=UTF-8' }
            });
            
            if (response.ok) {
                span.classList.toggle('completed');
                e.target.innerText = isCompleted ? '완료' : '취소';
            }
        } catch (error) {
            console.error('상태 변경 실패:', error);
        }
    }
});
```

---

### 수강생 교육 포인트 (Tip)
1.  **비동기 처리**: `fetch` API와 `async/await`를 사용하여 네트워크 통신 중에도 UI가 멈추지 않는 것을 설명해 주세요.
2.  **HTTP 메서드**: 데이터 조회(GET), 생성(POST), 수정(PUT/PATCH), 삭제(DELETE)의 차이점을 강조해 주세요.
3.  **가짜 서버(Mock API)의 한계**: JSONPlaceholder는 실제 DB에 데이터를 저장하지 않으므로, 새로고침하면 추가/삭제한 데이터가 초기화된다는 점을 미리 인지시켜 주시면 좋습니다.
4.  **이벤트 위임**: 리스트 아이템이 동적으로 계속 추가되므로, `ul` 태그 하나에 이벤트를 걸어 관리하는 방식이 효율적임을 알려주세요.
