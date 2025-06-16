@echo off
title Preparation GitHub - Windows Optimizer Pro v2.0

:: Changer vers le repertoire du script
cd /d "%~dp0"

echo =========================================
echo   Preparation GitHub Repository
echo =========================================
echo.

:: Nettoyage des fichiers temporaires
echo 🧹 Nettoyage des fichiers temporaires...
if exist "debug_detection.py" del "debug_detection.py"
if exist "test_device_detection.py" del "test_device_detection.py"
if exist "test_launch.py" del "test_launch.py"
if exist "device_detection_test_*.json" del "device_detection_test_*.json"
if exist "last_session.json" del "last_session.json"

:: Verification des fichiers essentiels GitHub
echo.
echo 📋 Verification des fichiers GitHub...

set "github_ready=true"

if not exist "README_GITHUB.md" (
    echo ❌ README_GITHUB.md manquant
    set "github_ready=false"
) else (
    echo ✅ README_GITHUB.md
)

if not exist "LICENSE" (
    echo ❌ LICENSE manquant
    set "github_ready=false"
) else (
    echo ✅ LICENSE
)

if not exist ".gitignore" (
    echo ❌ .gitignore manquant
    set "github_ready=false"
) else (
    echo ✅ .gitignore
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt manquant
    set "github_ready=false"
) else (
    echo ✅ requirements.txt
)

if not exist "data_img\main.PNG" (
    echo ❌ Images manquantes dans data_img
    set "github_ready=false"
) else (
    echo ✅ Images data_img
)

echo.
echo 📊 Statistiques du projet:
for /f %%i in ('dir *.py /b ^| find /c /v ""') do echo   Python files: %%i
for /f %%i in ('dir *.md /b ^| find /c /v ""') do echo   Documentation: %%i  
for /f %%i in ('dir *.bat /b ^| find /c /v ""') do echo   Scripts: %%i
for /f %%i in ('dir *.json /b ^| find /c /v ""') do echo   Config files: %%i

echo.
if "%github_ready%"=="true" (
    echo ✅ PROJET PRET POUR GITHUB!
    echo.
    echo 🚀 Prochaines etapes:
    echo    1. Creer le repository sur GitHub
    echo    2. Copier README_GITHUB.md vers README.md
    echo    3. Upload tous les fichiers
    echo    4. Creer la premiere release v2.0.0
    echo.
    echo 📋 Nom suggere: windows-optimizer-pro-gaming
    echo 🏷️ Topics: windows gaming optimization pc-tweaks python
) else (
    echo ❌ FICHIERS MANQUANTS - Verifiez ci-dessus
)

echo.
echo 📁 Structure finale:
tree /F /A

echo.
pause
