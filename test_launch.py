#!/usr/bin/env python3
"""
Test Rapide - Windows Optimizer Pro
Vérification rapide que l'application peut se lancer
"""

import sys
import os
import subprocess
import time

def test_launcher():
    """Test de lancement rapide de l'application"""
    print("🧪 Test de Lancement - Windows Optimizer Pro")
    print("=" * 50)
    
    # Test 1: Vérifier l'environnement virtuel
    venv_python = ".venv\\Scripts\\python.exe"
    if not os.path.exists(venv_python):
        print("❌ Environnement virtuel non trouvé")
        return False
    print("✅ Environnement virtuel OK")
    
    # Test 2: Vérifier le fichier principal
    if not os.path.exists("optimizer_python.py"):
        print("❌ Fichier optimizer_python.py non trouvé")
        return False
    print("✅ Fichier principal OK")
    
    # Test 3: Test d'import rapide
    try:
        result = subprocess.run([
            venv_python, "-c", 
            "import customtkinter, psutil, wmi; print('Imports OK')"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Imports principaux OK")
        else:
            print(f"❌ Erreur imports: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erreur test imports: {e}")
        return False
    
    # Test 4: Test de lancement de 3 secondes
    print("🚀 Test de lancement (3 secondes)...")
    try:
        process = subprocess.Popen([
            venv_python, "optimizer_python.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre 3 secondes
        time.sleep(3)
        
        # Vérifier si le processus est toujours actif
        if process.poll() is None:
            print("✅ Application lancée avec succès")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Application fermée prématurément: {stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lancement: {e}")
        return False

if __name__ == "__main__":
    success = test_launcher()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Test réussi - Windows Optimizer Pro est prêt!")
        print("💡 Vous pouvez maintenant utiliser START_HERE.bat")
    else:
        print("❌ Test échoué - Vérifiez la configuration")
        print("🔧 Solutions:")
        print("   1. Exécutez maintenance.bat")
        print("   2. Réinstallez avec universal_launcher.bat")
    
    input("\nAppuyez sur Entrée pour continuer...")
