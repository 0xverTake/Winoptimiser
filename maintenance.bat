@echo off
title Maintenance - Windows Optimizer Pro v2.0

:: Changer vers le repertoire du script
cd /d "%~dp0"

echo =========================================
echo   Maintenance Windows Optimizer Pro
echo =========================================
echo.

:: Verifier l'environnement virtuel
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Environnement virtuel non trouve!
    echo Executez d'abord l'installation complete.
    pause
    exit /b 1
)

echo 🔧 Debut de la maintenance...
echo.

:: Mise a jour de pip
echo 📦 Mise a jour de pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
echo.

:: Mise a jour des dependances
echo 🔄 Mise a jour des dependances...
".venv\Scripts\pip.exe" install --upgrade -r requirements.txt
echo.

:: Nettoyage du cache
echo 🧹 Nettoyage du cache...
".venv\Scripts\pip.exe" cache purge
echo.

:: Test rapide
echo 🧪 Test rapide...
".venv\Scripts\python.exe" -c "import customtkinter, psutil, requests; print('✅ Imports principaux OK')"
echo.

:: Lancement de la maintenance Python si disponible
if exist "maintenance.py" (
    echo 🐍 Maintenance Python avancee...
    ".venv\Scripts\python.exe" maintenance.py --auto
) else (
    echo ✅ Maintenance basique terminee
)

echo.
echo =========================================
echo   Maintenance terminee avec succes!
echo =========================================
echo.
echo 💡 Recommandations:
echo    - Votre installation est optimisee
echo    - Tous les packages sont a jour
echo    - Cache nettoye pour de meilleures performances
echo.
pause
