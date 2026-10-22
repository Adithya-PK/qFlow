@echo off
title QFlow - Network IP & QR Code Inspector
color 0B
cls

echo ==========================================================
echo        QFLOW: NETWORK IP & QR CODE REFRESH TOOL           
echo ==========================================================
echo.
echo [1/2] Detecting active Wi-Fi / Hotspot adapter IPv4 address...
echo.

ipconfig | findstr /i "IPv4 Address"
echo.

echo [2/2] Regenerating physical QR code for detected IP...
echo.
cd server
call npm run generate-qr
cd ..

echo.
echo ==========================================================
echo Scan customer-qr.png or use the Customer URL on your phone!
echo Ensure phone and laptop are on the exact same Wi-Fi or Hotspot!
echo ==========================================================
echo.
pause
