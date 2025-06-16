@echo off
title Liste des Fichiers - Windows Optimizer Pro v2.0

:: Changer vers le repertoire du script
cd /d "%~dp0"

echo =========================================================
echo   Windows Optimizer Pro - Gaming Edition v2.0
echo   Liste des fichiers du projet
echo =========================================================
echo.

echo 🚀 FICHIERS DE LANCEMENT:
echo.
if exist "START_HERE.bat" (echo ✅ START_HERE.bat - Demarrage automatique intelligent) else (echo ❌ START_HERE.bat)
if exist "universal_launcher.bat" (echo ✅ universal_launcher.bat - Gestionnaire complet Windows) else (echo ❌ universal_launcher.bat)
if exist "universal_launcher.py" (echo ✅ universal_launcher.py - Gestionnaire Python multiplateforme) else (echo ❌ universal_launcher.py)

echo.
echo 🎮 SCRIPTS PRINCIPAUX:
echo.
if exist "optimizer_python.py" (echo ✅ optimizer_python.py - Version Gaming Pro complete) else (echo ❌ optimizer_python.py)
if exist "optimizer_simple.py" (echo ✅ optimizer_simple.py - Version basique rapide) else (echo ❌ optimizer_simple.py)
if exist "test_dependencies.py" (echo ✅ test_dependencies.py - Test et diagnostic) else (echo ❌ test_dependencies.py)
if exist "restore_windows_defaults.py" (echo ✅ restore_windows_defaults.py - Restauration systeme) else (echo ❌ restore_windows_defaults.py)

echo.
echo 📚 DOCUMENTATION:
echo.
if exist "README.md" (echo ✅ README.md - Guide principal) else (echo ❌ README.md)
if exist "README_PRO.md" (echo ✅ README_PRO.md - Documentation complete Pro) else (echo ❌ README_PRO.md)
if exist "README_UNIVERSAL.md" (echo ✅ README_UNIVERSAL.md - Guide gestionnaire universel) else (echo ❌ README_UNIVERSAL.md)
if exist "PROJET_COMPLETE.md" (echo ✅ PROJET_COMPLETE.md - Resume du projet) else (echo ❌ PROJET_COMPLETE.md)

echo.
echo ⚙️ CONFIGURATION:
echo.
if exist "requirements.txt" (echo ✅ requirements.txt - Dependances Python) else (echo ❌ requirements.txt)
if exist "app_config_pro.json" (echo ✅ app_config_pro.json - Configuration application Pro) else (echo ❌ app_config_pro.json)
if exist "project_config.json" (echo ✅ project_config.json - Configuration projet) else (echo ❌ project_config.json)

echo.
echo 🔧 INSTALLATION:
echo.
echo ⚠️ Fichiers d'installation supprimes - Utiliser universal_launcher.bat

echo.
echo 🔄 ENVIRONNEMENT VIRTUEL:
echo.
if exist ".venv\" (echo ✅ .venv\ - Environnement virtuel Python) else (echo ❌ .venv\ - Non installe)
if exist ".venv\Scripts\python.exe" (echo ✅ Python executable dans venv) else (echo ❌ Python executable manquant)
if exist ".venv\Scripts\pip.exe" (echo ✅ Pip executable dans venv) else (echo ❌ Pip executable manquant)

echo.
echo 💾 FICHIERS DE DONNEES:
echo.
if exist "optimizer_backup.json" (echo ✅ optimizer_backup.json - Sauvegarde parametre) else (echo ⚠️ optimizer_backup.json - Sera cree au premier lancement)
if exist "launcher_config.json" (echo ✅ launcher_config.json - Config gestionnaire) else (echo ⚠️ launcher_config.json - Sera cree automatiquement)

echo.
echo 🖼️ RESSOURCES:
echo.
if exist "data_img\" (echo ✅ data_img\ - Repertoire images) else (echo ❌ data_img\)
if exist "data_img\main.PNG" (echo ✅ main.PNG - Image principale) else (echo ❌ main.PNG)
if exist "data_img\simple.PNG" (echo ✅ simple.PNG - Image version simple) else (echo ❌ simple.PNG)
if exist "data_img\team.png" (echo ✅ team.png - Image equipe) else (echo ❌ team.png)

echo.
echo 📊 STATISTIQUES DU PROJET:
echo.

:: Compter les fichiers
set file_count=0
for %%f in (*.*) do set /a file_count+=1

:: Taille du repertoire
for /f "tokens=3" %%a in ('dir /s /-c ^| find "octets"') do set dir_size=%%a

echo Nombre de fichiers: %file_count%
echo Taille approximative: %dir_size% octets
echo.

echo 🎯 RECOMMANDATIONS:
echo.
echo Pour commencer: Double-cliquez sur START_HERE.bat
echo Pour les experts: Utilisez universal_launcher.bat
echo Pour les devs: Lancez universal_launcher.py
echo.

echo =========================================================
echo   Tous les composants sont prets pour l'utilisation!
echo =========================================================
pause
