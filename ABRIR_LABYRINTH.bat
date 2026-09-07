@echo off
title LABYRINTH
color 0C
chcp 65001 >nul
cd /d "%~dp0"
mode con: cols=132 lines=44

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 labyrinth.py
    pause
    exit /b
)

where python >nul 2>nul
if %errorlevel%==0 (
    python labyrinth.py
    pause
    exit /b
)

echo Python no encontrado.
pause
