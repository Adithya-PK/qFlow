@echo off
title QFlow - AI-Powered Smart Queue Management System
color 0A
cls

echo ==========================================================
echo        QFLOW: SMART TOKEN & QUEUE MANAGEMENT SYSTEM       
echo   Department of AI & DS - Easwari Engineering College     
echo ==========================================================
echo.

:: Check Node.js installation
where node >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please install Node.js v18+ to run QFlow.
    pause
    exit /b
)

echo [1/3] Detecting network configuration...
for /f "tokens=4" %%a in ('route print 0.0.0.0 2^>nul ^| findstr "0.0.0.0"') do (
    set LOCAL_IP=%%a
    goto :ip_found
)
:ip_found
if "%LOCAL_IP%"=="" set LOCAL_IP=127.0.0.1

echo.
echo ==========================================================
echo   Staff Dashboard (Laptop):    http://localhost:5173/
echo   Customer Portal (Phone):     http://%LOCAL_IP%:5173/customer
echo   Backend Server:              http://localhost:5000
echo   Staff Login:                 admin@smartqueue.com / admin123
echo ==========================================================
echo.
echo [2/3] Starting Express Backend & Vite Frontend...
echo.

:: Automatically launch browser after 4 seconds in background
start "" cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:5173/"

:: Launch full development server
call npm run dev

pause
