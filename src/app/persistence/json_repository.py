"""
JsonRepository - Persistance JSON pour la calculatrice

Ce module implémente la persistance des données de la calculatrice
au format JSON dans un fichier local.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class JsonRepository:
    """
    Repository pour la persistance JSON.
    
    Stocke l'état de la calculatrice et son historique dans un fichier JSON.
    """
    
    DEFAULT_DIR = ".calculatorapp"
    DEFAULT_FILE = "history.json"
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialise le repository JSON.
        
        Args:
            storage_path: Chemin vers le fichier JSON (optionnel)
                         Si None, utilise le chemin par défaut
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            home_dir = Path.home()
            self.storage_path = home_dir / self.DEFAULT_DIR / self.DEFAULT_FILE
        
        # Créer le répertoire si nécessaire
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser le fichier s'il n'existe pas
        if not self.storage_path.exists():
            self._save({})
    
    def _load(self) -> Dict[str, Any]:
        """
        Charge les données depuis le fichier JSON.
        
        Returns:
            Dictionnaire contenant les données
        """
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save(self, data: Dict[str, Any]):
        """
        Sauvegarde les données dans le fichier JSON.
        
        Args:
            data: Dictionnaire à sauvegarder
        """
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def save_state(self, state: Dict[str, Any]):
        """
        Sauvegarde l'état de la calculatrice.
        
        Args:
            state: État complet de la calculatrice
        """
        data = self._load()
        data["state"] = state
        self._save(data)
    
    def load_state(self) -> Optional[Dict[str, Any]]:
        """
        Charge l'état de la calculatrice.
        
        Returns:
            État sauvegardé ou None s'il n'existe pas
        """
        data = self._load()
        return data.get("state")
    
    def save_history(self, history: list):
        """
        Sauvegarde l'historique des calculs.
        
        Args:
            history: Liste des entrées de l'historique
        """
        data = self._load()
        data["history"] = history
        self._save(data)
    
    def load_history(self) -> list:
        """
        Charge l'historique des calculs.
        
        Returns:
            Liste des entrées de l'historique
        """
        data = self._load()
        return data.get("history", [])
    
    def save_all(self, state: Dict[str, Any], history: list):
        """
        Sauvegarde l'état et l'historique.
        
        Args:
            state: État de la calculatrice
            history: Historique des calculs
        """
        data = {
            "state": state,
            "history": history,
        }
        self._save(data)
    
    def load_all(self) -> Dict[str, Any]:
        """
        Charge toutes les données.
        
        Returns:
            Dictionnaire contenant state et history
        """
        data = self._load()
        return {
            "state": data.get("state", {}),
            "history": data.get("history", []),
        }
    
    def clear(self):
        """Efface toutes les données."""
        self._save({})
    
    def delete(self):
        """Supprime le fichier de stockage."""
        if self.storage_path.exists():
            self.storage_path.unlink()
    
    @property
    def exists(self) -> bool:
        """Vérifie si le fichier de stockage existe."""
        return self.storage_path.exists()
