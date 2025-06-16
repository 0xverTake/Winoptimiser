@echo off
echo ========================================
echo   Windows Optimizer Python Version
echo ========================================
echo.

echo Verification des privileges administrateur...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Ô£ô Privileges administrateur detectes
) else (
    echo ✗ Privileges administrateur requis!
    echo.
    echo Veuillez executer en tant qu'administrateur
    pause
    exit /b 1
)

echo.
echo Lancement de l'optimiseur...
cd /d "%~dp0"
python "%~dp0optimizer_python.py"
pause
