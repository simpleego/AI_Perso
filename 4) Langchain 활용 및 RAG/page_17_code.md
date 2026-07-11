## 1. 이미지에서 추출한 원본 코드

```python
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI


# 메모리 초기화
memory = ConversationBufferMemory()


# 대화 체인 생성
conversation = ConversationChain(
    llm=OpenAI(temperature=0.7),
    memory=memory,
    verbose=True
)


# 첫 번째 대화
response = conversation.predict(
    input="안녕하세요! 제 이름은 김개발입니다."
)
print(response)


# 두 번째 대화: 이전 맥락 참조
response = conversation.predict(
    input="제 이름이 뭐였죠?"
)
print(response)


# 세 번째 대화
response = conversation.predict(
    input="제가 어떤 분야에 관심이 많을 것 같나요?"
)
print(response)


# 저장된 메모리 확인
print(memory.buffer)
```

## 2. 수정해야 할 부분

원본 코드는 과거 LangChain API를 사용합니다.

* `ConversationChain`은 deprecated 상태이며 `RunnableWithMessageHistory` 사용이 권장됩니다.
* `ConversationBufferMemory` 대신 메시지 목록을 관리하는 `InMemoryChatMessageHistory`를 사용할 수 있습니다.
* `langchain.llms.OpenAI` 대신 `langchain_openai.ChatOpenAI`를 사용합니다.
* `predict()` 대신 `invoke()`를 사용합니다.
* `memory.buffer` 대신 `history.messages`에서 저장된 대화를 확인합니다. ([LangChain 참고 문서][1])

---

# 3. 라이브러리 설치

터미널이나 명령 프롬프트에서 실행합니다.

```bash
pip install -U langchain langchain-openai python-dotenv
```

OpenAI 모델은 별도의 `langchain-openai` 통합 패키지를 통해 연결합니다. ([Docs by LangChain][2])

코랩에서는 다음과 같이 실행합니다.

```python
!pip install -qU langchain langchain-openai python-dotenv
```

---

# 4. `.env` 파일 생성

파이썬 파일과 같은 폴더에 `.env` 파일을 만듭니다.

```env
OPENAI_API_KEY=여기에_OpenAI_API_키_입력
OPENAI_MODEL=gpt-4.1-mini
```

`gpt-4.1-mini`는 OpenAI API에서 제공되는 소형 모델입니다. 계정에서 사용할 수 있는 다른 모델로 바꿔도 됩니다. ([OpenAI 개발자][3])

`.env` 파일은 GitHub에 올리지 않도록 `.gitignore`에 등록합니다.

```gitignore
.env
```

---

# 5. 현재 방식으로 수정한 전체 실습 코드

```python
import os

from dotenv import load_dotenv
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# ==================================================
# 1. 환경변수 불러오기
# ==================================================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY가 설정되지 않았습니다. "
        ".env 파일을 확인해주세요."
    )


# ==================================================
# 2. ChatOpenAI 모델 생성
# ==================================================
model = ChatOpenAI(
    model=model_name,
    temperature=0.7,
    timeout=30,
    max_retries=2,
)


# ==================================================
# 3. 대화 프롬프트 생성
# ==================================================
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
당신은 친절한 AI 강사입니다.

이전 대화 내용을 참고하여 일관성 있게 답변하세요.
사용자에 대해 확실하지 않은 내용은 임의로 단정하지 마세요.
답변은 한국어로 작성하세요.
""",
        ),

        # 이전 대화가 삽입되는 위치
        MessagesPlaceholder(variable_name="history"),

        # 현재 사용자의 입력
        ("human", "{input}"),
    ]
)


# ==================================================
# 4. 기본 체인 생성
# 프롬프트 → 모델
# ==================================================
base_chain = prompt | model


# ==================================================
# 5. 세션별 메모리 저장소
# ==================================================
memory_store = {}


def get_session_history(
    session_id: str
) -> InMemoryChatMessageHistory:
    """세션 ID에 해당하는 대화 기록을 반환한다."""

    if session_id not in memory_store:
        memory_store[session_id] = InMemoryChatMessageHistory()

    return memory_store[session_id]


# ==================================================
# 6. 메모리 기능을 체인에 연결
# ==================================================
conversation = RunnableWithMessageHistory(
    base_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


# ==================================================
# 7. 사용자 세션 설정
# ==================================================
session_config = {
    "configurable": {
        "session_id": "kim-developer"
    }
}


def chat(user_input: str) -> str:
    """사용자의 입력을 전달하고 문자열 응답을 반환한다."""

    response = conversation.invoke(
        {"input": user_input},
        config=session_config,
    )

    return response.content


# ==================================================
# 8. 첫 번째 대화
# ==================================================
print("사용자: 안녕하세요! 제 이름은 김개발입니다.")

response = chat(
    "안녕하세요! 제 이름은 김개발입니다. "
    "저는 인공지능과 프로그래밍에 관심이 있습니다."
)

print("AI:", response)


# ==================================================
# 9. 두 번째 대화: 이전 이름 참조
# ==================================================
print("\n사용자: 제 이름이 뭐였죠?")

response = chat("제 이름이 뭐였죠?")

print("AI:", response)


# ==================================================
# 10. 세 번째 대화: 이전 관심 분야 참조
# ==================================================
print("\n사용자: 제가 어떤 분야에 관심이 있나요?")

response = chat(
    "제가 앞에서 말한 관심 분야는 무엇인가요?"
)

print("AI:", response)


# ==================================================
# 11. 저장된 대화 기록 확인
# ==================================================
print("\n" + "=" * 60)
print("저장된 대화 메모리")
print("=" * 60)

history = memory_store["kim-developer"]

for message in history.messages:
    if message.type == "human":
        role = "사용자"
    elif message.type == "ai":
        role = "AI"
    else:
        role = message.type

    print(f"[{role}] {message.content}")
```

`MessagesPlaceholder`는 기존 메시지 목록이 프롬프트에 들어갈 위치를 나타내고, `RunnableWithMessageHistory`는 호출 전 대화 기록을 읽고 호출 후 새로운 사용자·AI 메시지를 자동으로 추가합니다. ([LangChain 참고 문서][4])

---

## 6. 예상되는 대화 흐름

```text
사용자: 안녕하세요! 제 이름은 김개발입니다.
AI: 안녕하세요, 김개발님. 만나서 반갑습니다.

사용자: 제 이름이 뭐였죠?
AI: 앞에서 김개발이라고 말씀하셨습니다.

사용자: 제가 앞에서 말한 관심 분야는 무엇인가요?
AI: 인공지능과 프로그래밍에 관심이 있다고 말씀하셨습니다.
```

모델의 실제 문장은 실행할 때마다 조금씩 달라질 수 있지만, 이름과 관심 분야를 이전 대화에서 찾아 답변하는 것이 핵심입니다.

---

# 7. 직접 대화하는 챗봇으로 확장

앞의 코드를 실행한 후 다음 반복문을 추가하면 터미널에서 계속 대화할 수 있습니다.

```python
print("\n대화형 챗봇을 시작합니다.")
print("'종료'를 입력하면 프로그램이 끝납니다.")

while True:
    user_input = input("\n사용자: ").strip()

    if user_input.lower() in ["종료", "exit", "quit"]:
        print("AI: 대화를 종료합니다.")
        break

    if not user_input:
        continue

    try:
        response = chat(user_input)
        print("AI:", response)

    except Exception as error:
        print("오류가 발생했습니다.")
        print("오류 내용:", error)
```

---

# 8. 사용자별 메모리 분리 원리

다음과 같이 `session_id`를 다르게 지정하면 각 사용자의 대화가 분리됩니다.

```python
kim_config = {
    "configurable": {
        "session_id": "kim"
    }
}

lee_config = {
    "configurable": {
        "session_id": "lee"
    }
}
```

```text
session_id = "kim"
김개발의 대화 기록

session_id = "lee"
이개발의 대화 기록
```

`RunnableWithMessageHistory`는 세션별 메시지 기록을 관리할 수 있어 여러 사용자나 여러 대화방을 구분하는 데 적합합니다. ([LangChain 참고 문서][1])

---

# 9. 메모리 초기화

특정 사용자의 대화를 삭제하려면 다음과 같이 실행합니다.

```python
memory_store["kim-developer"].clear()

print("대화 기록이 초기화되었습니다.")
```

저장소에서 세션 자체를 제거할 수도 있습니다.

```python
memory_store.pop("kim-developer", None)
```

---

## 기존 코드와 수정 코드 비교

| 기존 방식                      | 현재 실습 방식                      |
| -------------------------- | ----------------------------- |
| `ConversationChain`        | `RunnableWithMessageHistory`  |
| `ConversationBufferMemory` | `InMemoryChatMessageHistory`  |
| `langchain.llms.OpenAI`    | `langchain_openai.ChatOpenAI` |
| `conversation.predict()`   | `conversation.invoke()`       |
| `memory.buffer`            | `history.messages`            |
| 한 개의 전역 메모리                | `session_id`별 메모리             |

현재 예제의 메모리는 프로그램의 RAM에만 저장되므로 프로그램을 종료하면 사라집니다. 실제 서비스에서는 LangGraph의 checkpointer나 데이터베이스 기반 저장소를 사용해 대화를 영구 저장하는 구조로 확장해야 합니다. LangGraph는 단기 메모리를 그래프 상태와 checkpointer로 유지합니다. ([LangChain 참고 문서][5])

[1]: https://reference.langchain.com/python/langchain-classic/chains/conversation/base/ConversationChain?utm_source=chatgpt.com "ConversationChain | langchain_classic"
[2]: https://docs.langchain.com/oss/python/integrations/chat/openai?utm_source=chatgpt.com "ChatOpenAI integration - Docs by LangChain"
[3]: https://developers.openai.com/api/docs/models/gpt-4.1-mini?utm_source=chatgpt.com "GPT-4.1 mini Model | OpenAI API"
[4]: https://reference.langchain.com/python/langchain-core/prompts/chat/MessagesPlaceholder?utm_source=chatgpt.com "MessagesPlaceholder | langchain_core"
[5]: https://reference.langchain.com/python/langchain-core/chat_history/InMemoryChatMessageHistory?utm_source=chatgpt.com "InMemoryChatMessageHistory | langchain_core"
