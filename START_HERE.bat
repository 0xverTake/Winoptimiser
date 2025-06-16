@echo off
title Windows Optimizer - Demarrage Rapide

:: Changer vers le repertoire du script
cd /d "%~dp0"

:: Ce script detecte automatiquement la meilleure facon de lancer l'optimiseur

echo =========================================
echo   Windows Optimizer - Demarrage Rapide
echo =========================================
echo.

:: Verifier si l'environnement virtuel existe
if exist ".venv\Scripts\python.exe" (
    echo Environnement virtuel detecte - Lancement direct...
    
    :: Verifier les droits admin pour les fonctionnalites completes
    net session >nul 2>&1
    if %errorlevel% neq 0 (
        echo Relancement avec droits administrateur...
        powershell -Command "Start-Process '%~f0' -Verb RunAs"
        exit /b
    )
    
    :: Lancer directement la version Pro
    echo Lancement de Windows Optimizer Pro...
    ".venv\Scripts\python.exe" optimizer_python.py
    
    if %errorlevel% neq 0 (
        echo.
        echo Erreur detectee - Lancement du gestionnaire de reparation...
        pause
        goto :launcher
    )
) else (
    echo Premiere utilisation detectee - Lancement du gestionnaire...
    goto :launcher
)

goto :end

:launcher
echo Lancement du gestionnaire universel...
if exist "universal_launcher.bat" (
    call universal_launcher.bat
) else (
    python universal_launcher.py
)

:end
echo.
echo Merci d'avoir utilise Windows Optimizer!
timeout /t 3 >nul
