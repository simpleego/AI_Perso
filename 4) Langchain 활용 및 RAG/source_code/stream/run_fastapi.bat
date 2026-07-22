@echo off
call .venv\Scripts\activate
uvicorn 09_fastapi_sse_server:app --reload
