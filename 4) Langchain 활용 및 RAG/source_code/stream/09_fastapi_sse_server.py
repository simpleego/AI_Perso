"""FastAPI와 Server-Sent Events(SSE)를 이용한 Gemini 스트리밍 서버."""

from __future__ import annotations

import json

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from langchain_core.messages import HumanMessage

from common import content_to_text, get_model

app = FastAPI(title="LangChain Gemini Streaming Demo")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    """같은 폴더의 10_sse_client.html을 열도록 안내한다."""
    return """
    <h2>Gemini SSE 스트리밍 서버가 실행 중입니다.</h2>
    <p>브라우저에서 <code>10_sse_client.html</code> 파일을 열어 실습하세요.</p>
    <p>API 테스트: <code>/stream?query=파이썬을 설명해줘</code></p>
    """


@app.get("/stream")
async def stream_response(
    query: str = Query(min_length=1, max_length=1000),
) -> StreamingResponse:
    """LLM 청크를 SSE 형식으로 클라이언트에 전달한다."""

    async def generate():
        try:
            model = get_model()
            async for chunk in model.astream([HumanMessage(content=query)]):
                text = content_to_text(chunk.content)
                if text:
                    payload = json.dumps({"text": text}, ensure_ascii=False)
                    yield f"event: token\ndata: {payload}\n\n"

            yield "event: done\ndata: {}\n\n"
        except Exception as exc:
            payload = json.dumps({"error": str(exc)}, ensure_ascii=False)
            yield f"event: server_error\ndata: {payload}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
