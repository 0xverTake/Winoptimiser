@echo off
echo.
echo ========================================
echo   VERIFICATION FINALE AVANT GITHUB
echo ========================================
echo.

echo [1/6] Verification des fichiers principaux...
set "missing_files="
if not exist "optimizer_python.py" set "missing_files=%missing_files% optimizer_python.py"
if not exist "requirements.txt" set "missing_files=%missing_files% requirements.txt"
if not exist "README_GITHUB.md" set "missing_files=%missing_files% README_GITHUB.md"
if not exist "LICENSE" set "missing_files=%missing_files% LICENSE"
if not exist ".gitignore" set "missing_files=%missing_files% .gitignore"

if "%missing_files%"=="" (
    echo ✅ Tous les fichiers principaux sont presents
) else (
    echo ❌ Fichiers manquants: %missing_files%
)

echo.
echo [2/6] Verification des images...
set "missing_images="
if not exist "data_img\main.PNG" set "missing_images=%missing_images% main.PNG"
if not exist "data_img\simple.PNG" set "missing_images=%missing_images% simple.PNG"
if not exist "data_img\team.png" set "missing_images=%missing_images% team.png"

if "%missing_images%"=="" (
    echo ✅ Images principales presentes
) else (
    echo ❌ Images manquantes: %missing_images%
)

if exist "data_img\gaming-interface.png" (
    echo ✅ gaming-interface.png presente
) else (
    echo ⚠️ gaming-interface.png manquante - voir ADD_GAMING_IMAGE.md
)

echo.
echo [3/6] Verification de la documentation...
set "missing_docs="
if not exist "GITHUB_SETUP.md" set "missing_docs=%missing_docs% GITHUB_SETUP.md"
if not exist "GUIDE_PERIPHERIQUES.md" set "missing_docs=%missing_docs% GUIDE_PERIPHERIQUES.md"
if not exist "READY_FOR_GITHUB.md" set "missing_docs=%missing_docs% READY_FOR_GITHUB.md"

if "%missing_docs%"=="" (
    echo ✅ Documentation complete
) else (
    echo ❌ Documentation manquante: %missing_docs%
)

echo.
echo [4/6] Test des dependances Python...
python -c "import customtkinter, psutil, tkinter" 2>nul
if %errorlevel%==0 (
    echo ✅ Dependances Python OK
) else (
    echo ❌ Probleme avec les dependances Python
)

echo.
echo [5/6] Verification de la structure du projet...
if exist "data_img\" (
    echo ✅ Dossier data_img/ present
) else (
    echo ❌ Dossier data_img/ manquant
)

echo.
echo [6/6] Test de lancement rapide...
python test_dependencies.py >nul 2>&1
if %errorlevel%==0 (
    echo ✅ Test de lancement reussi
) else (
    echo ⚠️ Probleme potentiel au lancement
)

echo.
echo ========================================
echo           RESUME FINAL
echo ========================================

set "ready_count=0"
if "%missing_files%"=="" set /a "ready_count+=1"
if "%missing_images%"=="" set /a "ready_count+=1"
if "%missing_docs%"=="" set /a "ready_count+=1"

echo.
if %ready_count%==3 (
    echo ✅ PROJET PRET POUR GITHUB! 🚀
    echo.
    echo Actions suivantes:
    echo 1. Copier gaming-interface.png dans data_img/
    echo 2. Creer le repository GitHub
    echo 3. Copier README_GITHUB.md vers README.md
    echo 4. Upload tous les fichiers
    echo 5. Creer la premiere release v2.0.0
) else (
    echo ⚠️ QUELQUES ELEMENTS A CORRIGER
    echo Verifiez les elements marques ❌ ci-dessus
)

echo.
echo Voir GITHUB_SETUP.md pour les instructions detaillees
echo.
pause
