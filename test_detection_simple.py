"""
🧪 Test rapide de détection des périphériques gaming
Sans droits administrateur requis
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Configuration du logging
log_file = Path(__file__).parent / "test_detection.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def test_wmi_simple():
    """Test WMI simplifié sans droits admin"""
    logging.info("🧪 Test WMI simplifié...")
    
    try:
        import wmi
        c = wmi.WMI()
        logging.info("✅ Import WMI: OK")
        
        # Test simple de requête
        try:
            gpus = list(c.Win32_VideoController())
            logging.info(f"✅ GPU détectés: {len(gpus)}")
            for gpu in gpus[:2]:  # Afficher seulement les 2 premiers
                if gpu.Name:
                    logging.info(f"  📺 {gpu.Name}")
        except Exception as e:
            logging.error(f"❌ Erreur GPU: {e}")
            
        return True
            
    except Exception as e:
        logging.error(f"❌ Erreur WMI: {e}")
        return False

def test_powershell_fallback():
    """Test des méthodes PowerShell alternatives"""
    logging.info("🔄 Test PowerShell...")
    
    # Test GPU via PowerShell
    try:
        cmd = 'powershell "Get-WmiObject Win32_VideoController | Select-Object Name -First 3 | Format-Table -HideTableHeaders"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            gpu_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            logging.info(f"✅ PowerShell GPU: {len(gpu_lines)} détecté(s)")
            for gpu in gpu_lines[:2]:
                logging.info(f"  📺 {gpu}")
        else:
            logging.warning(f"⚠️  PowerShell erreur: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ PowerShell GPU: {e}")

    # Test périphériques USB/PnP
    try:
        cmd = 'powershell "Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like \'*gaming*\' -or $_.Name -like \'*razer*\' -or $_.Name -like \'*logitech*\' -or $_.Name -like \'*steelseries*\'} | Select-Object Name -First 5 | Format-Table -HideTableHeaders"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            device_lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            logging.info(f"✅ Périphériques gaming: {len(device_lines)} détecté(s)")
            for device in device_lines:
                logging.info(f"  🎮 {device}")
        else:
            logging.warning(f"⚠️  PowerShell périphériques erreur: {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ PowerShell périphériques: {e}")

def test_direct_imports():
    """Test des imports et modules Python"""
    logging.info("📦 Test des modules Python...")
    
    try:
        import customtkinter as ctk
        logging.info("✅ CustomTkinter: OK")
    except ImportError as e:
        logging.error(f"❌ CustomTkinter: {e}")
    
    try:
        import psutil
        logging.info("✅ psutil: OK")
    except ImportError as e:
        logging.error(f"❌ psutil: {e}")
    
    try:
        import wmi
        logging.info("✅ WMI: OK")
    except ImportError as e:
        logging.error(f"❌ WMI: {e}")

def main():
    """Test principal rapide"""
    print("=" * 60)
    print("🧪 TEST RAPIDE - Windows Optimizer Pro")
    print("=" * 60)
    print()
    
    # Test des modules
    test_direct_imports()
    print()
    
    # Test WMI
    if test_wmi_simple():
        print("✅ WMI fonctionne!")
    else:
        print("❌ WMI a des problèmes, test des alternatives...")
        test_powershell_fallback()
    
    print()
    print("=" * 60)
    print(f"📋 Rapport détaillé: {log_file}")
    print("=" * 60)
    
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
