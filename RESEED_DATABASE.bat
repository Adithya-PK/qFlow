@echo off
title QFlow - Demo Database Reseeder
color 0E
cls

cd /d "%~dp0"

echo ==========================================================
echo             QFLOW: DEMO DATABASE RESEEDER                 
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

echo Resetting active queue and restoring clean demo state...
echo - Default Admin Account (admin@smartqueue.com / admin123)
echo - 4 Active Service Counters (Counters 1-4)
echo - 5 Standard Service Categories
echo - 15 Historical Analytics Records
echo.

call node server/scripts/seed.js

echo.
echo ==========================================================
echo Database successfully reseeded! Clean demo state ready.
echo ==========================================================
echo.
pause
