"""실습 2: 내장 도구 - Tavily 웹 검색 도구를 Agent에 연결."""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults


# TavilySearchResults는 LangChain이 제공하는 검색 통합 도구다.
# 실행 전 OPENAI_API_KEY와 TAVILY_API_KEY 환경 변수가 필요하다.
search_tool = TavilySearchResults(
    max_results=3,              # 모델에 돌려줄 검색 결과 수
    search_depth="basic",
    include_answer=False,       # 검색 결과 원문을 근거로 Agent가 답하게 한다.
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 내장 도구도 커스텀 도구와 동일하게 tools 목록에 등록한다.
agent = create_agent(
    model=model,
    tools=[search_tool],
    system_prompt=(
        "당신은 AI 기술 리서치 조교입니다. 최신 정보가 필요한 질문에는 tavily_search_results_json "
        "도구를 사용하세요. 답변에는 검색 결과의 제목과 URL을 근거로 제시하세요. "
        "검색 결과에서 확인되지 않은 내용은 추측하지 마세요."
    ),
)

question = "LangChain 1.0에서 기존 initialize_agent 대신 권장하는 Agent 생성 API를 찾아 설명해줘."

result = agent.invoke(
    {"messages": [{"role": "user", "content": question}]}
)

print("[도구 정보]")
print("name:", search_tool.name)
print("description:", search_tool.description)
print("input schema:", search_tool.args)

print("\n[Agent 메시지 흐름]")
for message in result["messages"]:
    if getattr(message, "tool_calls", None):
        print("모델의 도구 호출:", message.tool_calls)
    elif message.type == "tool":
        print("검색 도구 결과:", str(message.content)[:800], "...")

print("\n[최종 답변]")
print(result["messages"][-1].content)

# 실습 과제:
# 1. max_results를 1과 5로 변경하여 답변의 근거 다양성을 비교한다.
# 2. 최신 정보 질문과 일반 개념 질문에서 도구 호출 여부가 달라지는지 확인한다.
