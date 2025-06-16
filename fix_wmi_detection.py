"""
🔧 Fix WMI Detection - Windows Optimizer Pro
Diagnostic et correction des erreurs WMI COM (-2147352567)
"""

import subprocess
import sys
import time
import wmi
import logging
from pathlib import Path

# Configuration du logging
log_file = Path(__file__).parent / "wmi_diagnostic.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def check_admin_rights():
    """Vérifier si le script est exécuté en tant qu'administrateur"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def repair_wmi_service():
    """Réparer le service WMI"""
    logging.info("🔧 Réparation du service WMI...")
    
    commands = [
        # Arrêter le service WMI
        "net stop winmgmt /y",
        # Reconstruire le repository WMI
        "winmgmt /resetrepository",
        # Redémarrer le service
        "net start winmgmt",
        # Synchroniser les fournisseurs WMI
        "winmgmt /resyncperf"
    ]
    
    for cmd in commands:
        try:
            logging.info(f"Exécution: {cmd}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"✅ Succès: {cmd}")
            else:
                logging.warning(f"⚠️  Erreur: {cmd} - {result.stderr}")
        except Exception as e:
            logging.error(f"❌ Exception: {cmd} - {e}")
        
        time.sleep(2)

def test_wmi_connection():
    """Tester la connexion WMI avec différentes méthodes"""
    logging.info("🧪 Test de connexion WMI...")
    
    # Test 1: Connexion WMI standard
    try:
        c = wmi.WMI()
        logging.info("✅ Test 1: Connexion WMI standard - OK")
        return True
    except Exception as e:
        logging.error(f"❌ Test 1: Connexion WMI standard - {e}")
    
    # Test 2: Connexion avec namespace spécifique
    try:
        c = wmi.WMI(namespace="root/cimv2")
        logging.info("✅ Test 2: Connexion namespace root/cimv2 - OK")
        return True
    except Exception as e:
        logging.error(f"❌ Test 2: Connexion namespace - {e}")
    
    # Test 3: Connexion avec privilèges
    try:
        c = wmi.WMI(privileges=["Security", "Backup", "Restore"])
        logging.info("✅ Test 3: Connexion avec privilèges - OK")
        return True
    except Exception as e:
        logging.error(f"❌ Test 3: Connexion avec privilèges - {e}")
    
    return False

def test_device_queries():
    """Tester les requêtes spécifiques aux périphériques"""
    logging.info("🎮 Test des requêtes périphériques...")
    
    queries = {
        "GPU": "SELECT * FROM Win32_VideoController",
        "Audio": "SELECT * FROM Win32_SoundDevice", 
        "USB": "SELECT * FROM Win32_USBControllerDevice",
        "Network": "SELECT * FROM Win32_NetworkAdapter",
        "Storage": "SELECT * FROM Win32_DiskDrive"
    }
    
    try:
        c = wmi.WMI()
        for device_type, query in queries.items():
            try:
                result = c.query(query)
                count = len(list(result))
                logging.info(f"✅ {device_type}: {count} périphérique(s) détecté(s)")
            except Exception as e:
                logging.error(f"❌ {device_type}: Erreur - {e}")
    except Exception as e:
        logging.error(f"❌ Impossible d'initialiser WMI pour les tests: {e}")

def alternative_detection_methods():
    """Méthodes alternatives de détection sans WMI"""
    logging.info("🔄 Test méthodes alternatives...")
    
    # Test PowerShell
    try:
        cmd = 'powershell "Get-WmiObject Win32_VideoController | Select-Object Name"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            logging.info("✅ PowerShell WMI: Fonctionnel")
        else:
            logging.warning("⚠️  PowerShell WMI: Problème")
    except Exception as e:
        logging.error(f"❌ PowerShell WMI: {e}")
    
    # Test WMIC
    try:
        cmd = 'wmic path win32_VideoController get name'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            logging.info("✅ WMIC: Fonctionnel")
        else:
            logging.warning("⚠️  WMIC: Problème")
    except Exception as e:
        logging.error(f"❌ WMIC: {e}")

def main():
    """Fonction principale de diagnostic et correction"""
    logging.info("=" * 60)
    logging.info("🚀 DIAGNOSTIC WMI - Windows Optimizer Pro")
    logging.info("=" * 60)
    
    # Vérifier les droits admin
    if not check_admin_rights():
        logging.error("❌ ERREUR: Ce script doit être exécuté en tant qu'administrateur!")
        logging.info("💡 Solution: Clic droit -> 'Exécuter en tant qu'administrateur'")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    logging.info("✅ Droits administrateur détectés")
    
    # Test initial
    if test_wmi_connection():
        logging.info("✅ WMI fonctionne correctement!")
        test_device_queries()
    else:
        logging.warning("⚠️  WMI ne fonctionne pas, tentative de réparation...")
        
        # Réparation
        repair_wmi_service()
        
        # Test après réparation
        logging.info("🔄 Test après réparation...")
        time.sleep(5)
        
        if test_wmi_connection():
            logging.info("✅ WMI réparé avec succès!")
            test_device_queries()
        else:
            logging.error("❌ WMI toujours défaillant, test des alternatives...")
            alternative_detection_methods()
    
    logging.info("=" * 60)
    logging.info(f"📋 Rapport complet sauvegardé: {log_file}")
    logging.info("=" * 60)
    
    input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()
