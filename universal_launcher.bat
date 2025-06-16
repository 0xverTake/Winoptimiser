@echo off
setlocal enabledelayedexpansion
title Windows Optimizer - Gestionnaire Universel v2.0

:: Changer vers le repertoire du script
cd /d "%~dp0"

:: Configuration des couleurs
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "RESET=%ESC%[0m"

cls
echo %CYAN%========================================================%RESET%
echo %MAGENTA%   Windows Optimizer - Gestionnaire Universel v2.0   %RESET%
echo %CYAN%========================================================%RESET%
echo %WHITE%Gestionnaire intelligent pour toutes les versions%RESET%
echo.

:: Variables de configuration
set "VENV_PATH=.venv"
set "REQUIREMENTS_FILE=requirements.txt"
set "MAIN_SCRIPT=optimizer_python.py"
set "SIMPLE_SCRIPT=optimizer_simple.py"
set "TEST_SCRIPT=test_dependencies.py"
set "PYTHON_CMD=python"
set "ERROR_OCCURRED=0"

:: Fonction pour afficher les messages avec couleurs
goto :main

:log_info
echo %BLUE%[INFO]%RESET% %~1
goto :eof

:log_success
echo %GREEN%[SUCCESS]%RESET% %~1
goto :eof

:log_warning
echo %YELLOW%[WARNING]%RESET% %~1
goto :eof

:log_error
echo %RED%[ERROR]%RESET% %~1
set "ERROR_OCCURRED=1"
goto :eof

:separator
echo %CYAN%--------------------------------------------------------%RESET%
goto :eof

:main
:: Vérification des droits administrateur
call :log_info "Verification des droits administrateur..."
net session >nul 2>&1
if %errorlevel% neq 0 (
    call :log_warning "Droits administrateur requis pour certaines fonctionnalites."
    echo %YELLOW%Relancement en tant qu'administrateur...%RESET%
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)
call :log_success "Droits administrateur detectes!"

call :separator

:: Menu principal
:menu
cls
echo %CYAN%========================================================%RESET%
echo %MAGENTA%   Windows Optimizer - Menu Principal   %RESET%
echo %CYAN%========================================================%RESET%
echo.
echo %WHITE%Choisissez une option:%RESET%
echo.
echo %GREEN%1.%RESET% %CYAN%Installation Complete%RESET% - Installer toutes les dependances
echo %GREEN%2.%RESET% %CYAN%Lancer Optimizer Pro%RESET% - Version gaming complete
echo %GREEN%3.%RESET% %CYAN%Lancer Optimizer Simple%RESET% - Version basique
echo %GREEN%4.%RESET% %CYAN%Test des Dependances%RESET% - Verifier l'installation
echo %GREEN%5.%RESET% %CYAN%Maintenance%RESET% - Optimiser et mettre a jour
echo %GREEN%6.%RESET% %CYAN%Gestion Environnement%RESET% - Options avancees
echo %GREEN%7.%RESET% %CYAN%Reparation%RESET% - Corriger les problemes
echo %GREEN%8.%RESET% %CYAN%Informations Systeme%RESET% - Diagnostic complet
echo %GREEN%9.%RESET% %CYAN%Desinstaller%RESET% - Supprimer l'environnement
echo %GREEN%0.%RESET% %RED%Quitter%RESET%
echo.
set /p "choice=%BLUE%Votre choix (0-9): %RESET%"

if "%choice%"=="1" goto :install_all
if "%choice%"=="2" goto :launch_pro
if "%choice%"=="3" goto :launch_simple
if "%choice%"=="4" goto :test_deps
if "%choice%"=="5" goto :maintenance
if "%choice%"=="6" goto :env_management
if "%choice%"=="7" goto :repair
if "%choice%"=="8" goto :system_info
if "%choice%"=="9" goto :uninstall
if "%choice%"=="0" goto :exit

call :log_error "Choix invalide!"
timeout /t 2 >nul
goto :menu

:: Installation complète
:install_all
call :separator
call :log_info "Demarrage de l'installation complete..."

:: Vérification de Python
call :log_info "Verification de Python..."
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "Python n'est pas installe ou non accessible!"
    echo %RED%Veuillez installer Python depuis https://python.org%RESET%
    echo %RED%Assurez-vous de cocher 'Add to PATH' lors de l'installation%RESET%
    pause
    goto :menu
)

for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set "PYTHON_VERSION=%%i"
call :log_success "Python %PYTHON_VERSION% detecte!"

:: Mise à jour de pip
call :log_info "Mise a jour de pip..."
%PYTHON_CMD% -m pip install --upgrade pip >nul 2>&1
if %errorlevel% equ 0 (
    call :log_success "Pip mis a jour avec succes!"
) else (
    call :log_warning "Impossible de mettre a jour pip, continuation..."
)

:: Création de l'environnement virtuel
call :log_info "Creation de l'environnement virtuel..."
if exist "%VENV_PATH%" (
    call :log_info "Environnement virtuel existant detecte, recreation..."
    rmdir /s /q "%VENV_PATH%" >nul 2>&1
)

%PYTHON_CMD% -m venv "%VENV_PATH%"
if %errorlevel% equ 0 (
    call :log_success "Environnement virtuel cree avec succes!"
) else (
    call :log_error "Echec de la creation de l'environnement virtuel!"
    pause
    goto :menu
)

:: Activation et installation des dépendances
call :log_info "Installation des dependances dans l'environnement virtuel..."
"%VENV_PATH%\Scripts\pip.exe" install --upgrade pip >nul 2>&1

if exist "%REQUIREMENTS_FILE%" (
    "%VENV_PATH%\Scripts\pip.exe" install -r "%REQUIREMENTS_FILE%"
    if %errorlevel% equ 0 (
        call :log_success "Dependances principales installees!"
    ) else (
        call :log_error "Echec de l'installation des dependances principales!"
    )
) else (
    call :log_warning "Fichier requirements.txt non trouve, installation manuelle..."
    call :log_info "Installation des packages essentiels..."
    
    "%VENV_PATH%\Scripts\pip.exe" install customtkinter>=5.1.2
    "%VENV_PATH%\Scripts\pip.exe" install psutil>=5.9.0
    "%VENV_PATH%\Scripts\pip.exe" install requests>=2.31.0
    "%VENV_PATH%\Scripts\pip.exe" install Pillow>=9.0.0
    
    call :log_info "Installation des packages optionnels..."
    "%VENV_PATH%\Scripts\pip.exe" install WMI>=1.5.1 2>nul
    if %errorlevel% equ 0 (
        call :log_success "WMI installe (fonctionnalites gaming completes)!"
    ) else (
        call :log_warning "WMI non installe (fonctionnalites gaming limitees)"
    )
    
    "%VENV_PATH%\Scripts\pip.exe" install pywin32>=306 2>nul
    "%VENV_PATH%\Scripts\pip.exe" install matplotlib>=3.7.0 2>nul
    "%VENV_PATH%\Scripts\pip.exe" install numpy>=1.24.0 2>nul
)

:: Test de l'installation
call :log_info "Test de l'installation..."
"%VENV_PATH%\Scripts\python.exe" -c "import customtkinter, psutil, requests; print('Test basique OK')" 2>nul
if %errorlevel% equ 0 (
    call :log_success "Installation terminee avec succes!"
) else (
    call :log_error "Probleme detecte dans l'installation!"
)

echo.
call :log_success "Installation complete terminee!"
echo %GREEN%Vous pouvez maintenant utiliser toutes les fonctionnalites.%RESET%
pause
goto :menu

:: Lancement Optimizer Pro
:launch_pro
call :separator
call :log_info "Lancement de Windows Optimizer Pro..."

if not exist "%VENV_PATH%\Scripts\python.exe" (
    call :log_error "Environnement virtuel non trouve!"
    echo %RED%Executez d'abord l'option 1 (Installation Complete)%RESET%
    pause
    goto :menu
)

if not exist "%MAIN_SCRIPT%" (
    call :log_error "Script principal non trouve: %MAIN_SCRIPT%"
    pause
    goto :menu
)

call :log_success "Demarrage de l'interface..."
"%VENV_PATH%\Scripts\python.exe" "%MAIN_SCRIPT%"

if %errorlevel% neq 0 (
    call :log_error "Erreur lors du lancement!"
    echo %RED%Verifiez les logs ci-dessus pour plus d'informations.%RESET%
    pause
)
goto :menu

:: Lancement Optimizer Simple
:launch_simple
call :separator
call :log_info "Lancement de Windows Optimizer Simple..."

if not exist "%SIMPLE_SCRIPT%" (
    call :log_error "Script simple non trouve: %SIMPLE_SCRIPT%"
    echo %YELLOW%Lancement de la version principale...%RESET%
    goto :launch_pro
)

if not exist "%VENV_PATH%\Scripts\python.exe" (
    call :log_warning "Environnement virtuel non trouve, utilisation de Python systeme..."
    %PYTHON_CMD% "%SIMPLE_SCRIPT%"
) else (
    "%VENV_PATH%\Scripts\python.exe" "%SIMPLE_SCRIPT%"
)

if %errorlevel% neq 0 (
    call :log_error "Erreur lors du lancement!"
    pause
)
goto :menu

:: Test des dépendances
:test_deps
call :separator
call :log_info "Test des dependances..."

if not exist "%VENV_PATH%\Scripts\python.exe" (
    call :log_error "Environnement virtuel non trouve!"
    echo %RED%Executez d'abord l'option 1 (Installation Complete)%RESET%
    pause
    goto :menu
)

if exist "%TEST_SCRIPT%" (
    "%VENV_PATH%\Scripts\python.exe" "%TEST_SCRIPT%"
) else (
    call :log_info "Script de test non trouve, test manuel..."
    
    echo %CYAN%Test des imports principaux...%RESET%
    "%VENV_PATH%\Scripts\python.exe" -c "import tkinter; print('✓ tkinter OK')" 2>nul || echo "✗ tkinter ERREUR"
    "%VENV_PATH%\Scripts\python.exe" -c "import customtkinter; print('✓ customtkinter OK')" 2>nul || echo "✗ customtkinter ERREUR"
    "%VENV_PATH%\Scripts\python.exe" -c "import psutil; print('✓ psutil OK')" 2>nul || echo "✗ psutil ERREUR"
    "%VENV_PATH%\Scripts\python.exe" -c "import requests; print('✓ requests OK')" 2>nul || echo "✗ requests ERREUR"
    "%VENV_PATH%\Scripts\python.exe" -c "import wmi; print('✓ WMI OK')" 2>nul || echo "⚠ WMI optionnel"
    
    call :log_success "Test basique termine!"
)
pause
goto :menu

:: Gestion de l'environnement
:env_management
call :separator
echo %CYAN%Options de gestion de l'environnement:%RESET%
echo.
echo %GREEN%1.%RESET% Recreer l'environnement virtuel
echo %GREEN%2.%RESET% Afficher les packages installes
echo %GREEN%3.%RESET% Nettoyer le cache pip
echo %GREEN%4.%RESET% Exporter la configuration
echo %GREEN%5.%RESET% Retour au menu principal
echo.
set /p "env_choice=%BLUE%Votre choix (1-5): %RESET%"

if "%env_choice%"=="1" goto :recreate_env
if "%env_choice%"=="2" goto :list_packages
if "%env_choice%"=="3" goto :clean_cache
if "%env_choice%"=="4" goto :export_config
if "%env_choice%"=="5" goto :menu

call :log_error "Choix invalide!"
timeout /t 2 >nul
goto :env_management

:recreate_env
call :log_info "Recreation de l'environnement virtuel..."
if exist "%VENV_PATH%" rmdir /s /q "%VENV_PATH%"
goto :install_all

:list_packages
if exist "%VENV_PATH%\Scripts\pip.exe" (
    call :log_info "Packages installes:"
    "%VENV_PATH%\Scripts\pip.exe" list
) else (
    call :log_error "Environnement virtuel non trouve!"
)
pause
goto :env_management

:clean_cache
call :log_info "Nettoyage du cache pip..."
if exist "%VENV_PATH%\Scripts\pip.exe" (
    "%VENV_PATH%\Scripts\pip.exe" cache purge >nul 2>&1
    call :log_success "Cache nettoye!"
) else (
    %PYTHON_CMD% -m pip cache purge >nul 2>&1
    call :log_success "Cache systeme nettoye!"
)
pause
goto :env_management

:export_config
call :log_info "Export de la configuration..."
if exist "%VENV_PATH%\Scripts\pip.exe" (
    "%VENV_PATH%\Scripts\pip.exe" freeze > requirements_current.txt
    call :log_success "Configuration exportee vers requirements_current.txt"
) else (
    call :log_error "Environnement virtuel non trouve!"
)
pause
goto :env_management

:: Réparation
:repair
call :separator
call :log_info "Mode reparation..."

echo %YELLOW%Tentative de reparation automatique...%RESET%

:: Vérification Python
%PYTHON_CMD% --version >nul 2>&1
if %errorlevel% neq 0 (
    call :log_error "Python non accessible!"
    echo %RED%Reinstallez Python avec l'option 'Add to PATH'%RESET%
)

:: Suppression et recréation de l'environnement
if exist "%VENV_PATH%" (
    call :log_info "Suppression de l'ancien environnement..."
    rmdir /s /q "%VENV_PATH%"
)

call :log_info "Recreation de l'environnement..."
goto :install_all

:: Informations système
:system_info
call :separator
call :log_info "Diagnostic systeme complet..."

echo %CYAN%=== INFORMATIONS SYSTEME ===%RESET%
echo OS: %OS%
echo Architecture: %PROCESSOR_ARCHITECTURE%
echo Utilisateur: %USERNAME%
echo Repertoire: %CD%
echo.

echo %CYAN%=== PYTHON ===%RESET%
%PYTHON_CMD% --version 2>nul || echo "Python non accessible"
if exist "%VENV_PATH%\Scripts\python.exe" (
    echo Environnement virtuel: OUI
    "%VENV_PATH%\Scripts\python.exe" --version
) else (
    echo Environnement virtuel: NON
)
echo.

echo %CYAN%=== FICHIERS ===%RESET%
if exist "%MAIN_SCRIPT%" (echo ✓ %MAIN_SCRIPT%) else (echo ✗ %MAIN_SCRIPT%)
if exist "%SIMPLE_SCRIPT%" (echo ✓ %SIMPLE_SCRIPT%) else (echo ✗ %SIMPLE_SCRIPT%)
if exist "%REQUIREMENTS_FILE%" (echo ✓ %REQUIREMENTS_FILE%) else (echo ✗ %REQUIREMENTS_FILE%)
if exist "%TEST_SCRIPT%" (echo ✓ %TEST_SCRIPT%) else (echo ✗ %TEST_SCRIPT%)
echo.

echo %CYAN%=== ESPACE DISQUE ===%RESET%
for %%i in (C:) do echo %%i %% libre sur %%i
echo.

echo %CYAN%=== PROCESSUS PYTHON ===%RESET%
tasklist /fi "imagename eq python*" 2>nul | find "python" || echo "Aucun processus Python actif"

pause
goto :menu

:: Mise à jour
:update_deps
call :separator
call :log_info "Mise a jour des dependances..."

if not exist "%VENV_PATH%\Scripts\pip.exe" (
    call :log_error "Environnement virtuel non trouve!"
    echo %RED%Executez d'abord l'option 1 (Installation Complete)%RESET%
    pause
    goto :menu
)

call :log_info "Mise a jour de pip..."
"%VENV_PATH%\Scripts\pip.exe" install --upgrade pip

call :log_info "Mise a jour des packages..."
if exist "%REQUIREMENTS_FILE%" (
    "%VENV_PATH%\Scripts\pip.exe" install --upgrade -r "%REQUIREMENTS_FILE%"
) else (
    "%VENV_PATH%\Scripts\pip.exe" install --upgrade customtkinter psutil requests Pillow
    "%VENV_PATH%\Scripts\pip.exe" install --upgrade WMI pywin32 2>nul
)

call :log_success "Mise a jour terminee!"
pause
goto :menu

:: Désinstallation
:uninstall
call :separator
call :log_warning "Desinstallation de l'environnement..."
echo %RED%Cette action supprimera completement l'environnement virtuel.%RESET%
echo %RED%Les scripts Python resteront intacts.%RESET%
echo.
set /p "confirm=%YELLOW%Etes-vous sur? (o/N): %RESET%"

if /i "%confirm%"=="o" (
    if exist "%VENV_PATH%" (
        rmdir /s /q "%VENV_PATH%"
        call :log_success "Environnement virtuel supprime!"
    ) else (
        call :log_info "Aucun environnement virtuel a supprimer."
    )
) else (
    call :log_info "Operation annulee."
)
pause
goto :menu

:: Sortie
:exit
call :separator
echo %GREEN%Merci d'avoir utilise Windows Optimizer!%RESET%
echo %CYAN%Pour relancer ce gestionnaire, executez: %~nx0%RESET%
echo.
timeout /t 3 >nul
exit /b 0
