#!/usr/bin/env python3
"""
Script de restauration des paramètres Windows par défaut
Restaure les paramètres d'origine de Windows sans dépendre d'une sauvegarde
"""

import winreg
import subprocess
import sys
import os
from datetime import datetime

class WindowsDefaultsRestorer:
    def __init__(self):
        self.restored_count = 0
        self.error_count = 0
        
    def log(self, message):
        """Afficher un message avec horodatage"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def set_registry_value(self, key_path, value_name, value, reg_type, hkey=winreg.HKEY_LOCAL_MACHINE):
        """Définir une valeur de registre"""
        try:
            with winreg.CreateKey(hkey, key_path) as key:
                winreg.SetValueEx(key, value_name, 0, reg_type, value)
            return True
        except Exception as e:
            self.log(f"Erreur registre {key_path}\\{value_name}: {e}")
            self.error_count += 1
            return False
    
    def delete_registry_value(self, key_path, value_name, hkey=winreg.HKEY_LOCAL_MACHINE):
        """Supprimer une valeur de registre"""
        try:
            with winreg.OpenKey(hkey, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
            return True
        except:
            return False
    
    def enable_service(self, service_name):
        """Activer et démarrer un service"""
        try:
            # Configurer le service en automatique
            subprocess.run(f'sc config "{service_name}" start= auto', 
                         shell=True, capture_output=True, check=False)
            # Démarrer le service
            subprocess.run(f'sc start "{service_name}"', 
                         shell=True, capture_output=True, check=False)
            self.log(f"Service {service_name} activé")
            self.restored_count += 1
            return True
        except:
            self.log(f"Impossible d'activer le service {service_name}")
            self.error_count += 1
            return False
    
    def restore_telemetry_settings(self):
        """Restaurer les paramètres de télémétrie par défaut"""
        self.log("Restauration des paramètres de télémétrie...")
        
        # Restaurer la télémétrie Windows (valeur par défaut : 3 pour Windows 10/11)
        if self.set_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "AllowTelemetry",
            3,  # Télémétrie complète (par défaut)
            winreg.REG_DWORD
        ):
            self.restored_count += 1
        
        # Supprimer les restrictions de télémétrie
        self.delete_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\DataCollection",
            "AllowTelemetry"
        )
        
        # Réactiver les services de télémétrie
        telemetry_services = [
            "DiagTrack",
            "dmwappushservice",
            "diagnosticshub.standardcollector.service"
        ]
        
        for service in telemetry_services:
            self.enable_service(service)
    
    def restore_privacy_settings(self):
        """Restaurer les paramètres de confidentialité par défaut"""
        self.log("Restauration des paramètres de confidentialité...")
        
        # Réactiver l'ID publicitaire
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\AdvertisingInfo",
            "Enabled",
            1,
            winreg.REG_DWORD,
            winreg.HKEY_CURRENT_USER
        ):
            self.restored_count += 1
        
        # Réactiver les services de localisation
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\location",
            "Value",
            "Allow",
            winreg.REG_SZ
        ):
            self.restored_count += 1
        
        # Réactiver les expériences personnalisées
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Privacy",
            "TailoredExperiencesWithDiagnosticDataEnabled",
            1,
            winreg.REG_DWORD,
            winreg.HKEY_CURRENT_USER
        ):
            self.restored_count += 1
        
        # Réactiver Cortana
        if self.set_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\Windows Search",
            "AllowCortana",
            1,
            winreg.REG_DWORD
        ):
            self.restored_count += 1
    
    def restore_performance_settings(self):
        """Restaurer les paramètres de performance par défaut"""
        self.log("Restauration des paramètres de performance...")
        
        # Restaurer les effets visuels (par défaut : laisser Windows choisir)
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",
            "VisualFXSetting",
            0,  # Laisser Windows choisir
            winreg.REG_DWORD,
            winreg.HKEY_CURRENT_USER
        ):
            self.restored_count += 1
        
        # Restaurer le délai de démarrage par défaut
        self.delete_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Serialize",
            "StartupDelayInMSec",
            winreg.HKEY_CURRENT_USER
        )
        
        # Restaurer les paramètres de jeu par défaut
        gaming_defaults = [
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile", "SystemResponsiveness", 20),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "GPU Priority", 2),
            (r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile\Tasks\Games", "Priority", 2),
        ]
        
        for key_path, value_name, default_value in gaming_defaults:
            if self.set_registry_value(key_path, value_name, default_value, winreg.REG_DWORD):
                self.restored_count += 1
    
    def restore_windows_services(self):
        """Restaurer les services Windows par défaut"""
        self.log("Restauration des services Windows...")
        
        # Services importants à réactiver
        important_services = [
            "WSearch",  # Windows Search
            "Themes",   # Thèmes Windows
            "Spooler",  # Spouleur d'impression
            "BITS",     # Service de transfert intelligent
            "wuauserv", # Windows Update
            "SysMain",  # Superfetch/Sysmain
        ]
        
        for service in important_services:
            self.enable_service(service)
    
    def restore_windows_features(self):
        """Restaurer les fonctionnalités Windows"""
        self.log("Restauration des fonctionnalités Windows...")
        
        # Réactiver Windows Defender (si désactivé)
        defender_keys = [
            (r"SOFTWARE\Policies\Microsoft\Windows Defender", "DisableAntiSpyware", 0),
            (r"SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection", "DisableRealtimeMonitoring", 0),
        ]
        
        for key_path, value_name, value in defender_keys:
            if self.set_registry_value(key_path, value_name, value, winreg.REG_DWORD):
                self.restored_count += 1
        
        # Réactiver Windows Update
        if self.set_registry_value(
            r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU",
            "NoAutoUpdate",
            0,
            winreg.REG_DWORD
        ):
            self.restored_count += 1
    
    def restore_ui_settings(self):
        """Restaurer les paramètres d'interface utilisateur"""
        self.log("Restauration des paramètres d'interface...")
        
        # Restaurer l'affichage des extensions de fichiers (masquer par défaut)
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "HideFileExt",
            1,  # Masquer les extensions (par défaut)
            winreg.REG_DWORD,
            winreg.HKEY_CURRENT_USER
        ):
            self.restored_count += 1
        
        # Restaurer l'affichage des fichiers cachés (masquer par défaut)
        if self.set_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "Hidden",
            2,  # Ne pas afficher les fichiers cachés (par défaut)
            winreg.REG_DWORD,
            winreg.HKEY_CURRENT_USER
        ):
            self.restored_count += 1
        
        # Réactiver le tremblement pour minimiser
        self.delete_registry_value(
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced",
            "DisallowShaking",
            winreg.HKEY_CURRENT_USER
        )
    
    def restore_all_defaults(self):
        """Restaurer tous les paramètres Windows par défaut"""
        self.log("=== DÉBUT DE LA RESTAURATION DES PARAMÈTRES PAR DÉFAUT ===")
        self.log("ATTENTION: Cette opération va restaurer Windows à ses paramètres d'origine")
        
        try:
            # Vérifier les privilèges administrateur
            import ctypes
            if not ctypes.windll.shell32.IsUserAnAdmin():
                self.log("ERREUR: Privilèges administrateur requis!")
                return False
            
            # Restaurer chaque catégorie
            self.restore_telemetry_settings()
            self.restore_privacy_settings()
            self.restore_performance_settings()
            self.restore_windows_services()
            self.restore_windows_features()
            self.restore_ui_settings()
            
            self.log("=== RESTAURATION TERMINÉE ===")
            self.log(f"✅ {self.restored_count} paramètres restaurés")
            self.log(f"❌ {self.error_count} erreurs rencontrées")
            
            if self.restored_count > 0:
                self.log("🔄 REDÉMARRAGE RECOMMANDÉ pour que tous les changements prennent effet")
                return True
            else:
                self.log("Aucun paramètre n'a été restauré")
                return False
                
        except Exception as e:
            self.log(f"ERREUR CRITIQUE: {e}")
            return False

def main():
    """Fonction principale"""
    print("=" * 60)
    print("  RESTAURATION DES PARAMÈTRES WINDOWS PAR DÉFAUT")
    print("=" * 60)
    print()
    print("Ce script va restaurer Windows à ses paramètres d'origine.")
    print("ATTENTION: Cela annulera toutes les optimisations précédentes!")
    print()
    
    # Demander confirmation
    response = input("Voulez-vous continuer? (oui/non): ").lower().strip()
    if response not in ['oui', 'o', 'yes', 'y']:
        print("Opération annulée.")
        return
    
    print()
    
    # Créer et exécuter le restaurateur
    restorer = WindowsDefaultsRestorer()
    success = restorer.restore_all_defaults()
    
    print()
    if success:
        print("🎉 RESTAURATION RÉUSSIE!")
        print("Redémarrez votre ordinateur pour finaliser les changements.")
    else:
        print("⚠️  RESTAURATION INCOMPLÈTE")
        print("Certains paramètres n'ont pas pu être restaurés.")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
