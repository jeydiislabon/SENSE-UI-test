@echo off
title SENSE - Student Portal
echo ========================================
echo   SENSE - Student Portal
echo   Sentiment Faculty Evaluation System
echo ========================================
echo.

:: Try python from PATH first
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Python found.
    echo Installing dependencies...
    python -m pip install flask==3.0.3 --quiet
    echo Starting server...
    echo.
    echo Open your browser at: http://127.0.0.1:5000
    echo Press Ctrl+C to stop the server.
    echo.
    python app.py
    goto end
)

:: Try common Python install locations
set PYTHON=
for %%U in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
) do (
    if exist %%U (
        set PYTHON=%%U
        goto found
    )
)

:: Python not found
echo [ERROR] Python not found on this machine.
echo.
echo Please install Python first:
echo   1. Open Microsoft Store and search for "Python 3.12"
echo   2. Click Get and wait for installation
echo   3. Close this window and double-click run.bat again
echo.
pause
goto end

:found
echo [OK] Python found at %PYTHON%
echo Installing dependencies...
%PYTHON% -m pip install flask==3.0.3 --quiet
echo Starting server...
echo.
echo Open your browser at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server.
echo.
%PYTHON% app.py

:end
pause
