@echo off
setlocal EnableDelayedExpansion
title QFlow - Network IP & QR Code Inspector
color 0B
cls

cd /d "%~dp0"

echo ==========================================================
echo        QFLOW: NETWORK IP DETECTOR & QR CODE REFRESH       
echo   Department of AI & DS - Easwari Engineering College     
echo ==========================================================
echo.

where node >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Node.js is not installed or not in PATH!
    pause
    exit /b
)

echo [1/3] Detecting active Wi-Fi / Hotspot adapter IPv4 address...
for /f "delims=" %%i in ('node scripts/print_ip.js') do set DETECTED_IP=%%i

echo.
echo ==========================================================
echo   DETECTED ACTIVE IP:    %DETECTED_IP%
echo   Customer Mobile URL:   http://%DETECTED_IP%:5173/customer
echo   Staff Dashboard URL:   http://localhost:5173/
echo ==========================================================
echo.

echo [2/3] Regenerating physical QR code files for %DETECTED_IP%...
node server/scripts/generateQR.js

echo.
echo [3/3] Checking server connection status...
node scripts/check_health.js
if %errorlevel% equ 0 (
    echo.
    echo [OK] System is live! Phone can scan the QR code right now.
) else (
    echo.
    echo [NOTICE] Backend server is not running. Double-click START_QFLOW.bat to launch!
)

echo.
echo ==========================================================
echo All QR code files in 'qr/' are 100%% updated for %DETECTED_IP%!
echo Opening high-resolution QR Poster in your browser...
echo ==========================================================
echo.

start "" "qr/customer-poster.html"

pause
