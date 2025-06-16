"""
🧪 Test Avancé de Détection Gaming - Sans Admin
Test de toutes les méthodes de détection disponibles
"""

import subprocess
import sys
import time
import logging
from pathlib import Path

# Configuration du logging
log_file = Path(__file__).parent / "test_detection_avance.log"
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def test_wmi_direct():
    """Test WMI direct (même méthode que l'optimiseur)"""
    logging.info("🎮 Test WMI Direct (méthode optimiseur)...")
    
    try:
        import wmi
        c = wmi.WMI()
        
        # Test GPU avec list() comme dans l'optimiseur corrigé
        try:
            gpus = list(c.Win32_VideoController())
            gpu_count = 0
            for gpu in gpus:
                if gpu.Name and gpu.Name.strip():
                    if "Intel(R) UHD" not in gpu.Name and "Intel(R) HD" not in gpu.Name:
                        gpu_count += 1
                        logging.info(f"  📺 GPU Gaming: {gpu.Name}")
                        
                        # Vérifier si c'est gaming
                        if any(brand in gpu.Name.upper() for brand in ['NVIDIA', 'AMD', 'RADEON', 'GEFORCE', 'RTX', 'GTX', 'RX']):
                            logging.info(f"    🎮 GAMING: OUI")
                        
            logging.info(f"✅ WMI Direct GPU: {gpu_count} détecté(s)")
            
        except Exception as e:
            logging.error(f"❌ WMI Direct GPU: {e}")
        
        # Test Audio
        try:
            audio_devices = list(c.Win32_SoundDevice())
            audio_count = 0
            for audio in audio_devices:
                if audio.Name and audio.Name.strip() and audio.Name != "Aucun":
                    exclude_keywords = ['High Definition Audio', 'Microsoft', 'Composite', 'Generic']
                    if not any(keyword in audio.Name for keyword in exclude_keywords):
                        audio_count += 1
                        logging.info(f"  🎵 Audio: {audio.Name}")
                        
            logging.info(f"✅ WMI Direct Audio: {audio_count} détecté(s)")
            
        except Exception as e:
            logging.error(f"❌ WMI Direct Audio: {e}")
            
        # Test Périphériques USB
        try:
            pnp_devices = list(c.Win32_PnPEntity())
            gaming_count = 0
            gaming_keywords = ['gaming', 'mouse', 'keyboard', 'razer', 'logitech', 'corsair', 'steelseries', 'hyperx']
            
            for device in pnp_devices:
                if device.Name and hasattr(device, 'Service') and device.Service:
                    name_lower = device.Name.lower()
                    if any(keyword in name_lower for keyword in gaming_keywords):
                        gaming_count += 1
                        logging.info(f"  🎮 Gaming Device: {device.Name}")
                        
            logging.info(f"✅ WMI Direct USB Gaming: {gaming_count} détecté(s)")
            
        except Exception as e:
            logging.error(f"❌ WMI Direct USB: {e}")
            
        return True
        
    except Exception as e:
        logging.error(f"❌ WMI Direct général: {e}")
        return False

def test_powershell_cim():
    """Test PowerShell avec Get-CimInstance (méthode moderne)"""
    logging.info("🔄 Test PowerShell CIM...")
    
    try:
        # GPU via PowerShell CIM
        cmd = 'powershell "Get-CimInstance Win32_VideoController | Where-Object {$_.Name -notlike \'*UHD*\' -and $_.Name -notlike \'*HD Graphics*\'} | Select-Object Name | Format-List"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0 and result.stdout.strip():
            gpu_lines = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'Name' in line and ':' in line]
            for gpu in gpu_lines:
                if gpu:
                    logging.info(f"  📺 PowerShell GPU: {gpu}")
            logging.info(f"✅ PowerShell GPU: {len(gpu_lines)} détecté(s)")
        else:
            logging.warning(f"⚠️  PowerShell GPU: Aucun résultat")
            
    except Exception as e:
        logging.error(f"❌ PowerShell GPU: {e}")

def test_wmic_legacy():
    """Test WMIC (méthode legacy)"""
    logging.info("🛠️ Test WMIC Legacy...")
    
    try:
        # GPU via WMIC
        cmd = 'wmic path win32_VideoController get name /format:list'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            gpu_lines = [line.split('=')[1].strip() for line in result.stdout.split('\n') if 'Name=' in line and line.split('=')[1].strip()]
            gaming_gpus = [gpu for gpu in gpu_lines if gpu and 'Intel(R) UHD' not in gpu and 'Intel(R) HD' not in gpu]
            
            for gpu in gaming_gpus:
                logging.info(f"  📺 WMIC GPU: {gpu}")
            logging.info(f"✅ WMIC GPU: {len(gaming_gpus)} détecté(s)")
        else:
            logging.warning(f"⚠️  WMIC: Erreur {result.stderr}")
            
    except Exception as e:
        logging.error(f"❌ WMIC: {e}")

def test_device_manager():
    """Test via Device Manager PowerShell"""
    logging.info("📟 Test Device Manager...")
    
    try:
        cmd = 'powershell "Get-PnpDevice | Where-Object {$_.FriendlyName -match \'gaming|razer|logitech|steelseries|corsair|mouse|keyboard\'} | Select-Object FriendlyName, Status | Format-List"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
        
        if result.returncode == 0 and result.stdout.strip():
            device_lines = [line.split(':')[1].strip() for line in result.stdout.split('\n') if 'FriendlyName' in line and ':' in line]
            for device in device_lines:
                if device and len(device) > 3:
                    logging.info(f"  🎮 Device Manager: {device}")
            logging.info(f"✅ Device Manager: {len(device_lines)} détecté(s)")
        else:
            logging.warning(f"⚠️  Device Manager: Aucun résultat")
            
    except Exception as e:
        logging.error(f"❌ Device Manager: {e}")

def main():
    """Test principal complet"""
    print("=" * 70)
    print("🧪 TEST AVANCÉ DÉTECTION GAMING - Windows Optimizer Pro")
    print("=" * 70)
    print()
    
    # Test toutes les méthodes
    print("🎯 Test de toutes les méthodes de détection...")
    print()
    
    success = test_wmi_direct()
    print()
    
    test_powershell_cim()
    print()
    
    test_wmic_legacy()
    print()
    
    test_device_manager()
    print()
    
    print("=" * 70)
    print(f"📋 Rapport détaillé sauvegardé: {log_file}")
    
    if success:
        print("✅ WMI fonctionne - Les périphériques devraient être détectés !")
    else:
        print("❌ WMI a des problèmes - Les fallbacks seront utilisés")
        
    print("=" * 70)
    print()
    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
