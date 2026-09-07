@echo off
title LABYRINTH
color 0C
chcp 65001 >nul
cd /d "%~dp0"
mode con: cols=132 lines=44

if exist "LABYRINTH\LABYRINTH.exe" (
    "LABYRINTH\LABYRINTH.exe"
    pause
    exit /b
)

echo No se encontro LABYRINTH\LABYRINTH.exe
pause
