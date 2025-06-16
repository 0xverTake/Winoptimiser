@echo off
echo ========================================
echo   Installation des dependances Python
echo ========================================
echo.

echo Verification de Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ✗ Python n'est pas installe ou n'est pas dans le PATH!
    echo.
    echo Veuillez installer Python depuis https://python.org
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo ✓ Python detecte
python --version

echo.
echo Installation des dependances...
echo.

REM Nettoyage du cache pip
python -m pip cache purge

REM Mise à jour de pip et setuptools
python -m pip install --upgrade pip setuptools wheel

REM Installation des dépendances depuis requirements.txt
python -m pip install --no-cache-dir -r requirements.txt

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo ✓ Installation reussie!
    echo ========================================
    echo.
    echo Vous pouvez maintenant lancer:
    echo   1. Version simple:    run_simple.bat
    echo   2. Version complete:  run_optimizer.bat
    echo.
) else (
    echo.
    echo ========================================
    echo ✗ Erreur lors de l'installation
    echo ========================================
    echo.
    echo Essayez d'executer manuellement:
    echo python -m pip install -r requirements.txt
    echo.
)

pause
