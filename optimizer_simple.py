#!/usr/bin/env python3
"""
Windows Optimizer Python - Version Simple
Utilise uniquement les modules Python standard
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import winreg
import subprocess
import os
import json
import threading
from datetime import datetime

class SimpleWindowsOptimizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Windows Optimizer Python - Version Simple")
        self.root.geometry("800x600")
        
        self.backup_file = "optimizer_backup.json"
        self.original_settings = {}
        
        self.setup_ui()
        self.load_backup()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre
        title_label = tk.Label(main_frame, text="🚀 Windows Optimizer Python", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Onglets
        self.setup_performance_tab()
        self.setup_restore_tab()
        
        # Boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.apply_btn = tk.Button(button_frame, text="🔧 Appliquer", 
                                  command=self.apply_optimizations,
                                  bg="lightblue", font=("Arial", 12, "bold"))
        self.apply_btn.pack(side="left", padx=10)
        
        self.restore_btn = tk.Button(button_frame, text="🔄 Restaurer", 
                                    command=self.restore_original_settings,
                                    bg="orange", font=("Arial", 12, "bold"))
        self.restore_btn.pack(side="right", padx=10)
        
        # Log
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10)
        self.log_text.pack(fill="x", pady=10)
        
    def setup_performance_tab(self):
        perf_frame = ttk.Frame(self.notebook)
        self.notebook.add(perf_frame, text="🚀 Performance")
        
        self.perf_vars = {}
        options = [
            ("disable_telemetry", "Désactiver la télémétrie Windows"),
            ("optimize_visual", "Optimiser les effets visuels"),
            ("disable_startup_delay", "Supprimer le délai de démarrage"),
            ("optimize_gaming", "Optimisations pour les jeux"),
        ]
        
        for key, text in options:
            self.perf_vars[key] = tk.BooleanVar()
            cb = tk.Checkbutton(perf_frame, text=text, variable=self.perf_vars[key])
            cb.pack(anchor="w", padx=20, pady=5)
    
    def setup_restore_tab(self):
        restore_frame = ttk.Frame(self.notebook)
        self.notebook.add(restore_frame, text="🔄 Restauration")
        
        info_label = tk.Label(restore_frame, 
                             text="Restauration des paramètres Windows d'origine",
                             font=("Arial", 12))
        info_label.pack(pady=20)
        
        if os.path.exists(self.backup_file):
            backup_label = tk.Label(restore_frame, text="✅ Sauvegarde trouvée", fg="green")
        else:
            backup_label = tk.Label(restore_frame, text="❌ Aucune sauvegarde", fg="red")
        backup_label.pack(pady=10)
        
        restore_all_btn = tk.Button(restore_frame, text="🔄 Restaurer tout",
                                   command=self.restore_all_settings,
                                   bg="lightgreen", font=("Arial", 11, "bold"))
        restore_all_btn.pack(pady=10)
        
        backup_btn = tk.Button(restore_frame, text="💾 Créer sauvegarde",
                              command=self.create_manual_backup,
                              bg="lightgray", font=("Arial", 11, "bold"))
        backup_btn.pack(pady=10)
    
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def backup_registry_value(self, key_path, value_name, hkey=winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.OpenKey(hkey, key_path) as key:
                value, reg_type = winreg.QueryValueEx(key, value_name)
                backup_key = f"{hkey}\\{key_path}\\{value_name}"
                self.original_settings[backup_key] = {
                    "value": value, "type": reg_type, "hkey": hkey
                }
                return True
        except:
            return False
    
    def set_registry_value(self, key_path, value_name, value, reg_type, hkey=winreg.HKEY_LOCAL_MACHINE):
        try:
            with winreg.CreateKey(hkey, key_path) as key:
                winreg.SetValueEx(key, value_name, 0, reg_type, value)
            return True
        except Exception as e:
            self.log_message(f"Erreur registre: {e}")
            return False
    
    def disable_telemetry(self):
        self.log_message("Désactivation de la télémétrie...")
        self.backup_registry_value(r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry")
        self.set_registry_value(r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
                               "AllowTelemetry", 0, winreg.REG_DWORD)
        
        services = ["DiagTrack", "dmwappushservice"]
        for service in services:
            try:
                subprocess.run(f'sc stop "{service}"', shell=True, capture_output=True)
                subprocess.run(f'sc config "{service}" start= disabled', shell=True, capture_output=True)
                self.log_message(f"Service {service} désactivé")
            except:
                pass
    
    def optimize_performance(self):
        self.log_message("Optimisation des performances...")
        
        if self.perf_vars["optimize_visual"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", 
                                     "VisualFXSetting", winreg.HKEY_CURRENT_USER)
            self.set_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
                                   "VisualFXSetting", 2, winreg.REG_DWORD, winreg.HKEY_CURRENT_USER)
        
        if self.perf_vars["disable_startup_delay"].get():
            self.backup_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
                                     "StartupDelayInMSec", winreg.HKEY_CURRENT_USER)
            self.set_registry_value(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
                                   "StartupDelayInMSec", 0, winreg.REG_DWORD, winreg.HKEY_CURRENT_USER)
        
        if self.perf_vars["optimize_gaming"].get():
            gaming_tweaks = [
                (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 1),
                (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 8),
            ]
            for key_path, value_name, value in gaming_tweaks:
                self.backup_registry_value(key_path, value_name)
                self.set_registry_value(key_path, value_name, value, winreg.REG_DWORD)
    
    def save_backup(self):
        try:
            with open(self.backup_file, 'w') as f:
                json.dump(self.original_settings, f, indent=2)
            self.log_message(f"Sauvegarde créée: {self.backup_file}")
        except Exception as e:
            self.log_message(f"Erreur sauvegarde: {e}")
    
    def load_backup(self):
        try:
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r') as f:
                    self.original_settings = json.load(f)
                self.log_message("Sauvegarde chargée")
        except Exception as e:
            self.log_message(f"Erreur chargement: {e}")
    
    def restore_original_settings(self):
        if not self.original_settings:
            messagebox.showwarning("Attention", "Aucune sauvegarde trouvée!")
            return
        
        if messagebox.askyesno("Confirmation", "Restaurer les paramètres d'origine?"):
            self.log_message("Restauration en cours...")
            
            for backup_key, backup_data in self.original_settings.items():
                try:
                    parts = backup_key.split("\\")
                    hkey = backup_data["hkey"]
                    key_path = "\\".join(parts[1:-1])
                    value_name = parts[-1]
                    
                    self.set_registry_value(key_path, value_name, backup_data["value"],
                                          backup_data["type"], hkey)
                except Exception as e:
                    self.log_message(f"Erreur restauration {backup_key}: {e}")
            
            self.log_message("Restauration terminée")
            messagebox.showinfo("Succès", "Paramètres restaurés!")
    
    def restore_all_settings(self):
        self.restore_original_settings()
    
    def create_manual_backup(self):
        self.log_message("Création sauvegarde manuelle...")
        
        important_keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Policies\Microsoft\Windows\DataCollection", "AllowTelemetry"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects", "VisualFXSetting"),
        ]
        
        for hkey, key_path, value_name in important_keys:
            self.backup_registry_value(key_path, value_name, hkey)
        
        self.save_backup()
        messagebox.showinfo("Succès", "Sauvegarde créée!")
    
    def apply_optimizations(self):
        if messagebox.askyesno("Confirmation", "Appliquer les optimisations?"):
            self.log_message("=== DÉBUT OPTIMISATIONS ===")
            
            if not os.path.exists(self.backup_file):
                self.create_manual_backup()
            
            threading.Thread(target=self._apply_optimizations_thread, daemon=True).start()
    
    def _apply_optimizations_thread(self):
        try:
            if self.perf_vars["disable_telemetry"].get():
                self.disable_telemetry()
            
            self.optimize_performance()
            
            self.log_message("=== OPTIMISATIONS TERMINÉES ===")
            self.root.after(0, lambda: messagebox.showinfo("Succès", "Optimisations appliquées!"))
            
        except Exception as e:
            self.log_message(f"Erreur: {e}")
            self.root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur: {e}"))
    
    def run(self):
        self.log_message("Windows Optimizer Python démarré")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = SimpleWindowsOptimizer()
        app.run()
    except Exception as e:
        print(f"Erreur: {e}")
        input("Appuyez sur Entrée pour quitter...")
