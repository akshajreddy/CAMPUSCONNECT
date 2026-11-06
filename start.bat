@echo off
title CampusConnect Landing Page
echo ========================================================
echo       Starting CampusConnect Local Preview Server
echo ========================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Python detected. Starting Python HTTP server on port 3000...
    python serve.py 3000
    goto end
)

echo Python not found on PATH. Attempting direct browser launch...
start "" "index.html"

:end
pause
