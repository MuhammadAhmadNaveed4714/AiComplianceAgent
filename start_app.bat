@echo off
title AI Compliance Agent Launcher
echo ====================================================
echo   STARTING AI COMPLIANCE AGENT (Class Demo)
echo ====================================================
echo.

echo 1. Starting the Brain (Backend API)...
:: This opens a new window for the server and listens to the whole WiFi network (0.0.0.0)
start "Backend API" cmd /k "venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000"

echo    ... Waiting 5 seconds for the Brain to wake up ...
timeout /t 5 >nul

echo 2. Starting the Face (Frontend UI)...
:: This runs Streamlit and connects it to the network
call venv\Scripts\activate
python -m streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501

pause