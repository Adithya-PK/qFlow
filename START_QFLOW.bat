@echo off
setlocal EnableDelayedExpansion
title QFlow - AI-Powered Smart Queue Management System
color 0A
cls

cd /d "%~dp0"

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

:: Step 1: Detect active Wi-Fi / Hotspot IP
echo [1/4] Detecting active network configuration...
for /f "delims=" %%i in ('node scripts/print_ip.js') do set LOCAL_IP=%%i
if "%LOCAL_IP%"=="" set LOCAL_IP=127.0.0.1

:: Step 2: Auto-refresh QR code for detected IP
echo [2/4] Ensuring QR code matches active network (%LOCAL_IP%)...
call node server/scripts/generateQR.js >nul 2>nul

:: Step 3: Prevent Port Conflicts (frees ports 5000 and 5173 if hanging)
echo [3/4] Checking ports 5000 and 5173...
netstat -ano | findstr :5000 >nul 2>nul
if %errorlevel% equ 0 (
    echo [INFO] Freeing existing server process to ensure clean startup...
    taskkill /F /IM node.exe >nul 2>nul
    timeout /t 1 /nobreak >nul
)

echo.
echo ==========================================================
echo   Staff Dashboard (Laptop):    http://localhost:5173/
echo   Customer Portal (Phone):     http://%LOCAL_IP%:5173/customer
echo   Backend Server:              http://localhost:5000
echo   Staff Login:                 admin@smartqueue.com / admin123
echo ==========================================================
echo.
echo [4/4] Starting Express Backend & Vite Frontend...
echo.

:: Automatically launch browser after 4 seconds
start "" cmd /c "timeout /t 4 /nobreak >nul && start http://localhost:5173/"

:: Launch full development server (runs both backend and frontend concurrently)
call npm run dev

pause
