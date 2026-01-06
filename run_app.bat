@echo off
call .venv\Scripts\activate.bat
start "" uvicorn app.main:app --port 8001 --reload
ping -n 6 127.0.0.1 > nul
start http://localhost:8001