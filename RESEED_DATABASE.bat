@echo off
title QFlow - Database Reseeder
color 0E
cls

echo ==========================================================
echo             QFLOW: DEMO DATABASE RESEEDER                 
echo ==========================================================
echo.
echo Resetting active queue and restoring clean demo state...
echo - Default Admin Account (admin@smartqueue.com / admin123)
echo - 4 Active Service Counters (Counters 1-4)
echo - 5 Standard Service Categories
echo - 15 Historical Analytics Records
echo.

cd server
call npm run seed
cd ..

echo.
echo ==========================================================
echo Database successfully reseeded! Clean demo state ready.
echo ==========================================================
echo.
pause
