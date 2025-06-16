#!/usr/bin/env python3
"""
Windows Optimizer - Gestionnaire Universel Python
Version Python du gestionnaire pour toutes les plateformes
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
import ctypes
import time

class Colors:
    """Couleurs pour l'affichage console"""
    if platform.system() == "Windows":
        # Activer les couleurs ANSI sur Windows
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass
    
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class OptimizerManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.venv_path = self.base_dir / ".venv"
        self.requirements_file = self.base_dir / "requirements.txt"
        self.main_script = self.base_dir / "optimizer_python.py"
        self.simple_script = self.base_dir / "optimizer_simple.py"
        self.test_script = self.base_dir / "test_dependencies.py"
        self.config_file = self.base_dir / "launcher_config.json"
        
        # Configuration par défaut
        self.config = {
            "last_run": None,
            "python_path": sys.executable,
            "install_count": 0,
            "preferred_version": "pro"
        }
        
        self.load_config()
    
    def load_config(self):
        """Charger la configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
        except Exception as e:
            self.log_warning(f"Impossible de charger la configuration: {e}")
    
    def save_config(self):
        """Sauvegarder la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.log_warning(f"Impossible de sauvegarder la configuration: {e}")
    
    def log_info(self, message):
        """Afficher un message d'information"""
        print(f"{Colors.BLUE}[INFO]{Colors.RESET} {message}")
    
    def log_success(self, message):
        """Afficher un message de succès"""
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} {message}")
    
    def log_warning(self, message):
        """Afficher un avertissement"""
        print(f"{Colors.YELLOW}[WARNING]{Colors.RESET} {message}")
    
    def log_error(self, message):
        """Afficher une erreur"""
        print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")
    
    def separator(self):
        """Afficher une ligne de séparation"""
        print(f"{Colors.CYAN}{'─' * 60}{Colors.RESET}")
    
    def clear_screen(self):
        """Effacer l'écran"""
        os.system('cls' if platform.system() == "Windows" else 'clear')
    
    def check_admin(self):
        """Vérifier les droits administrateur (Windows uniquement)"""
        if platform.system() == "Windows":
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False
        return True  # Sur Linux/Mac, on assume que l'utilisateur peut utiliser sudo si nécessaire
    
    def get_python_version(self):
        """Obtenir la version de Python"""
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            return "Inconnue"
        except:
            return "Erreur"
    
    def check_venv_exists(self):
        """Vérifier si l'environnement virtuel existe"""
        if platform.system() == "Windows":
            python_exe = self.venv_path / "Scripts" / "python.exe"
        else:
            python_exe = self.venv_path / "bin" / "python"
        
        return python_exe.exists()
    
    def get_venv_python_path(self):
        """Obtenir le chemin Python de l'environnement virtuel"""
        if platform.system() == "Windows":
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")
    
    def get_venv_pip_path(self):
        """Obtenir le chemin pip de l'environnement virtuel"""
        if platform.system() == "Windows":
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")
    
    def show_header(self):
        """Afficher l'en-tête"""
        self.clear_screen()
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.MAGENTA}{Colors.BOLD}   Windows Optimizer - Gestionnaire Universel v2.0   {Colors.RESET}")
        print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")
        print(f"{Colors.WHITE}Gestionnaire intelligent pour toutes les versions{Colors.RESET}")
        
        # Informations système
        if not self.check_admin():
            print(f"{Colors.YELLOW}⚠️  Certaines fonctionnalités nécessitent des droits administrateur{Colors.RESET}")
        
        print()
    
    def show_menu(self):
        """Afficher le menu principal"""
        print(f"{Colors.WHITE}Choisissez une option:{Colors.RESET}")
        print()
        print(f"{Colors.GREEN}1.{Colors.RESET} {Colors.CYAN}Installation Complète{Colors.RESET} - Installer toutes les dépendances")
        print(f"{Colors.GREEN}2.{Colors.RESET} {Colors.CYAN}Lancer Optimizer Pro{Colors.RESET} - Version gaming complète")
        print(f"{Colors.GREEN}3.{Colors.RESET} {Colors.CYAN}Lancer Optimizer Simple{Colors.RESET} - Version basique")
        print(f"{Colors.GREEN}4.{Colors.RESET} {Colors.CYAN}Test des Dépendances{Colors.RESET} - Vérifier l'installation")
        print(f"{Colors.GREEN}5.{Colors.RESET} {Colors.CYAN}Gestion Environnement{Colors.RESET} - Options avancées")
        print(f"{Colors.GREEN}6.{Colors.RESET} {Colors.CYAN}Réparation{Colors.RESET} - Corriger les problèmes")
        print(f"{Colors.GREEN}7.{Colors.RESET} {Colors.CYAN}Informations Système{Colors.RESET} - Diagnostic complet")
        print(f"{Colors.GREEN}8.{Colors.RESET} {Colors.CYAN}Mise à Jour{Colors.RESET} - Mettre à jour les dépendances")
        print(f"{Colors.GREEN}9.{Colors.RESET} {Colors.CYAN}Configuration{Colors.RESET} - Paramètres du gestionnaire")
        print(f"{Colors.GREEN}0.{Colors.RESET} {Colors.RED}Quitter{Colors.RESET}")
        print()
    
    def get_user_choice(self, prompt="Votre choix: ", valid_choices=None):
        """Obtenir le choix de l'utilisateur"""
        while True:
            try:
                choice = input(f"{Colors.BLUE}{prompt}{Colors.RESET}").strip()
                if valid_choices is None or choice in valid_choices:
                    return choice
                else:
                    self.log_error(f"Choix invalide! Options valides: {', '.join(valid_choices)}")
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Opération annulée par l'utilisateur.{Colors.RESET}")
                return None
            except EOFError:
                return None
    
    def install_all(self):
        """Installation complète"""
        self.separator()
        self.log_info("Démarrage de l'installation complète...")
        
        # Vérification de Python
        self.log_info("Vérification de Python...")
        python_version = self.get_python_version()
        if "Erreur" in python_version or "Inconnue" in python_version:
            self.log_error("Python n'est pas installé ou non accessible!")
            self.log_error("Veuillez installer Python depuis https://python.org")
            input("Appuyez sur Entrée pour continuer...")
            return False
        
        self.log_success(f"Python détecté: {python_version}")
        
        # Mise à jour de pip
        self.log_info("Mise à jour de pip...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
            self.log_success("Pip mis à jour avec succès!")
        except subprocess.CalledProcessError:
            self.log_warning("Impossible de mettre à jour pip, continuation...")
        
        # Création de l'environnement virtuel
        self.log_info("Création de l'environnement virtuel...")
        if self.venv_path.exists():
            self.log_info("Environnement virtuel existant détecté, recréation...")
            shutil.rmtree(self.venv_path)
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], 
                          check=True, capture_output=True)
            self.log_success("Environnement virtuel créé avec succès!")
        except subprocess.CalledProcessError as e:
            self.log_error(f"Échec de la création de l'environnement virtuel: {e}")
            input("Appuyez sur Entrée pour continuer...")
            return False
        
        # Installation des dépendances
        self.log_info("Installation des dépendances...")
        pip_path = self.get_venv_pip_path()
        
        # Mise à jour de pip dans l'environnement virtuel
        try:
            subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
        except subprocess.CalledProcessError:
            pass
        
        # Installation à partir du fichier requirements.txt
        if self.requirements_file.exists():
            try:
                subprocess.run([pip_path, "install", "-r", str(self.requirements_file)], 
                              check=True, capture_output=True)
                self.log_success("Dépendances principales installées!")
            except subprocess.CalledProcessError:
                self.log_error("Échec de l'installation des dépendances principales!")
                # Installation manuelle de secours
                self._install_essential_packages(pip_path)
        else:
            self.log_warning("Fichier requirements.txt non trouvé, installation manuelle...")
            self._install_essential_packages(pip_path)
        
        # Test de l'installation
        self.log_info("Test de l'installation...")
        python_path = self.get_venv_python_path()
        try:
            result = subprocess.run([python_path, "-c", 
                                   "import customtkinter, psutil, requests; print('Test basique OK')"], 
                                  check=True, capture_output=True, text=True)
            self.log_success("Installation terminée avec succès!")
            
            # Mise à jour de la configuration
            self.config["install_count"] += 1
            self.config["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.save_config()
            
        except subprocess.CalledProcessError:
            self.log_error("Problème détecté dans l'installation!")
        
        print()
        self.log_success("Installation complète terminée!")
        print(f"{Colors.GREEN}Vous pouvez maintenant utiliser toutes les fonctionnalités.{Colors.RESET}")
        input("Appuyez sur Entrée pour continuer...")
        return True
    
    def _install_essential_packages(self, pip_path):
        """Installation des packages essentiels"""
        essential_packages = [
            "customtkinter>=5.1.2",
            "psutil>=5.9.0", 
            "requests>=2.31.0",
            "Pillow>=9.0.0"
        ]
        
        optional_packages = [
            "WMI>=1.5.1",
            "pywin32>=306",
            "matplotlib>=3.7.0",
            "numpy>=1.24.0"
        ]
        
        self.log_info("Installation des packages essentiels...")
        for package in essential_packages:
            try:
                subprocess.run([pip_path, "install", package], 
                              check=True, capture_output=True)
                self.log_success(f"✓ {package}")
            except subprocess.CalledProcessError:
                self.log_error(f"✗ {package}")
        
        self.log_info("Installation des packages optionnels...")
        for package in optional_packages:
            try:
                subprocess.run([pip_path, "install", package], 
                              check=True, capture_output=True)
                self.log_success(f"✓ {package}")
            except subprocess.CalledProcessError:
                self.log_warning(f"⚠ {package} (optionnel)")
    
    def launch_pro(self):
        """Lancer Optimizer Pro"""
        self.separator()
        self.log_info("Lancement de Windows Optimizer Pro...")
        
        if not self.check_venv_exists():
            self.log_error("Environnement virtuel non trouvé!")
            print(f"{Colors.RED}Exécutez d'abord l'option 1 (Installation Complète){Colors.RESET}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        if not self.main_script.exists():
            self.log_error(f"Script principal non trouvé: {self.main_script}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        self.log_success("Démarrage de l'interface...")
        python_path = self.get_venv_python_path()
        
        try:
            # Lancement en arrière-plan pour permettre l'interface graphique
            subprocess.run([python_path, str(self.main_script)], check=True)
        except subprocess.CalledProcessError as e:
            self.log_error(f"Erreur lors du lancement: {e}")
            print(f"{Colors.RED}Vérifiez les logs ci-dessus pour plus d'informations.{Colors.RESET}")
            input("Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            self.log_info("Lancement interrompu par l'utilisateur.")
    
    def launch_simple(self):
        """Lancer Optimizer Simple"""
        self.separator()
        self.log_info("Lancement de Windows Optimizer Simple...")
        
        if not self.simple_script.exists():
            self.log_error(f"Script simple non trouvé: {self.simple_script}")
            print(f"{Colors.YELLOW}Lancement de la version principale...{Colors.RESET}")
            self.launch_pro()
            return
        
        # Utiliser l'environnement virtuel si disponible, sinon Python système
        if self.check_venv_exists():
            python_path = self.get_venv_python_path()
        else:
            self.log_warning("Environnement virtuel non trouvé, utilisation de Python système...")
            python_path = sys.executable
        
        try:
            subprocess.run([python_path, str(self.simple_script)], check=True)
        except subprocess.CalledProcessError as e:
            self.log_error(f"Erreur lors du lancement: {e}")
            input("Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            self.log_info("Lancement interrompu par l'utilisateur.")
    
    def test_dependencies(self):
        """Tester les dépendances"""
        self.separator()
        self.log_info("Test des dépendances...")
        
        if not self.check_venv_exists():
            self.log_error("Environnement virtuel non trouvé!")
            print(f"{Colors.RED}Exécutez d'abord l'option 1 (Installation Complète){Colors.RESET}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        python_path = self.get_venv_python_path()
        
        if self.test_script.exists():
            try:
                subprocess.run([python_path, str(self.test_script)], check=True)
            except subprocess.CalledProcessError:
                self.log_error("Échec du test des dépendances")
        else:
            self.log_info("Script de test non trouvé, test manuel...")
            self._manual_test(python_path)
        
        input("Appuyez sur Entrée pour continuer...")
    
    def _manual_test(self, python_path):
        """Test manuel des dépendances"""
        tests = [
            ("tkinter", "import tkinter; print('✓ tkinter OK')"),
            ("customtkinter", "import customtkinter; print('✓ customtkinter OK')"),
            ("psutil", "import psutil; print('✓ psutil OK')"),
            ("requests", "import requests; print('✓ requests OK')"),
            ("WMI", "import wmi; print('✓ WMI OK')"),
        ]
        
        print(f"{Colors.CYAN}Test des imports principaux...{Colors.RESET}")
        for name, test_code in tests:
            try:
                result = subprocess.run([python_path, "-c", test_code], 
                                      capture_output=True, text=True, check=True)
                print(result.stdout.strip())
            except subprocess.CalledProcessError:
                if name == "WMI":
                    print("⚠ WMI optionnel")
                else:
                    print(f"✗ {name} ERREUR")
        
        self.log_success("Test basique terminé!")
    
    def show_system_info(self):
        """Afficher les informations système"""
        self.separator()
        self.log_info("Diagnostic système complet...")
        
        print(f"{Colors.CYAN}=== INFORMATIONS SYSTÈME ==={Colors.RESET}")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.machine()}")
        print(f"Utilisateur: {os.getenv('USERNAME', os.getenv('USER', 'Inconnu'))}")
        print(f"Répertoire: {os.getcwd()}")
        print(f"Python: {self.get_python_version()}")
        print()
        
        print(f"{Colors.CYAN}=== ENVIRONNEMENT VIRTUEL ==={Colors.RESET}")
        if self.check_venv_exists():
            print("État: ✓ Installé")
            python_path = self.get_venv_python_path()
            try:
                result = subprocess.run([python_path, "--version"], 
                                      capture_output=True, text=True)
                print(f"Version: {result.stdout.strip()}")
            except:
                print("Version: Erreur")
        else:
            print("État: ✗ Non installé")
        print()
        
        print(f"{Colors.CYAN}=== FICHIERS ==={Colors.RESET}")
        files_to_check = [
            (self.main_script, "optimizer_python.py"),
            (self.simple_script, "optimizer_simple.py"),
            (self.requirements_file, "requirements.txt"),
            (self.test_script, "test_dependencies.py"),
        ]
        
        for file_path, name in files_to_check:
            if file_path.exists():
                print(f"✓ {name}")
            else:
                print(f"✗ {name}")
        print()
        
        print(f"{Colors.CYAN}=== CONFIGURATION ==={Colors.RESET}")
        print(f"Installations: {self.config['install_count']}")
        print(f"Dernière exécution: {self.config.get('last_run', 'Jamais')}")
        print(f"Version préférée: {self.config.get('preferred_version', 'Non définie')}")
        
        input("Appuyez sur Entrée pour continuer...")
    
    def update_dependencies(self):
        """Mettre à jour les dépendances"""
        self.separator()
        self.log_info("Mise à jour des dépendances...")
        
        if not self.check_venv_exists():
            self.log_error("Environnement virtuel non trouvé!")
            print(f"{Colors.RED}Exécutez d'abord l'option 1 (Installation Complète){Colors.RESET}")
            input("Appuyez sur Entrée pour continuer...")
            return
        
        pip_path = self.get_venv_pip_path()
        
        self.log_info("Mise à jour de pip...")
        try:
            subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                          check=True, capture_output=True)
            self.log_success("Pip mis à jour!")
        except subprocess.CalledProcessError:
            self.log_warning("Impossible de mettre à jour pip")
        
        self.log_info("Mise à jour des packages...")
        if self.requirements_file.exists():
            try:
                subprocess.run([pip_path, "install", "--upgrade", "-r", str(self.requirements_file)], 
                              check=True, capture_output=True)
                self.log_success("Packages mis à jour!")
            except subprocess.CalledProcessError:
                self.log_error("Échec de la mise à jour")
        else:
            # Mise à jour manuelle des packages essentiels
            essential_packages = ["customtkinter", "psutil", "requests", "Pillow"]
            for package in essential_packages:
                try:
                    subprocess.run([pip_path, "install", "--upgrade", package], 
                                  check=True, capture_output=True)
                    self.log_success(f"✓ {package}")
                except subprocess.CalledProcessError:
                    self.log_warning(f"⚠ {package}")
        
        self.log_success("Mise à jour terminée!")
        input("Appuyez sur Entrée pour continuer...")
    
    def manage_config(self):
        """Gérer la configuration"""
        self.separator()
        print(f"{Colors.CYAN}Configuration du gestionnaire:{Colors.RESET}")
        print()
        print(f"1. Version préférée: {self.config.get('preferred_version', 'Non définie')}")
        print(f"2. Chemin Python: {self.config.get('python_path', 'Défaut')}")
        print(f"3. Réinitialiser la configuration")
        print(f"4. Exporter la configuration")
        print(f"5. Retour au menu principal")
        print()
        
        choice = self.get_user_choice("Votre choix (1-5): ", ["1", "2", "3", "4", "5"])
        
        if choice == "1":
            print("Versions disponibles:")
            print("1. pro - Version complète gaming")
            print("2. simple - Version basique")
            version_choice = self.get_user_choice("Choisir (1-2): ", ["1", "2"])
            if version_choice == "1":
                self.config["preferred_version"] = "pro"
            elif version_choice == "2":
                self.config["preferred_version"] = "simple"
            self.save_config()
            self.log_success("Configuration sauvegardée!")
        
        elif choice == "2":
            new_path = input("Nouveau chemin Python (Entrée pour défaut): ").strip()
            if new_path:
                self.config["python_path"] = new_path
                self.save_config()
                self.log_success("Chemin Python mis à jour!")
        
        elif choice == "3":
            confirm = self.get_user_choice("Réinitialiser la configuration? (o/N): ")
            if confirm and confirm.lower() == 'o':
                self.config = {
                    "last_run": None,
                    "python_path": sys.executable,
                    "install_count": 0,
                    "preferred_version": "pro"
                }
                self.save_config()
                self.log_success("Configuration réinitialisée!")
        
        elif choice == "4":
            config_export = self.base_dir / "config_export.json"
            try:
                with open(config_export, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                self.log_success(f"Configuration exportée vers: {config_export}")
            except Exception as e:
                self.log_error(f"Erreur d'export: {e}")
        
        input("Appuyez sur Entrée pour continuer...")
    
    def repair(self):
        """Mode réparation"""
        self.separator()
        self.log_info("Mode réparation...")
        
        print(f"{Colors.YELLOW}Tentative de réparation automatique...{Colors.RESET}")
        
        # Suppression et recréation de l'environnement
        if self.venv_path.exists():
            self.log_info("Suppression de l'ancien environnement...")
            shutil.rmtree(self.venv_path)
        
        self.log_info("Recréation de l'environnement...")
        self.install_all()
    
    def run(self):
        """Boucle principale"""
        try:
            while True:
                self.show_header()
                self.show_menu()
                
                choice = self.get_user_choice("Votre choix (0-9): ", 
                                            ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])
                
                if choice is None or choice == "0":
                    break
                elif choice == "1":
                    self.install_all()
                elif choice == "2":
                    self.launch_pro()
                elif choice == "3":
                    self.launch_simple()
                elif choice == "4":
                    self.test_dependencies()
                elif choice == "5":
                    self.repair()  # Simplifié pour l'instant
                elif choice == "6":
                    self.repair()
                elif choice == "7":
                    self.show_system_info()
                elif choice == "8":
                    self.update_dependencies()
                elif choice == "9":
                    self.manage_config()
        
        except KeyboardInterrupt:
            pass
        
        finally:
            self.separator()
            print(f"{Colors.GREEN}Merci d'avoir utilisé Windows Optimizer!{Colors.RESET}")
            print(f"{Colors.CYAN}Pour relancer ce gestionnaire, exécutez: python {Path(__file__).name}{Colors.RESET}")

def main():
    """Point d'entrée principal"""
    try:
        manager = OptimizerManager()
        manager.run()
    except Exception as e:
        print(f"{Colors.RED}Erreur fatale: {e}{Colors.RESET}")
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

if __name__ == "__main__":
    main()
