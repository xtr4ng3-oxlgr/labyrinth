@echo off
title LABYRINTH - Build checksum demo
color 0C
cd /d "%~dp0"

where gcc >nul 2>nul
if %errorlevel% neq 0 (
    echo gcc no encontrado. Este helper es opcional.
    pause
    exit /b
)

gcc checksum_demo.c -O2 -o checksum_demo.exe
pause
