#!/usr/bin/env python3
"""
Windows Optimizer Python Version
Version avancée de l'optimiseur Windows avec interface graphique moderne
Inclut une fonction de restauration des paramètres d'origine
"""

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

class WindowsOptimizer:
    def __init__(self):
        # Configuration de l'apparence
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Fenêtre principale
        self.root = ctk.CTk()
        self.root.title("Windows Optimizer Python - v1.0")
        self.root.geometry("1000x700")
        self.root.iconbitmap("optimizer.ico") if os.path.exists("optimizer.ico") else None
        
        # Variables
        self.backup_file = "optimizer_backup.json"
        self.original_settings = {}
        self.is_admin = self.check_admin()
        
        # Interface utilisateur
        self.setup_ui()
        
        # Charger la sauvegarde si elle existe
        self.load_backup()
        
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
        🚀 Windows Optimizer Python v1.0
        
        Version Python de l'optimiseur Windows avec interface moderne.
        
        Fonctionnalités:
        • Optimisations de performance
        • Protection de la confidentialité
        • Gestion des services Windows
        • Nettoyage système
        • Restauration des paramètres d'origine
        
        ⚠️ Attention: Utilisez cet outil avec précaution.
        Créez toujours une sauvegarde avant d'appliquer des modifications.
        
        Basé sur le projet Optimizer original de hellzerg.
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
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
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
    
    def run(self):
        """Lancer l'application"""
        self.log_message("Windows Optimizer Python démarré")
        self.log_message("Sélectionnez les optimisations désirées et cliquez sur 'Appliquer'")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        import ctypes
        app = WindowsOptimizer()
        app.run()
    except ImportError as e:
        print(f"Erreur d'importation: {e}")
        print("Installez les dépendances avec: pip install -r requirements.txt")
    except Exception as e:
        print(f"Erreur: {e}")
