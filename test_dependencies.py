#!/usr/bin/env python3
"""
Test script pour vérifier que toutes les dépendances sont installées
et que les fonctionnalités principales fonctionnent.
"""

import sys
import traceback

def test_imports():
    """Tester les imports principaux"""
    print("🔍 Test des imports...")
    
    try:
        import tkinter as tk
        print("✅ tkinter - OK")
    except ImportError as e:
        print(f"❌ tkinter - ERREUR: {e}")
        return False
    
    try:
        import customtkinter as ctk
        print("✅ customtkinter - OK")
    except ImportError as e:
        print(f"❌ customtkinter - ERREUR: {e}")
        print("   💡 Solution: pip install customtkinter")
        return False
    
    try:
        import psutil
        print("✅ psutil - OK")
    except ImportError as e:
        print(f"❌ psutil - ERREUR: {e}")
        print("   💡 Solution: pip install psutil")
        return False
    
    try:
        import requests
        print("✅ requests - OK")
    except ImportError as e:
        print(f"❌ requests - ERREUR: {e}")
        print("   💡 Solution: pip install requests")
        return False
    
    try:
        import wmi
        print("✅ WMI - OK")
    except ImportError as e:
        print(f"⚠️ WMI - Optionnel: {e}")
        print("   💡 Solution: pip install WMI")
        print("   📝 Note: WMI est optionnel, certaines fonctions seront limitées")
    
    try:
        import winreg
        print("✅ winreg - OK")
    except ImportError as e:
        print(f"❌ winreg - ERREUR: {e}")
        return False
    
    return True

def test_system_info():
    """Tester la récupération d'informations système"""
    print("\n🖥️ Test des informations système...")
    
    try:
        import psutil
        import platform
        
        print(f"🔹 OS: {platform.system()} {platform.release()}")
        print(f"🔹 CPU: {psutil.cpu_count()} cores, {psutil.cpu_percent(interval=1):.1f}% utilisation")
        
        memory = psutil.virtual_memory()
        print(f"🔹 RAM: {memory.total // (1024**3)} GB total, {memory.percent:.1f}% utilisé")
        
        disk = psutil.disk_usage('C:')
        print(f"🔹 Disque C: {disk.total // (1024**3)} GB total, {disk.percent:.1f}% utilisé")
        
        print("✅ Informations système récupérées avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des informations système: {e}")
        return False

def test_wmi_functionality():
    """Tester les fonctionnalités WMI"""
    print("\n🔌 Test des fonctionnalités WMI...")
    
    try:
        import wmi
        c = wmi.WMI()
        
        # Test GPU
        gpus = list(c.Win32_VideoController())
        print(f"🔹 {len(gpus)} carte(s) graphique(s) détectée(s)")
        
        # Test disques
        disks = list(c.Win32_DiskDrive())
        print(f"🔹 {len(disks)} disque(s) détecté(s)")
        
        print("✅ Fonctionnalités WMI opérationnelles")
        return True
        
    except ImportError:
        print("⚠️ WMI non disponible - fonctionnalités limitées")
        return True
    except Exception as e:
        print(f"❌ Erreur WMI: {e}")
        return False

def test_gui():
    """Tester l'interface graphique"""
    print("\n🖼️ Test de l'interface graphique...")
    
    try:
        import customtkinter as ctk
        
        # Test création fenêtre
        ctk.set_appearance_mode("dark")
        root = ctk.CTk()
        root.title("Test GUI")
        root.geometry("300x200")
        root.withdraw()  # Cacher la fenêtre
        
        # Test widgets
        label = ctk.CTkLabel(root, text="Test OK")
        label.pack(pady=20)
        
        button = ctk.CTkButton(root, text="Fermer")
        button.pack(pady=10)
        
        # Mettre à jour une fois
        root.update_idletasks()
        
        print("✅ Interface graphique fonctionnelle")
        
        # Nettoyer proprement
        root.quit()
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur interface graphique: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=" * 60)
    print("🚀 Windows Optimizer Pro - Test des Dépendances")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Imports
    if test_imports():
        tests_passed += 1
    
    # Test 2: Informations système
    if test_system_info():
        tests_passed += 1
    
    # Test 3: WMI
    if test_wmi_functionality():
        tests_passed += 1
    
    # Test 4: Interface graphique
    if test_gui():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés avec succès!")
        print("✅ Vous pouvez lancer Windows Optimizer Pro")
        print("\n💡 Commande de lancement:")
        print("   python optimizer_python.py")
        return True
    else:
        print("❌ Certains tests ont échoué")
        print("🔧 Veuillez résoudre les problèmes avant de continuer")
        print("\n💡 Installation des dépendances:")
        print("   pip install -r requirements.txt")
        return False

if __name__ == "__main__":
    try:
        success = main()
        input("\nAppuyez sur Entrée pour continuer...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur inattendue: {e}")
        traceback.print_exc()
        input("\nAppuyez sur Entrée pour continuer...")
        sys.exit(1)
