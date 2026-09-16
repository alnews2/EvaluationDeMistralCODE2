"""
package.py - Script de packaging pour CalculatorApp

Ce script permet de créer un package installable pour l'application.
"""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


# Configuration
APP_NAME = "CalculatorApp"
VERSION = "1.0.0"

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
PACKAGE_DIR = PROJECT_ROOT / "package"


def clean_package_dirs():
    """Nettoie les répertoires de package."""
    for path in [DIST_DIR, PACKAGE_DIR]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def create_wheel():
    """Crée un wheel Python."""
    print("Creating Python wheel...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "build", "--wheel"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error creating wheel: {e}")
        sys.exit(1)


def create_sdist():
    """Crée une distribution source."""
    print("Creating source distribution...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "build", "--sdist"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error creating sdist: {e}")
        sys.exit(1)


def create_package():
    """Crée un package complet."""
    print("Creating complete package...")
    
    clean_package_dirs()
    create_wheel()
    create_sdist()
    
    # Copier les fichiers dans le répertoire package
    dist_path = DIST_DIR
    if dist_path.exists():
        for item in dist_path.iterdir():
            if item.is_file():
                shutil.copy(item, PACKAGE_DIR)
    
    print(f"Package created in {PACKAGE_DIR}")


def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Package CalculatorApp")
    parser.add_argument(
        "--type",
        choices=["wheel", "sdist", "all"],
        default="all",
        help="Type de package à créer (wheel, sdist, ou all)"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Nettoyer avant de créer le package"
    )
    
    args = parser.parse_args()
    
    # Nettoyer si demandé
    if args.clean:
        clean_package_dirs()
    
    # Créer le package
    if args.type == "wheel":
        create_wheel()
    elif args.type == "sdist":
        create_sdist()
    else:
        create_package()
    
    print("Package creation completed successfully!")


if __name__ == "__main__":
    main()
