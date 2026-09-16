"""
build.py - Script de build pour CalculatorApp

Ce script permet de créer des exécutables pour Windows et Linux
en utilisant pyinstaller.
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


# Configuration
APP_NAME = "CalculatorApp"
MAIN_SCRIPT = "src/main.py"
ICON_FILE = None  # "assets/icon.ico" si disponible

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"


def clean_build_dirs():
    """Nettoie les répertoires de build."""
    for path in [BUILD_DIR, DIST_DIR]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def build_with_pyinstaller(platform: str = None):
    """
    Construit l'application avec pyinstaller.
    
    Args:
        platform: Plateforme cible (windows, linux, ou None pour auto-détection)
    """
    # Détecter la plateforme si non spécifiée
    if platform is None:
        platform = sys.platform.lower()
    
    # Configuration spécifique à la plateforme
    if platform == "windows" or platform == "win32":
        output_dir = BUILD_DIR / "windows"
        executable_name = f"{APP_NAME}.exe"
        onefile = True
    elif platform == "linux" or platform == "linux2":
        output_dir = BUILD_DIR / "linux"
        executable_name = APP_NAME
        onefile = True
    else:
        output_dir = BUILD_DIR / platform
        executable_name = APP_NAME
        onefile = True
    
    # Créer le répertoire de sortie
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Arguments de base pour pyinstaller
    pyinstaller_args = [
        "--name", APP_NAME,
        "--clean",
        "--noconfirm",
        "--log-level", "INFO",
    ]
    
    # Ajouter l'icône si disponible
    if ICON_FILE and Path(ICON_FILE).exists():
        pyinstaller_args.extend(["--icon", ICON_FILE])
    
    # Configuration pour un seul fichier ou un dossier
    if onefile:
        pyinstaller_args.append("--onefile")
    
    # Ajouter le script principal
    pyinstaller_args.append(str(PROJECT_ROOT / MAIN_SCRIPT))
    
    # Exécuter pyinstaller
    print(f"Building {APP_NAME} for {platform}...")
    print(f"PyInstaller command: pyinstaller {' '.join(pyinstaller_args)}")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pyinstaller"] + pyinstaller_args,
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)
    
    # Copier l'exécutable dans le bon répertoire
    dist_path = DIST_DIR / APP_NAME
    if dist_path.exists():
        if platform == "windows" or platform == "win32":
            target = output_dir / executable_name
        else:
            target = output_dir / executable_name
        
        shutil.copy(dist_path, target)
        print(f"Built executable: {target}")
    
    # Nettoyer le dossier dist
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)


def build_all():
    """Construit pour toutes les plateformes."""
    print("Building for all platforms...")
    
    # Nettoyer
    clean_build_dirs()
    
    # Construire pour Windows (même sous Linux, pyinstaller peut créer des builds Windows)
    try:
        build_with_pyinstaller("windows")
    except Exception as e:
        print(f"Failed to build for Windows: {e}")
    
    # Construire pour Linux
    try:
        build_with_pyinstaller("linux")
    except Exception as e:
        print(f"Failed to build for Linux: {e}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Build CalculatorApp")
    parser.add_argument(
        "--platform",
        choices=["windows", "linux", "all"],
        default=None,
        help="Plateforme cible (windows, linux, ou all)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Nettoyer avant de construire"
    )
    
    args = parser.parse_args()
    
    # Nettoyer si demandé
    if args.clean:
        clean_build_dirs()
    
    # Construire
    if args.platform == "all":
        build_all()
    elif args.platform:
        build_with_pyinstaller(args.platform)
    else:
        # Détecter automatiquement
        current_platform = platform.system().lower()
        if current_platform == "windows":
            build_with_pyinstaller("windows")
        elif current_platform == "linux":
            build_with_pyinstaller("linux")
        else:
            build_with_pyinstaller(current_platform)
    
    print("Build completed successfully!")


if __name__ == "__main__":
    main()
