@echo off
title Hotel Booking - Frontend
pushd "%~dp0frontend"

echo Installing dependencies...
call npm install
echo.

echo Starting Frontend Development Server...
echo.
call npm run dev

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Frontend server stopped unexpectedly. Code: %errorlevel%
    pause
)
popd
