@echo off
chcp 65001 >nul

REM Se placer dans le répertoire du script
cd /d "%~dp0"

echo.
echo 🔧 =================================================
echo    FIX WMI DETECTION - Windows Optimizer Pro
echo 🔧 =================================================
echo.
echo 🎯 Ce script va diagnostiquer et corriger les erreurs WMI
echo    Erreur détectée: COM Error (-2147352567)
echo.
echo ⚠️  ATTENTION: Exécution en tant qu'administrateur requise
echo.
pause

echo.
echo 🚀 Lancement du diagnostic WMI...
echo.

python fix_wmi_detection.py

echo.
echo ✅ Diagnostic terminé!
echo.
echo 📋 Vérifiez le fichier wmi_diagnostic.log pour les détails
echo 🔄 Relancez Windows Optimizer Pro pour tester
echo.
pause
