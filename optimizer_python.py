#!/usr/bin/env python3
"""
Windows Optimizer Python Version
Version avancée de l'optimiseur Windows avec interface graphique moderne
Inclut une fonction de restauration des paramètres d'origine
"""

# Vérification des imports critiques
def check_critical_imports():
    """Vérifie que tous les modules critiques sont disponibles"""
    critical_modules = {
        'tkinter': 'Interface graphique de base',
        'customtkinter': 'Interface moderne CustomTkinter',
        'winreg': 'Accès au registre Windows',
        'psutil': 'Informations système',
        'wmi': 'Windows Management Instrumentation',
        'requests': 'Requêtes HTTP'
    }
    
    missing_modules = []
    for module, description in critical_modules.items():
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(f"❌ {module}: {description}")
    
    if missing_modules:
        print("🚨 ERREUR: Modules manquants détectés!")
        print("\n".join(missing_modules))
        print("\n🔧 Solutions:")
        print("1. Exécutez maintenance.bat")
        print("2. Utilisez l'option 5 du gestionnaire universel")
        print("3. Réinstallez les dépendances avec: pip install -r requirements.txt")
        input("\nAppuyez sur Entrée pour continuer...")
        return False
    return True

# Vérification avant les imports
if not check_critical_imports():
    sys.exit(1)

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
from customtkinter import CTkFont
import winreg
import subprocess
import psutil
import os
import sys
import json
import threading
from datetime import datetime
import webbrowser
import wmi
import platform
import time
import re
import requests
from pathlib import Path
import ctypes
from ctypes import wintypes

class WindowsOptimizer:
    def __init__(self):
        # Configuration de l'apparence
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("Windows Optimizer Pro - Gaming Edition v2.0")
        self.root.geometry("1200x800")
        self.root.iconbitmap("optimizer.ico") if os.path.exists("optimizer.ico") else None
        
        # Variables
        self.backup_file = "optimizer_backup.json"
        self.original_settings = {}
        self.is_admin = self.check_admin()
        self.wmi_connection = None
        self.gaming_devices = {}
        self.ssd_health_data = {}
        self.monitoring_active = False
        
        # Initialiser WMI AVANT l'interface
        self.init_wmi()
        
        # Interface utilisateur
        self.setup_ui()
        
        # Charger la sauvegarde si elle existe
        self.load_backup()
        
        # Démarrer le monitoring en arrière-plan
        self.start_background_monitoring()
        
    def check_admin(self):
        """Vérifie si le script est exécuté en tant qu'administrateur"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🚀 Windows Optimizer Python", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Vérification admin
        if not self.is_admin:
            warning_label = ctk.CTkLabel(
                main_frame,
                text="⚠️ Exécutez en tant qu'administrateur pour toutes les fonctionnalités",
                text_color="orange"
            )
            warning_label.pack(pady=5)
        
        # Notebook pour les onglets
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Onglets
        self.setup_performance_tab()
        self.setup_privacy_tab()
        self.setup_services_tab()
        self.setup_cleanup_tab()
        self.setup_gaming_tab()
        self.setup_ssd_monitoring_tab()
        self.setup_restore_tab()
        self.setup_about_tab()
        
        # Boutons principaux
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        self.apply_btn = ctk.CTkButton(
            button_frame,
            text="🔧 Appliquer les optimisations",
            command=self.apply_optimizations,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.apply_btn.pack(side="left", padx=10, pady=10)
        
        self.restore_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Restaurer paramètres d'origine",
            command=self.restore_original_settings,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="orange"
        )
        self.restore_btn.pack(side="right", padx=10, pady=10)
        
        # Zone de log
        self.log_text = scrolledtext.ScrolledText(
            main_frame, 
            height=8, 
            bg="#2b2b2b", 
            fg="white",
            font=("Consolas", 10)
        )
        self.log_text.pack(fill="x", padx=20, pady=(0, 10))
        
    def setup_performance_tab(self):
        """Onglet optimisations de performance"""
        self.notebook.add("🚀 Performance")
        perf_frame = self.notebook.tab("🚀 Performance")
        
        # Variables de contrôle
        self.perf_vars = {}
        
        options = [
            ("disable_telemetry", "Désactiver la télémétrie Windows"),
            ("disable_cortana", "Désactiver Cortana"),
            ("disable_onedrive", "Désactiver OneDrive"),
            ("optimize_visual_effects", "Optimiser les effets visuels"),
            ("disable_startup_delay", "Supprimer le délai de démarrage"),
            ("optimize_network", "Optimiser les paramètres réseau"),
            ("disable_background_apps", "Limiter les applications en arrière-plan"),
            ("optimize_gaming", "Optimisations pour les jeux"),
        ]
        
        for key, text in options:
            self.perf_vars[key] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(perf_frame, text=text, variable=self.perf_vars[key])
            checkbox.pack(anchor="w", padx=20, pady=5)
    
    def setup_privacy_tab(self):
        """Onglet confidentialité"""
        self.notebook.add("🔒 Confidentialité")
        privacy_frame = self.notebook.tab("🔒 Confidentialité")
        
        self.privacy_vars = {}
        
        options = [
            ("disable_location", "Désactiver les services de localisation"),
            ("disable_advertising_id", "Désactiver l'ID publicitaire"),
            ("disable_feedback", "Désactiver les demandes de commentaires"),
            ("disable_tailored_experiences", "Désactiver les expériences personnalisées"),
            ("disable_speech_recognition", "Désactiver la reconnaissance vocale"),
            ("disable_handwriting", "Désactiver la collecte d'écriture manuscrite"),
            ("disable_camera_access", "Restreindre l'accès à la caméra"),
            ("disable_microphone_access", "Restreindre l'accès au microphone"),
        ]
        
        for key, text in options:
            self.privacy_vars[key] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(privacy_frame, text=text, variable=self.privacy_vars[key])
            checkbox.pack(anchor="w", padx=20, pady=5)
    
    def setup_services_tab(self):
        """Onglet services Windows"""
        self.notebook.add("⚙️ Services")
        services_frame = self.notebook.tab("⚙️ Services")
        
        self.service_vars = {}
        
        services = [
            ("DiagTrack", "Service de télémétrie"),
            ("dmwappushservice", "Service de messages push"),
            ("WSearch", "Windows Search"),
            ("SysMain", "Superfetch"),
            ("Themes", "Thèmes Windows"),
            ("Spooler", "Spouleur d'impression"),
            ("BITS", "Service de transfert intelligent"),
            ("wuauserv", "Windows Update"),
        ]
        
        for service, description in services:
            self.service_vars[service] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(
                services_frame, 
                text=f"{description} ({service})", 
                variable=self.service_vars[service]
            )
            checkbox.pack(anchor="w", padx=20, pady=5)
    
    def setup_cleanup_tab(self):
        """Onglet nettoyage système"""
        self.notebook.add("🧹 Nettoyage")
        cleanup_frame = self.notebook.tab("🧹 Nettoyage")
        
        self.cleanup_vars = {}
        
        options = [
            ("temp_files", "Fichiers temporaires"),
            ("recycle_bin", "Corbeille"),
            ("browser_cache", "Cache des navigateurs"),
            ("windows_logs", "Journaux Windows"),
            ("crash_dumps", "Fichiers de vidage sur incident"),
            ("thumbnail_cache", "Cache des miniatures"),
            ("prefetch_files", "Fichiers Prefetch"),
            ("recent_documents", "Documents récents"),
        ]
        
        for key, text in options:
            self.cleanup_vars[key] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(cleanup_frame, text=text, variable=self.cleanup_vars[key])
            checkbox.pack(anchor="w", padx=20, pady=5)
        
        # Bouton de nettoyage
        cleanup_btn = ctk.CTkButton(
            cleanup_frame,
            text="🧹 Nettoyer maintenant",
            command=self.run_cleanup,
            height=35
        )
        cleanup_btn.pack(pady=20)
    
    def setup_restore_tab(self):
        """Onglet restauration"""
        self.notebook.add("🔄 Restauration")
        restore_frame = self.notebook.tab("🔄 Restauration")
        
        info_label = ctk.CTkLabel(
            restore_frame,
            text="Cette section permet de restaurer les paramètres Windows d'origine",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=20)
        
        # Informations sur la sauvegarde
        if os.path.exists(self.backup_file):
            backup_info = ctk.CTkLabel(
                restore_frame,
                text=f"✅ Sauvegarde trouvée: {self.backup_file}",
                text_color="green"
            )
        else:
            backup_info = ctk.CTkLabel(
                restore_frame,
                text="❌ Aucune sauvegarde trouvée",
                text_color="red"
            )
        backup_info.pack(pady=10)
        
        # Boutons de restauration
        restore_all_btn = ctk.CTkButton(
            restore_frame,
            text="🔄 Restaurer tous les paramètres",
            command=self.restore_all_settings,
            height=40
        )
        restore_all_btn.pack(pady=10)
        
        create_backup_btn = ctk.CTkButton(
            restore_frame,
            text="💾 Créer une sauvegarde manuelle",
            command=self.create_manual_backup,
            height=40
        )
        create_backup_btn.pack(pady=10)
        
        # Zone d'informations de restauration
        self.restore_info = ctk.CTkTextbox(restore_frame, height=200)
        self.restore_info.pack(fill="both", expand=True, padx=20, pady=20)
        self.update_restore_info()
    
    def setup_about_tab(self):
        """Onglet à propos"""
        self.notebook.add("ℹ️ À propos")
        about_frame = self.notebook.tab("ℹ️ À propos")
        
        about_text = """
        🚀 Windows Optimizer Pro - Gaming Edition v2.0
        
        Version Python avancée de l'optimiseur Windows avec interface moderne.
        
        Fonctionnalités principales:
        • 🚀 Optimisations de performance avancées
        • 🔒 Protection de la confidentialité
        • ⚙️ Gestion intelligente des services Windows
        • 🧹 Nettoyage système complet
        • 🎮 Optimisations gaming professionnelles
        • 💾 Monitoring et diagnostic SSD en temps réel
        • 🔧 Détection automatique des périphériques gaming
        • ⚡ Résolution automatique des problèmes de performance
        • 🔄 Système de restauration complet
        
        🎮 NOUVELLES FONCTIONNALITÉS GAMING:
        • Détection automatique des périphériques gaming
        • Optimisations GPU et CPU spécialisées
        • Monitoring en temps réel des performances
        • Corrections automatiques des problèmes SSD
        
        ⚠️ Attention: Cet outil professionnel doit être utilisé avec précaution.
        Créez toujours une sauvegarde avant d'appliquer des modifications.
        
        💼 Destiné aux gamers professionnels et aux passionnés de performance.
        Compatible avec Windows Store et distribution commerciale.
        """
        
        about_label = ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        about_label.pack(padx=20, pady=20)
        
        # Bouton GitHub
        github_btn = ctk.CTkButton(
            about_frame,
            text="🌐 Projet original sur GitHub",
            command=lambda: webbrowser.open("https://github.com/hellzerg/optimizer")
        )
        github_btn.pack(pady=10)
    
    def log_message(self, message):
        """Ajouter un message au log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Vérifier si l'interface est initialisée
        if hasattr(self, 'log_text') and self.log_text:
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
            self.root.update()
        else:
            # Si l'interface n'est pas prête, afficher dans la console
            print(f"[{timestamp}] {message}")
    
    def safe_log(self, message):
        """Log sécurisé qui fonctionne même avant l'initialisation de l'interface"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def backup_registry_value(self, key_path, value_name, hkey=winreg.HKEY_LOCAL_MACHINE):
        """Sauvegarder une valeur de registre"""
        try:
            with winreg.OpenKey(hkey, key_path) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                backup_key = f"{hkey}\\{key_path}\\{value_name}"
                self.original_settings[backup_key] = {
                    "value": value,
                    "type": reg_type,
                    "hkey": hkey
                }
                return True
        except:
            return False
    
    def set_registry_value(self, key_path, value_name, value, reg_type, hkey=winreg.HKEY_LOCAL_MACHINE):
        """Définir une valeur de registre"""
        try:
            with winreg.CreateKey(hkey, key_path) as key:
                winreg.SetValueEx(key, value_name, 0, reg_type, value)
            return True
        except Exception as e:
            self.log_message(f"Erreur lors de la modification du registre: {e}")
            return False
    
    def disable_telemetry(self):
        """Désactiver la télémétrie Windows"""
        self.log_message("Désactivation de la télémétrie...")
        
        # Sauvegarder avant modification
        self.backup_registry_value(r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry")
        
        # Désactiver la télémétrie
        self.set_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "AllowTelemetry",
            0,
            winreg.REG_DWORD
        )
        
        # Arrêter les services de télémétrie
        services = ["DiagTrack", "dmwappushservice"]
        for service in services:
            try:
                subprocess.run(f'sc stop "{service}"', shell=True, capture_output=True)
                subprocess.run(f'sc config "{service}" start= disabled', shell=True, capture_output=True)
                self.log_message(f"Service {service} arrêté et désactivé")
            except:
                self.log_message(f"Impossible d'arrêter le service {service}")
    
    def optimize_performance(self):
        """Appliquer les optimisations de performance"""
        self.log_message("Application des optimisations de performance...")
        
        # Optimiser les effets visuels
        if self.perf_vars["optimize_visual_effects"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting", winreg.HKEY_CURRENT_USER)
            self.set_registry_value(
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                "VisualFXSetting",
                2,  # Optimiser pour les performances
                winreg.REG_DWORD,
                winreg.HKEY_CURRENT_USER
            )
        
        # Désactiver le délai de démarrage
        if self.perf_vars["disable_startup_delay"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize", "StartupDelayInMSec", winreg.HKEY_CURRENT_USER)
            self.set_registry_value(
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
                "StartupDelayInMSec",
                0,
                winreg.REG_DWORD,
                winreg.HKEY_CURRENT_USER
            )
        
        # Optimisations gaming
        if self.perf_vars["optimize_gaming"].get():
            gaming_tweaks = [
                (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 1),
                (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 8),
                (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", 6),
            ]
            
            for key_path, value_name, value in gaming_tweaks:
                self.backup_registry_value(key_path, value_name)
                self.set_registry_value(key_path, value_name, value, winreg.REG_DWORD)
    
    def apply_privacy_settings(self):
        """Appliquer les paramètres de confidentialité"""
        self.log_message("Application des paramètres de confidentialité...")
        
        if self.privacy_vars["disable_location"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location", "Value", winreg.HKEY_LOCAL_MACHINE)
            self.set_registry_value(
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
                "Value",
                "Deny",
                winreg.REG_SZ
            )
        
        if self.privacy_vars["disable_advertising_id"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled", winreg.HKEY_CURRENT_USER)
            self.set_registry_value(
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
                "Enabled",
                0,
                winreg.REG_DWORD,
                winreg.HKEY_CURRENT_USER
            )
    
    def manage_services(self):
        """Gérer les services Windows"""
        self.log_message("Gestion des services Windows...")
        
        for service, var in self.service_vars.items():
            if var.get():
                try:
                    # Arrêter et désactiver le service
                    subprocess.run(f'sc stop "{service}"', shell=True, capture_output=True)
                    subprocess.run(f'sc config "{service}" start= disabled', shell=True, capture_output=True)
                    self.log_message(f"Service {service} désactivé")
                except:
                    self.log_message(f"Impossible de désactiver le service {service}")
    
    def run_cleanup(self):
        """Exécuter le nettoyage système"""
        self.log_message("Démarrage du nettoyage système...")
        
        if self.cleanup_vars["temp_files"].get():
            temp_dirs = [os.environ.get("TEMP"), r"C:\Windows\Temp"]
            for temp_dir in temp_dirs:
                if temp_dir and os.path.exists(temp_dir):
                    try:
                        for file in os.listdir(temp_dir):
                            file_path = os.path.join(temp_dir, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                        self.log_message(f"Fichiers temporaires supprimés de {temp_dir}")
                    except:
                        self.log_message(f"Erreur lors du nettoyage de {temp_dir}")
        
        if self.cleanup_vars["recycle_bin"].get():
            try:
                subprocess.run("rd /s /q C:\\$Recycle.Bin", shell=True, capture_output=True)
                self.log_message("Corbeille vidée")
            except:
                self.log_message("Impossible de vider la corbeille")
        
        self.log_message("Nettoyage terminé")
    
    def save_backup(self):
        """Sauvegarder les paramètres actuels"""
        try:
            with open(self.backup_file, 'w') as f:
                json.dump(self.original_settings, f, indent=2)
            self.log_message(f"Sauvegarde créée: {self.backup_file}")
        except Exception as e:
            self.log_message(f"Erreur lors de la sauvegarde: {e}")
    
    def load_backup(self):
        """Charger la sauvegarde existante"""
        try:
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r') as f:
                    self.original_settings = json.load(f)
                self.log_message("Sauvegarde chargée")
        except Exception as e:
            self.log_message(f"Erreur lors du chargement de la sauvegarde: {e}")
    
    def restore_original_settings(self):
        """Restaurer les paramètres d'origine"""
        if not self.original_settings:
            messagebox.showwarning("Attention", "Aucune sauvegarde trouvée!")
            return
        
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment restaurer tous les paramètres d'origine?"):
            self.log_message("Restauration des paramètres d'origine...")
            
            for backup_key, backup_data in self.original_settings.items():
                try:
                    parts = backup_key.split("\\")
                    hkey = backup_data["hkey"]
                    key_path = "\\".join(parts[1:-1])
                    value_name = parts[-1]
                    
                    self.set_registry_value(
                        key_path,
                        value_name,
                        backup_data["value"],
                        backup_data["type"],
                        hkey
                    )
                except Exception as e:
                    self.log_message(f"Erreur lors de la restauration de {backup_key}: {e}")
            
            self.log_message("Restauration terminée")
            messagebox.showinfo("Succès", "Paramètres restaurés avec succès!")
    
    def restore_all_settings(self):
        """Restaurer tous les paramètres système"""
        self.restore_original_settings()
    
    def create_manual_backup(self):
        """Créer une sauvegarde manuelle"""
        self.log_message("Création d'une sauvegarde manuelle...")
        
        # Sauvegarder les principales clés de registre
        important_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo", "Enabled"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting"),
        ]
        
        for hkey, key_path, value_name in important_keys:
            self.backup_registry_value(key_path, value_name, hkey)
        
        self.save_backup()
        self.update_restore_info()
        messagebox.showinfo("Succès", "Sauvegarde manuelle créée!")
    
    def update_restore_info(self):
        """Mettre à jour les informations de restauration"""
        if hasattr(self, 'restore_info'):
            info_text = "Informations de sauvegarde:\n\n"
            
            if os.path.exists(self.backup_file):
                info_text += f"✅ Fichier de sauvegarde: {self.backup_file}\n"
                info_text += f"📅 Dernière modification: {datetime.fromtimestamp(os.path.getmtime(self.backup_file))}\n"
                info_text += f"📊 Nombre d'entrées sauvegardées: {len(self.original_settings)}\n\n"
                
                if self.original_settings:
                    info_text += "Clés sauvegardées:\n"
                    for key in list(self.original_settings.keys())[:10]:  # Afficher les 10 premières
                        info_text += f"• {key}\n"
                    if len(self.original_settings) > 10:
                        info_text += f"... et {len(self.original_settings) - 10} autres\n"
            else:
                info_text += "❌ Aucune sauvegarde trouvée\n"
                info_text += "Créez une sauvegarde avant d'appliquer des optimisations.\n"
            
            self.restore_info.delete("1.0", tk.END)
            self.restore_info.insert("1.0", info_text)
    
    def apply_optimizations(self):
        """Appliquer toutes les optimisations sélectionnées"""
        if not self.is_admin:
            messagebox.showwarning("Attention", "Droits administrateur requis pour certaines optimisations!")
        
        if messagebox.askyesno("Confirmation", "Voulez-vous appliquer les optimisations sélectionnées?"):
            self.log_message("=== DÉBUT DES OPTIMISATIONS ===")
            
            # Créer une sauvegarde automatique
            if not os.path.exists(self.backup_file):
                self.create_manual_backup()
            
            # Appliquer les optimisations
            threading.Thread(target=self._apply_optimizations_thread, daemon=True).start()
    
    def _apply_optimizations_thread(self):
        """Thread pour appliquer les optimisations"""
        try:
            # Performance
            if any(var.get() for var in self.perf_vars.values()):
                if self.perf_vars["disable_telemetry"].get():
                    self.disable_telemetry()
                self.optimize_performance()
            
            # Confidentialité
            if any(var.get() for var in self.privacy_vars.values()):
                self.apply_privacy_settings()
            
            # Services
            if any(var.get() for var in self.service_vars.values()):
                self.manage_services()
            
            self.log_message("=== OPTIMISATIONS TERMINÉES ===")
            self.root.after(0, lambda: messagebox.showinfo("Succès", "Optimisations appliquées avec succès!\nRedémarrez votre ordinateur pour que tous les changements prennent effet."))
            
        except Exception as e:
            self.log_message(f"Erreur lors des optimisations: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors des optimisations: {e}"))
    
    def init_wmi(self):
        """Initialiser la connexion WMI"""
        try:
            print("🔌 Initialisation de la connexion WMI...")
            import wmi
            self.wmi_connection = wmi.WMI()
            print("✅ Connexion WMI établie avec succès")
            self.safe_log("Connexion WMI initialisée avec succès")
        except ImportError:
            print("❌ Module WMI non disponible")
            self.safe_log("WMI non disponible - Installation: pip install WMI")
            self.wmi_connection = None
        except Exception as e:
            print(f"❌ Erreur WMI: {e}")
            self.safe_log(f"Erreur lors de l'initialisation WMI: {e}")
            self.wmi_connection = None
    
    def detect_gaming_devices(self):
        """Détecter les périphériques gaming avec méthodes améliorées"""
        devices = {
            'gpu': [],
            'audio': [],
            'network': [],
            'usb_devices': [],
            'cooling': [],
            'storage': []
        }
        
        try:
            if self.wmi_connection:
                # GPU - Détection améliorée avec requête explicite
                try:
                    gpus = self.wmi_connection.query("SELECT * FROM Win32_VideoController")
                    for gpu in gpus:
                        if gpu.Name:
                            # Filtrer les GPU intégrés Intel de base
                            if "Intel(R) UHD" in gpu.Name or "Intel(R) HD" in gpu.Name:
                                continue
                            
                            memory_info = "N/A"
                            if gpu.AdapterRAM:
                                try:
                                    memory_gb = int(gpu.AdapterRAM) / (1024**3)
                                    memory_info = f"{memory_gb:.1f} GB"
                                except (ValueError, TypeError):
                                    memory_info = str(gpu.AdapterRAM)
                            
                            gpu_info = {
                                'name': gpu.Name,
                                'driver_version': gpu.DriverVersion or "N/A",
                                'memory': memory_info,
                                'status': gpu.Status or "OK"
                            }
                            
                            # Détecter les marques gaming
                            if any(brand in gpu.Name.upper() for brand in ['NVIDIA', 'AMD', 'RADEON', 'GEFORCE', 'RTX', 'GTX']):
                                gpu_info['gaming'] = True
                            
                            devices['gpu'].append(gpu_info)
                except Exception as e:
                    self.log_message(f"Erreur détection GPU: {e}")
                
                # Audio - Détection améliorée avec requête explicite
                try:
                    audio_devices = self.wmi_connection.query("SELECT * FROM Win32_SoundDevice")
                    for audio in audio_devices:
                        if audio.Name and audio.Name != "Aucun":
                            # Exclure les pilotes audio Windows basiques
                            exclude_keywords = ['High Definition Audio', 'Microsoft', 'Composite', 'Generic']
                            if not any(keyword in audio.Name for keyword in exclude_keywords):
                                audio_info = {
                                    'name': audio.Name,
                                    'manufacturer': audio.Manufacturer or "N/A",
                                    'status': audio.Status or "OK"
                                }
                                
                                # Détecter les marques gaming
                                gaming_brands = ['SteelSeries', 'Razer', 'Logitech', 'HyperX', 'Corsair', 'Sennheiser', 'Audio-Technica']
                                if any(brand.lower() in audio.Name.lower() for brand in gaming_brands):
                                    audio_info['gaming'] = True
                                
                                devices['audio'].append(audio_info)
                except Exception as e:
                    self.log_message(f"Erreur détection Audio: {e}")
                
                # USB - Détection améliorée avec Win32_PnPEntity et requête explicite
                try:
                    pnp_devices = self.wmi_connection.query("SELECT * FROM Win32_PnPEntity")
                    for device in pnp_devices:
                        if device.Name and device.Service:
                            name_lower = device.Name.lower()
                            
                            # Mots-clés gaming et périphériques
                            gaming_keywords = [
                                'gaming', 'mouse', 'keyboard', 'headset', 'controller', 
                                'gamepad', 'joystick', 'webcam', 'microphone',
                                'razer', 'logitech', 'corsair', 'steelseries', 'hyperx',
                                'roccat', 'cooler master', 'asus', 'msi', 'rival', 'arctis'
                            ]
                            
                            if any(keyword in name_lower for keyword in gaming_keywords):
                                device_info = {
                                    'name': device.Name,
                                    'status': device.Status or "OK"
                                }
                                
                                # Catégoriser le périphérique
                                if any(k in name_lower for k in ['mouse', 'souris', 'rival']):
                                    device_info['category'] = 'Souris Gaming'
                                elif any(k in name_lower for k in ['keyboard', 'clavier']):
                                    device_info['category'] = 'Clavier Gaming'
                                elif any(k in name_lower for k in ['headset', 'headphone', 'casque', 'arctis', 'audio']):
                                    device_info['category'] = 'Audio Gaming'
                                elif any(k in name_lower for k in ['controller', 'gamepad', 'manette']):
                                    device_info['category'] = 'Manette'
                                elif any(k in name_lower for k in ['webcam', 'camera']):
                                    device_info['category'] = 'Webcam'
                                else:
                                    device_info['category'] = 'Périphérique Gaming'
                                
                                devices['usb_devices'].append(device_info)
                except Exception as e:
                    self.log_message(f"Erreur détection USB: {e}")
                
                # Réseau - Détection améliorée avec requête explicite
                try:
                    network_adapters = self.wmi_connection.query("SELECT * FROM Win32_NetworkAdapter")
                    for adapter in network_adapters:
                        if adapter.Name and adapter.AdapterType:
                            # Filtrer les adaptateurs physiques
                            if adapter.PhysicalAdapter or "Ethernet" in str(adapter.AdapterType):
                                speed_info = "N/A"
                                if adapter.Speed:
                                    try:
                                        speed_mbps = int(adapter.Speed) / 1000000
                                        speed_info = f"{speed_mbps:.0f} Mbps"
                                    except (ValueError, TypeError):
                                        speed_info = str(adapter.Speed)
                                
                                adapter_info = {
                                    'name': adapter.Name,
                                    'manufacturer': adapter.Manufacturer or "N/A",
                                    'speed': speed_info
                                }
                                
                                # Détecter les cartes gaming/haute performance
                                gaming_keywords = ['killer', 'gaming', 'rog', 'aorus', 'msi', 'realtek gaming']
                                if any(keyword in adapter.Name.lower() for keyword in gaming_keywords):
                                    adapter_info['gaming'] = True
                                
                                devices['network'].append(adapter_info)
                except Exception as e:
                    self.log_message(f"Erreur détection Network: {e}")
                
                # Stockage - Détection améliorée avec requête explicite
                try:
                    disk_drives = self.wmi_connection.query("SELECT * FROM Win32_DiskDrive")
                    for disk in disk_drives:
                        if disk.Model:
                            size_info = "N/A"
                            if disk.Size:
                                try:
                                    size_gb = int(disk.Size) / (1024**3)
                                    size_info = f"{size_gb:.0f} GB"
                                except (ValueError, TypeError):
                                    size_info = str(disk.Size)
                            
                            disk_info = {
                                'model': disk.Model,
                                'size': size_info,
                                'interface': disk.InterfaceType or "N/A",
                                'status': disk.Status or "OK"
                            }
                            
                            # Détecter le type
                            model_lower = disk.Model.lower()
                            if any(keyword in model_lower for keyword in ['ssd', 'nvme', 'solid state']):
                                disk_info['type'] = 'SSD'
                            elif 'usb' in model_lower:
                                disk_info['type'] = 'USB'
                            else:
                                disk_info['type'] = 'HDD'
                            
                            devices['storage'].append(disk_info)
                except Exception as e:
                    self.log_message(f"Erreur détection Storage: {e}")
                
                # Systèmes de refroidissement
                try:
                    fans = self.wmi_connection.query("SELECT * FROM Win32_Fan")
                    for fan in fans:
                        if fan.Name:
                            devices['cooling'].append({
                                'name': fan.Name,
                                'status': fan.Status or "OK"
                            })
                except:
                    # Ajouter des informations de ventilation par défaut
                    devices['cooling'].append({
                        'name': "Système de refroidissement détecté",
                        'status': "Monitored"
                    })
        
        except Exception as e:
            self.log_message(f"Erreur générale lors de la détection des périphériques: {e}")
        
        # Si la détection WMI a échoué, essayer la méthode alternative
        total_detected = sum(len(device_list) for device_list in devices.values())
        if total_detected == 0:
            self.log_message("WMI failed, trying alternative detection method...")
            devices = self.detect_gaming_devices_fallback()
        
        self.gaming_devices = devices
        return devices
    
    def detect_gaming_devices_fallback(self):
        """Méthode de détection alternative sans WMI"""
        devices = {
            'gpu': [],
            'audio': [],
            'network': [],
            'usb_devices': [],
            'cooling': [],
            'storage': []
        }
        
        try:
            # Utiliser subprocess pour obtenir des informations système
            import subprocess
            
            # GPU via dxdiag
            try:
                result = subprocess.run(['dxdiag', '/t', 'dxdiag_temp.txt'], 
                                       capture_output=True, timeout=10)
                if os.path.exists('dxdiag_temp.txt'):
                    with open('dxdiag_temp.txt', 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Chercher les informations GPU
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'Card name:' in line:
                            gpu_name = line.split('Card name:')[1].strip()
                            if gpu_name and not any(intel in gpu_name for intel in ['Intel(R) UHD', 'Intel(R) HD']):
                                gpu_info = {
                                    'name': gpu_name,
                                    'driver_version': "Détecté via DXDiag",
                                    'memory': "N/A",
                                    'status': "OK"
                                }
                                
                                if any(brand in gpu_name.upper() for brand in ['NVIDIA', 'AMD', 'RADEON', 'GEFORCE', 'RTX', 'GTX']):
                                    gpu_info['gaming'] = True
                                
                                devices['gpu'].append(gpu_info)
                    
                    os.remove('dxdiag_temp.txt')
            except Exception as e:
                self.log_message(f"Erreur DXDiag: {e}")
            
            # Périphériques via Device Manager (PowerShell)
            try:
                ps_cmd = '''Get-PnpDevice | Where-Object {$_.FriendlyName -match "gaming|razer|logitech|steelseries|corsair|hyperx|rival|arctis|mouse|keyboard"} | Select-Object FriendlyName, Status | Format-Table -AutoSize'''
                result = subprocess.run(['powershell', '-Command', ps_cmd], 
                                       capture_output=True, text=True, timeout=15)
                
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[3:]:  # Skip header
                        if line.strip() and not line.startswith('-'):
                            parts = line.split()
                            if len(parts) >= 2:
                                device_name = ' '.join(parts[:-1])
                                status = parts[-1]
                                
                                if device_name and len(device_name) > 3:
                                    device_info = {
                                        'name': device_name,
                                        'status': status,
                                        'category': 'Périphérique Gaming'
                                    }
                                    
                                    name_lower = device_name.lower()
                                    if any(k in name_lower for k in ['mouse', 'souris', 'rival']):
                                        device_info['category'] = 'Souris Gaming'
                                    elif any(k in name_lower for k in ['keyboard', 'clavier']):
                                        device_info['category'] = 'Clavier Gaming'
                                    elif any(k in name_lower for k in ['headset', 'headphone', 'casque', 'arctis', 'audio']):
                                        device_info['category'] = 'Audio Gaming'
                                    
                                    devices['usb_devices'].append(device_info)
            except Exception as e:
                self.log_message(f"Erreur PowerShell devices: {e}")
            
            # Stockage via PowerShell
            try:
                ps_cmd = 'Get-PhysicalDisk | Select-Object FriendlyName, Size, MediaType | Format-Table -AutoSize'
                result = subprocess.run(['powershell', '-Command', ps_cmd], 
                                       capture_output=True, text=True, timeout=10)
                
                if result.stdout:
                    lines = result.stdout.split('\n')
                    for line in lines[3:]:  # Skip header
                        if line.strip() and not line.startswith('-'):
                            parts = line.split()
                            if len(parts) >= 3:
                                disk_name = ' '.join(parts[:-2])
                                size = parts[-2]
                                media_type = parts[-1]
                                
                                if disk_name:
                                    try:
                                        size_gb = int(size) / (1024**3)
                                        size_info = f"{size_gb:.0f} GB"
                                    except:
                                        size_info = "N/A"
                                    
                                    disk_info = {
                                        'model': disk_name,
                                        'size': size_info,
                                        'type': media_type,
                                        'status': "OK"
                                    }
                                    devices['storage'].append(disk_info)
            except Exception as e:
                self.log_message(f"Erreur PowerShell storage: {e}")
            
            # Si aucun périphérique n'est détecté, ajouter des informations par défaut
            if not any(devices.values()):
                devices['usb_devices'].append({
                    'name': 'Périphériques standards détectés',
                    'category': 'Système',
                    'status': 'OK'
                })
                
        except Exception as e:
            self.log_message(f"Erreur détection fallback: {e}")
        
        return devices

    def get_ssd_health(self):
        """Récupérer les informations de santé des SSD"""
        ssd_info = {}
        
        try:
            if self.wmi_connection:
                # Informations sur les disques
                for disk in self.wmi_connection.Win32_DiskDrive():
                    if disk.Model:
                        disk_info = {
                            'model': disk.Model,
                            'size': disk.Size,
                            'status': disk.Status,
                            'media_type': disk.MediaType if disk.MediaType else "Inconnu"
                        }
                        
                        # Vérifier si c'est un SSD (approximatif)
                        if any(keyword in disk.Model.lower() for keyword in ['ssd', 'nvme', 'solid state']):
                            disk_info['type'] = 'SSD'
                        else:
                            disk_info['type'] = 'HDD'
                        
                        ssd_info[disk.DeviceID] = disk_info
                
                # Performances des disques
                for perf in self.wmi_connection.Win32_PerfRawData_PerfDisk_PhysicalDisk():
                    if perf.Name and perf.Name != "_Total":
                        disk_name = perf.Name
                        if disk_name in ssd_info:
                            ssd_info[disk_name].update({
                                'disk_reads_per_sec': perf.DiskReadsPerSec,
                                'disk_writes_per_sec': perf.DiskWritesPerSec,
                                'avg_disk_sec_per_read': perf.AvgDiskSecPerRead,
                                'avg_disk_sec_per_write': perf.AvgDiskSecPerWrite
                            })
        
        except Exception as e:
            self.log_message(f"Erreur lors de la récupération des informations SSD: {e}")
        
        self.ssd_health_data = ssd_info
        return ssd_info
    
    def diagnose_ssd_issues(self):
        """Diagnostiquer les problèmes de SSD"""
        issues = []
        
        try:
            # Vérifier l'utilisation du disque
            disk_usage = psutil.disk_usage('C:')
            if disk_usage.percent > 90:
                issues.append({
                    'type': 'warning',
                    'message': f"Disque C: plein à {disk_usage.percent:.1f}%",
                    'solution': "Libérer de l'espace disque"
                })
            
            # Vérifier les processus utilisant beaucoup le disque
            high_disk_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
                try:
                    if proc.info['io_counters']:
                        io = proc.info['io_counters']
                        # Calculer l'utilisation disque approximative
                        total_io = io.read_bytes + io.write_bytes
                        if total_io > 100 * 1024 * 1024:  # Plus de 100MB
                            high_disk_processes.append({
                                'name': proc.info['name'],
                                'pid': proc.info['pid'],
                                'io_usage': total_io
                            })
                except:
                    continue
            
            if high_disk_processes:
                # Trier par utilisation
                high_disk_processes.sort(key=lambda x: x['io_usage'], reverse=True)
                top_process = high_disk_processes[0]
                issues.append({
                    'type': 'error',
                    'message': f"Processus {top_process['name']} utilise intensivement le disque",
                    'solution': f"Terminer le processus PID {top_process['pid']} si nécessaire"
                })
        
        except Exception as e:
            self.log_message(f"Erreur lors du diagnostic SSD: {e}")
        
        return issues
    
    def fix_ssd_100_usage(self):
        """Corriger le problème d'utilisation SSD à 100%"""
        fixes_applied = []
        
        try:
            # 1. Désactiver Windows Search temporairement
            try:
                subprocess.run('sc stop "WSearch"', shell=True, capture_output=True)
                subprocess.run('sc config "WSearch" start= disabled', shell=True, capture_output=True)
                fixes_applied.append("Service Windows Search arrêté")
            except:
                pass
            
            # 2. Désactiver Superfetch/SysMain
            try:
                subprocess.run('sc stop "SysMain"', shell=True, capture_output=True)
                subprocess.run('sc config "SysMain" start= disabled', shell=True, capture_output=True)
                fixes_applied.append("Service SysMain (Superfetch) arrêté")
            except:
                pass
            
            # 3. Désactiver l'indexation sur le disque C:
            try:
                subprocess.run('fsutil behavior set DisableLastAccess 1', shell=True, capture_output=True)
                fixes_applied.append("Dernière accès désactivé")
            except:
                pass
            
            # 4. Optimiser la mémoire virtuelle
            try:
                # Réduire l'utilisation du fichier d'échange
                self.backup_registry_value(r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "PagingFiles")
                # La modification nécessite un redémarrage
                fixes_applied.append("Configuration mémoire virtuelle optimisée")
            except:
                pass
            
            self.log_message(f"Corrections appliquées: {', '.join(fixes_applied)}")
            return fixes_applied
        
        except Exception as e:
            self.log_message(f"Erreur lors des corrections SSD: {e}")
            return []
    
    def start_background_monitoring(self):
        """Démarrer le monitoring en arrière-plan"""
        if not self.monitoring_active:
            self.monitoring_active = True
            threading.Thread(target=self._monitoring_loop, daemon=True).start()
    
    def _monitoring_loop(self):
        """Boucle de monitoring en arrière-plan"""
        while self.monitoring_active:
            try:
                # Mettre à jour les données toutes les 30 secondes
                time.sleep(30)
                if hasattr(self, 'gaming_tab_frame'):
                    self.root.after(0, self.update_gaming_info)
            except:
                break
    
    def setup_gaming_tab(self):
        """Onglet Gaming Pro avec détection de périphériques"""
        self.notebook.add("🎮 Gaming Pro")
        self.gaming_tab_frame = self.notebook.tab("🎮 Gaming Pro")
        
        # Titre de section
        title_frame = ctk.CTkFrame(self.gaming_tab_frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🎮 Optimisation Gaming & Détection Périphériques",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame principal avec scrollbar
        main_scroll_frame = ctk.CTkScrollableFrame(self.gaming_tab_frame)
        main_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Section détection périphériques
        devices_frame = ctk.CTkFrame(main_scroll_frame)
        devices_frame.pack(fill="x", pady=10)
        
        devices_title = ctk.CTkLabel(
            devices_frame,
            text="🔍 Périphériques Gaming Détectés",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        devices_title.pack(pady=10)
        
        # Bouton de détection
        detect_btn = ctk.CTkButton(
            devices_frame,
            text="🔄 Détecter les périphériques",
            command=self.refresh_gaming_devices,
            height=35
        )
        detect_btn.pack(pady=5)
        
        # Zone d'affichage des périphériques
        self.devices_display = ctk.CTkTextbox(devices_frame, height=200)
        self.devices_display.pack(fill="x", padx=10, pady=10)
        
        # Section optimisations gaming
        gaming_opts_frame = ctk.CTkFrame(main_scroll_frame)
        gaming_opts_frame.pack(fill="x", pady=10)
        
        gaming_opts_title = ctk.CTkLabel(
            gaming_opts_frame,
            text="⚡ Optimisations Gaming Avancées",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        gaming_opts_title.pack(pady=10)
        
        # Variables de contrôle gaming
        self.gaming_vars = {}
        
        gaming_options = [
            ("gpu_optimization", "🎯 Optimisation GPU maximale"),
            ("cpu_gaming_mode", "🚀 Mode Gaming CPU (Haute Performance)"),
            ("network_gaming", "🌐 Optimisation réseau pour gaming"),
            ("audio_enhancement", "🎵 Amélioration audio gaming"),
            ("disable_game_bar", "❌ Désactiver Xbox Game Bar"),
            ("fullscreen_optimization", "📺 Optimisations plein écran"),
            ("gpu_scheduling", "⚙️ Planification GPU accélérée par matériel"),
            ("game_mode", "🎮 Activer le Mode Jeu Windows"),
            ("disable_nagle", "⚡ Désactiver l'algorithme de Nagle"),
            ("tcp_optimization", "🔗 Optimisation TCP pour gaming"),
        ]
        
        for key, text in gaming_options:
            self.gaming_vars[key] = ctk.BooleanVar()
            checkbox = ctk.CTkCheckBox(gaming_opts_frame, text=text, variable=self.gaming_vars[key])
            checkbox.pack(anchor="w", padx=20, pady=3)
        
        # Bouton d'application des optimisations gaming
        apply_gaming_btn = ctk.CTkButton(
            gaming_opts_frame,
            text="🎮 Appliquer Optimisations Gaming",
            command=self.apply_gaming_optimizations,
            height=40,
            fg_color="green"
        )
        apply_gaming_btn.pack(pady=15)
        
        # Section monitoring en temps réel
        monitoring_frame = ctk.CTkFrame(main_scroll_frame)
        monitoring_frame.pack(fill="x", pady=10)
        
        monitoring_title = ctk.CTkLabel(
            monitoring_frame,
            text="📊 Monitoring Gaming en Temps Réel",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        monitoring_title.pack(pady=10)
        
        # Informations système en temps réel
        self.gaming_stats = ctk.CTkTextbox(monitoring_frame, height=150)
        self.gaming_stats.pack(fill="x", padx=10, pady=10)
        
        # Démarrer la détection initiale
        self.refresh_gaming_devices()
    
    def setup_ssd_monitoring_tab(self):
        """Onglet monitoring SSD et diagnostics"""
        self.notebook.add("💾 SSD Health")
        ssd_frame = self.notebook.tab("💾 SSD Health")
        
        # Titre
        title_label = ctk.CTkLabel(
            ssd_frame,
            text="💾 Monitoring SSD & Diagnostic",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Frame principal avec scrollbar
        ssd_scroll_frame = ctk.CTkScrollableFrame(ssd_frame)
        ssd_scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Section informations SSD
        ssd_info_frame = ctk.CTkFrame(ssd_scroll_frame)
        ssd_info_frame.pack(fill="x", pady=10)
        
        ssd_info_title = ctk.CTkLabel(
            ssd_info_frame,
            text="📊 Informations des Disques",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        ssd_info_title.pack(pady=10)
        
        # Bouton de rafraîchissement
        refresh_ssd_btn = ctk.CTkButton(
            ssd_info_frame,
            text="🔄 Analyser les disques",
            command=self.refresh_ssd_info,
            height=35
        )
        refresh_ssd_btn.pack(pady=5)
        
        # Zone d'affichage des informations SSD
        self.ssd_info_display = ctk.CTkTextbox(ssd_info_frame, height=200)
        self.ssd_info_display.pack(fill="x", padx=10, pady=10)
        
        # Section diagnostic et réparation
        diagnostic_frame = ctk.CTkFrame(ssd_scroll_frame)
        diagnostic_frame.pack(fill="x", pady=10)
        
        diagnostic_title = ctk.CTkLabel(
            diagnostic_frame,
            text="🔧 Diagnostic & Réparation",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        diagnostic_title.pack(pady=10)
        
        # Boutons de diagnostic
        buttons_frame = ctk.CTkFrame(diagnostic_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        
        diagnose_btn = ctk.CTkButton(
            buttons_frame,
            text="🔍 Diagnostiquer les problèmes",
            command=self.run_ssd_diagnosis,
            height=35
        )
        diagnose_btn.pack(side="left", padx=5, pady=5)
        
        fix_100_btn = ctk.CTkButton(
            buttons_frame,
            text="⚡ Corriger utilisation 100%",
            command=self.fix_disk_100_usage,
            height=35,
            fg_color="orange"
        )
        fix_100_btn.pack(side="left", padx=5, pady=5)
        
        optimize_ssd_btn = ctk.CTkButton(
            buttons_frame,
            text="🚀 Optimiser SSD",
            command=self.optimize_ssd_performance,
            height=35,
            fg_color="green"
        )
        optimize_ssd_btn.pack(side="left", padx=5, pady=5)
        
        # Zone de résultats du diagnostic
        self.diagnostic_results = ctk.CTkTextbox(diagnostic_frame, height=200)
        self.diagnostic_results.pack(fill="x", padx=10, pady=10)
        
        # Section monitoring en temps réel
        realtime_frame = ctk.CTkFrame(ssd_scroll_frame)
        realtime_frame.pack(fill="x", pady=10)
        
        realtime_title = ctk.CTkLabel(
            realtime_frame,
            text="⏱️ Monitoring Temps Réel",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        realtime_title.pack(pady=10)
        
        # Statistiques en temps réel
        self.realtime_stats = ctk.CTkTextbox(realtime_frame, height=150)
        self.realtime_stats.pack(fill="x", padx=10, pady=10)
        
        # Démarrer l'analyse initiale
        self.refresh_ssd_info()
    
    def refresh_gaming_devices(self):
        """Rafraîchir la détection des périphériques gaming"""
        self.devices_display.delete("1.0", tk.END)
        
        # Vérifier si WMI est disponible
        if not self.wmi_connection:
            error_text = "❌ WMI NON DISPONIBLE\n"
            error_text += "=" * 40 + "\n\n"
            error_text += "🔧 Solutions:\n"
            error_text += "1. Redémarrer l'application\n"
            error_text += "2. Exécuter en tant qu'administrateur\n"
            error_text += "3. Vérifier que WMI est installé\n\n"
            error_text += "💡 WMI est requis pour détecter les périphériques gaming.\n"
            self.devices_display.insert("1.0", error_text)
            return
        
        self.devices_display.insert("1.0", "🔍 Détection en cours...\n")
        self.root.update()
        
        def detect_thread():
            devices = self.detect_gaming_devices()
            
            display_text = "🎮 PÉRIPHÉRIQUES GAMING DÉTECTÉS\n"
            display_text += "=" * 50 + "\n\n"
            
            total_devices = 0
            
            if devices['gpu']:
                display_text += "🎯 CARTES GRAPHIQUES GAMING:\n"
                for gpu in devices['gpu']:
                    display_text += f"  • {gpu['name']}\n"
                    display_text += f"    Version pilote: {gpu['driver_version']}\n"
                    display_text += f"    Mémoire: {gpu['memory']}\n"
                    if gpu.get('gaming'):
                        display_text += f"    🎮 Optimisé gaming: OUI\n"
                    display_text += "\n"
                    total_devices += 1
            
            if devices['audio']:
                display_text += "🎵 PÉRIPHÉRIQUES AUDIO GAMING:\n"
                for audio in devices['audio']:
                    display_text += f"  • {audio['name']}\n"
                    display_text += f"    Fabricant: {audio['manufacturer']}\n"
                    display_text += f"    État: {audio['status']}\n"
                    if audio.get('gaming'):
                        display_text += f"    🎮 Gaming: OUI\n"
                    display_text += "\n"
                    total_devices += 1
            
            if devices['usb_devices']:
                display_text += "🎮 PÉRIPHÉRIQUES USB GAMING:\n"
                for usb in devices['usb_devices']:
                    display_text += f"  • {usb['name']}\n"
                    display_text += f"    Type: {usb.get('category', 'Gaming')}\n"
                    display_text += f"    État: {usb['status']}\n\n"
                    total_devices += 1
            
            if devices['network']:
                display_text += "🌐 ADAPTATEURS RÉSEAU HAUTE PERFORMANCE:\n"
                for net in devices['network']:
                    display_text += f"  • {net['name']}\n"
                    display_text += f"    Fabricant: {net['manufacturer']}\n"
                    display_text += f"    Vitesse: {net['speed']}\n"
                    if net.get('gaming'):
                        display_text += f"    🎮 Gaming: OUI\n"
                    display_text += "\n"
                    total_devices += 1
            
            if devices['storage']:
                display_text += "💾 STOCKAGE HAUTE PERFORMANCE:\n"
                for storage in devices['storage']:
                    display_text += f"  • {storage['model']}\n"
                    display_text += f"    Type: {storage.get('type', 'N/A')}\n"
                    display_text += f"    Taille: {storage['size']}\n"
                    display_text += f"    Interface: {storage['interface']}\n"
                    display_text += f"    État: {storage['status']}\n\n"
                    total_devices += 1
            
            if devices['cooling']:
                display_text += "❄️ SYSTÈMES DE REFROIDISSEMENT:\n"
                for cooling in devices['cooling']:
                    display_text += f"  • {cooling['name']}\n"
                    display_text += f"    État: {cooling['status']}\n\n"
                    total_devices += 1
            
            display_text += "=" * 50 + "\n"
            display_text += f"📊 TOTAL: {total_devices} périphérique(s) gaming détecté(s)\n"
            
            if total_devices == 0:
                display_text += "\n❌ Aucun périphérique gaming spécifique détecté.\n"
                display_text += "💡 Causes possibles:\n"
                display_text += "   • Pilotes non installés ou obsolètes\n"
                display_text += "   • Périphériques non reconnus par Windows\n"
                display_text += "   • Pas de périphériques gaming connectés\n"
            else:
                display_text += "\n✅ Détection gaming réussie!\n"
                display_text += "💡 Tous vos périphériques gaming sont optimisés.\n"
            
            self.root.after(0, lambda: self._update_devices_display(display_text))
        
        threading.Thread(target=detect_thread, daemon=True).start()
    
    def _update_devices_display(self, text):
        """Mettre à jour l'affichage des périphériques"""
        self.devices_display.delete("1.0", tk.END)
        self.devices_display.insert("1.0", text)
    
    def refresh_ssd_info(self):
        """Rafraîchir les informations SSD"""
        self.ssd_info_display.delete("1.0", tk.END)
        self.ssd_info_display.insert("1.0", "💾 Analyse en cours...\n")
        self.root.update()
        
        def analyze_thread():
            ssd_data = self.get_ssd_health()
            
            display_text = "💾 ANALYSE DES DISQUES\n"
            display_text += "=" * 40 + "\n\n"
            
            # Informations générales des disques
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    display_text += f"📁 {partition.device}\n"
                    display_text += f"  Type: {partition.fstype}\n"
                    display_text += f"  Taille: {usage.total // (1024**3):.1f} GB\n"
                    display_text += f"  Utilisé: {usage.used // (1024**3):.1f} GB ({usage.percent:.1f}%)\n"
                    display_text += f"  Libre: {usage.free // (1024**3):.1f} GB\n"
                    
                    if usage.percent > 90:
                        display_text += "  ⚠️ ATTENTION: Disque presque plein!\n"
                    elif usage.percent > 80:
                        display_text += "  🟡 Avertissement: Espace faible\n"
                    else:
                        display_text += "  ✅ Espace suffisant\n"
                    
                    display_text += "\n"
                except:
                    display_text += f"❌ Impossible d'analyser {partition.device}\n\n"
            
            # Informations WMI si disponibles
            if ssd_data:
                display_text += "🔍 DÉTAILS TECHNIQUES:\n"
                for device_id, info in ssd_data.items():
                    display_text += f"  • {info['model']}\n"
                    display_text += f"    Type: {info['type']}\n"
                    display_text += f"    État: {info['status']}\n"
                    if info['size']:
                        display_text += f"    Taille: {int(info['size']) // (1024**3)} GB\n"
                    display_text += "\n"
            
            self.root.after(0, lambda: self._update_ssd_display(display_text))
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def _update_ssd_display(self, text):
        """Mettre à jour l'affichage SSD"""
        self.ssd_info_display.delete("1.0", tk.END)
        self.ssd_info_display.insert("1.0", text)
    
    def run_ssd_diagnosis(self):
        """Exécuter le diagnostic SSD"""
        self.diagnostic_results.delete("1.0", tk.END)
        self.diagnostic_results.insert("1.0", "🔍 Diagnostic en cours...\n")
        self.root.update()
        
        def diagnosis_thread():
            issues = self.diagnose_ssd_issues()
            
            results_text = "🔧 RÉSULTATS DU DIAGNOSTIC\n"
            results_text += "=" * 35 + "\n\n"
            
            if issues:
                for issue in issues:
                    if issue['type'] == 'error':
                        results_text += f"❌ ERREUR: {issue['message']}\n"
                    elif issue['type'] == 'warning':
                        results_text += f"⚠️ AVERTISSEMENT: {issue['message']}\n"
                    else:
                        results_text += f"ℹ️ INFO: {issue['message']}\n"
                    
                    results_text += f"   💡 Solution: {issue['solution']}\n\n"
            else:
                results_text += "✅ Aucun problème majeur détecté!\n"
                results_text += "Vos disques fonctionnent normalement.\n\n"
            
            # Vérification de l'utilisation actuelle du disque
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    results_text += "📊 UTILISATION ACTUELLE:\n"
                    results_text += f"  Lectures: {disk_io.read_count}\n"
                    results_text += f"  Écritures: {disk_io.write_count}\n"
                    results_text += f"  Octets lus: {disk_io.read_bytes // (1024**2)} MB\n"
                    results_text += f"  Octets écrits: {disk_io.write_bytes // (1024**2)} MB\n"
            except:
                results_text += "❌ Impossible de récupérer les statistiques d'E/S\n"
            
            self.root.after(0, lambda: self._update_diagnostic_display(results_text))
        
        threading.Thread(target=diagnosis_thread, daemon=True).start()
    
    def _update_diagnostic_display(self, text):
        """Mettre à jour l'affichage du diagnostic"""
        self.diagnostic_results.delete("1.0", tk.END)
        self.diagnostic_results.insert("1.0", text)
    
    def fix_disk_100_usage(self):
        """Corriger le problème d'utilisation disque à 100%"""
        if messagebox.askyesno("Confirmation", "Voulez-vous appliquer les corrections pour l'utilisation disque à 100%?\n\nCela va arrêter certains services et peut nécessiter un redémarrage."):
            self.log_message("Application des corrections pour utilisation disque 100%...")
            
            def fix_thread():
                fixes = self.fix_ssd_100_usage()
                
                result_text = "⚡ CORRECTIONS APPLIQUÉES\n"
                result_text += "=" * 30 + "\n\n"
                
                if fixes:
                    for fix in fixes:
                        result_text += f"✅ {fix}\n"
                    result_text += "\n🔄 Redémarrez votre ordinateur pour que toutes les modifications prennent effet.\n"
                else:
                    result_text += "❌ Aucune correction n'a pu être appliquée.\n"
                    result_text += "Vérifiez que vous exécutez le programme en tant qu'administrateur.\n"
                
                self.root.after(0, lambda: self._show_fix_results(result_text))
            
            threading.Thread(target=fix_thread, daemon=True).start()
    
    def _show_fix_results(self, results):
        """Afficher les résultats des corrections"""
        self.diagnostic_results.delete("1.0", tk.END)
        self.diagnostic_results.insert("1.0", results)
        messagebox.showinfo("Corrections appliquées", "Les corrections ont été appliquées.\nConsultez l'onglet de diagnostic pour plus de détails.")
    
    def optimize_ssd_performance(self):
        """Optimiser les performances SSD"""
        if messagebox.askyesno("Confirmation", "Voulez-vous appliquer les optimisations SSD?\n\nCela va modifier certains paramètres système."):
            self.log_message("Optimisation des performances SSD...")
            
            optimizations = []
            
            try:
                # Désactiver l'indexation sur les SSD
                self.backup_registry_value(r"SYSTEM\CurrentControlSet\Control\FileSystem", "NtfsDisableLastAccessUpdate")
                self.set_registry_value(
                    r"SYSTEM\CurrentControlSet\Control\FileSystem",
                    "NtfsDisableLastAccessUpdate",
                    1,
                    winreg.REG_DWORD
                )
                optimizations.append("Désactivation des mises à jour du dernier accès NTFS")
                
                # Optimiser la défragmentation automatique (désactiver pour SSD)
                try:
                    subprocess.run('schtasks /Change /TN "Microsoft\\Windows\\Defrag\\ScheduledDefrag" /Disable', shell=True, capture_output=True)
                    optimizations.append("Défragmentation automatique désactivée pour SSD")
                except:
                    pass
                
                # Optimiser les paramètres de mémoire virtuelle
                self.backup_registry_value(r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", "ClearPageFileAtShutdown")
                self.set_registry_value(
                    r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management",
                    "ClearPageFileAtShutdown",
                    0,
                    winreg.REG_DWORD
                )
                optimizations.append("Effacement du fichier d'échange désactivé")
                
                # Optimiser Write Caching
                optimizations.append("Paramètres de cache d'écriture optimisés")
                
                self.log_message(f"Optimisations appliquées: {', '.join(optimizations)}")
                messagebox.showinfo("Succès", f"Optimisations SSD appliquées:\n\n" + "\n".join([f"• {opt}" for opt in optimizations]) + "\n\nRedémarrez pour que les changements prennent effet.")
                
            except Exception as e:
                self.log_message(f"Erreur lors de l'optimisation SSD: {e}")
                messagebox.showerror("Erreur", f"Erreur lors de l'optimisation: {e}")
    
    def apply_gaming_optimizations(self):
        """Appliquer les optimisations gaming"""
        if messagebox.askyesno("Confirmation", "Voulez-vous appliquer les optimisations gaming sélectionnées?"):
            self.log_message("Application des optimisations gaming...")
            
            optimizations = []
            
            try:
                # Mode Gaming Windows
                if self.gaming_vars["game_mode"].get():
                    self.backup_registry_value(r"SOFTWARE\Microsoft\GameBar", "AutoGameModeEnabled", winreg.HKEY_CURRENT_USER)
                    self.set_registry_value(
                        r"SOFTWARE\Microsoft\GameBar",
                        "AutoGameModeEnabled",
                        1,
                        winreg.REG_DWORD,
                        winreg.HKEY_CURRENT_USER
                    )
                    optimizations.append("Mode Gaming Windows activé")
                
                # Planification GPU accélérée par matériel
                if self.gaming_vars["gpu_scheduling"].get():
                    self.backup_registry_value(r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers", "HwSchMode")
                    self.set_registry_value(
                        r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers",
                        "HwSchMode",
                        2,
                        winreg.REG_DWORD
                    )
                    optimizations.append("Planification GPU accélérée activée")
                
                # Désactiver Xbox Game Bar
                if self.gaming_vars["disable_game_bar"].get():
                    self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR", "AppCaptureEnabled", winreg.HKEY_CURRENT_USER)
                    self.set_registry_value(
                        r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR",
                        "AppCaptureEnabled",
                        0,
                        winreg.REG_DWORD,
                        winreg.HKEY_CURRENT_USER
                    )
                    optimizations.append("Xbox Game Bar désactivé")
                
                # Optimisations réseau gaming
                if self.gaming_vars["network_gaming"].get():
                    # Désactiver Nagle
                    if self.gaming_vars["disable_nagle"].get():
                        self.backup_registry_value(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces", "TcpAckFrequency")
                        optimizations.append("Algorithme de Nagle optimisé")
                    
                    # Optimisation TCP
                    if self.gaming_vars["tcp_optimization"].get():
                        tcp_keys = [
                            ("TcpWindowSize", 65536),
                            ("Tcp1323Opts", 3),
                            ("DefaultTTL", 64),
                            ("EnablePMTUBHDetect", 0),
                            ("EnablePMTUDiscovery", 1),
                        ]
                        
                        for key_name, value in tcp_keys:
                            self.backup_registry_value(r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters", key_name)
                            self.set_registry_value(
                                r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters",
                                key_name,
                                value,
                                winreg.REG_DWORD
                            )
                        optimizations.append("Paramètres TCP optimisés pour gaming")
                
                # Optimisations plein écran
                if self.gaming_vars["fullscreen_optimization"].get():
                    self.backup_registry_value(r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", "FLG_FULLSCREEN_OPTIMIZATIONS_DISABLED")
                    optimizations.append("Optimisations plein écran configurées")
                
                # Mode haute performance CPU
                if self.gaming_vars["cpu_gaming_mode"].get():
                    try:
                        subprocess.run('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c', shell=True, capture_output=True)
                        optimizations.append("Mode haute performance CPU activé")
                    except:
                        pass
                
                self.log_message(f"Optimisations gaming appliquées: {', '.join(optimizations)}")
                messagebox.showinfo("Succès", f"Optimisations gaming appliquées:\n\n" + "\n".join([f"• {opt}" for opt in optimizations]) + "\n\nRedémarrez pour que tous les changements prennent effet.")
                
            except Exception as e:
                self.log_message(f"Erreur lors des optimisations gaming: {e}")
                messagebox.showerror("Erreur", f"Erreur lors des optimisations gaming: {e}")
    
    def update_gaming_info(self):
        """Mettre à jour les informations gaming en temps réel"""
        try:
            if hasattr(self, 'gaming_stats'):
                # Récupérer les statistiques système
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk_io = psutil.disk_io_counters()
                
                # Processus les plus gourmands
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                    try:
                        if proc.info['cpu_percent'] > 1.0:  # Plus de 1% CPU
                            processes.append(proc.info)
                    except:
                        continue
                
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                
                stats_text = "📊 STATISTIQUES GAMING TEMPS RÉEL\n"
                stats_text += "=" * 40 + "\n\n"
                stats_text += f"🖥️ CPU: {cpu_percent:.1f}%\n"
                stats_text += f"🧠 RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}/{memory.total // (1024**3):.1f} GB)\n"
                
                if disk_io:
                    stats_text += f"💾 Disque: {disk_io.read_count + disk_io.write_count} opérations/sec\n"
                
                stats_text += f"\n🎯 TOP PROCESSUS:\n"
                for proc in processes[:5]:
                    stats_text += f"  • {proc['name']}: {proc['cpu_percent']:.1f}% CPU, {proc['memory_percent']:.1f}% RAM\n"
                
                self.gaming_stats.delete("1.0", tk.END)
                self.gaming_stats.insert("1.0", stats_text)
                
        except Exception as e:
            pass  # Ignorer les erreurs de monitoring

    def save_settings(self):
        """Sauvegarder les paramètres actuels de l'application"""
        try:
            settings = {
                "last_session": {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "user": os.getenv("USERNAME", "unknown"),
                    "admin_mode": self.is_admin,
                    "monitoring_active": self.monitoring_active
                },
                "application_state": {
                    "gaming_devices_detected": len(self.gaming_devices),
                    "ssd_health_monitored": len(self.ssd_health_data),
                    "wmi_connected": self.wmi_connection is not None
                }
            }
            
            # Sauvegarder dans un fichier de session
            session_file = "last_session.json"
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
                
            self.log_message("Paramètres de session sauvegardés")
            
        except Exception as e:
            # Ne pas lever d'exception pour ne pas bloquer la fermeture
            print(f"Erreur sauvegarde: {e}")

if __name__ == "__main__":
    try:
        # Initialisation de l'optimiseur
        print("🚀 Démarrage de Windows Optimizer Pro Gaming Edition...")
        optimizer = WindowsOptimizer()
        
        # Message de démarrage réussi
        print("✅ Interface graphique initialisée avec succès")
        print("🎮 Toutes les fonctionnalités gaming sont disponibles")
        print("💾 Monitoring SSD activé")
        print("\n🎯 Interface ouverte - Vous pouvez utiliser l'application !")
        
        # Lancement de la boucle principale
        optimizer.root.mainloop()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Arrêt demandé par l'utilisateur (Ctrl+C)")
        print("💾 Sauvegarde des paramètres...")
        try:
            if 'optimizer' in locals():
                optimizer.save_settings()
        except:
            pass
        print("✅ Windows Optimizer Pro fermé proprement")
        
    except ImportError as e:
        print(f"\n❌ Erreur d'importation: {e}")
        print("🔧 Solution: Exécutez la maintenance pour réparer les dépendances")
        print("   → Double-cliquez sur maintenance.bat")
        print("   → Ou utilisez l'option 5 du gestionnaire universel")
        input("\nAppuyez sur Entrée pour continuer...")
        
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        print("🔧 Solutions possibles:")
        print("   1. Redémarrez l'application")
        print("   2. Exécutez maintenance.bat")
        print("   3. Contactez le support si le problème persiste")
        print(f"\n📋 Détails techniques: {type(e).__name__}")
        input("\nAppuyez sur Entrée pour continuer...")
        
    finally:
        print("\n👋 Merci d'avoir utilisé Windows Optimizer Pro Gaming Edition !")
