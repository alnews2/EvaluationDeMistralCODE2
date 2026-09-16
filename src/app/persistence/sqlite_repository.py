"""
SQLiteRepository - Persistance SQLite pour la calculatrice

Ce module implémente la persistance des données de la calculatrice
via une base de données SQLite.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class SQLiteRepository:
    """
    Repository pour la persistance SQLite.
    
    Stocke l'état de la calculatrice et son historique dans une base SQLite.
    """
    
    DEFAULT_DIR = ".calculatorapp"
    DEFAULT_FILE = "calculator.db"
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialise le repository SQLite.
        
        Args:
            storage_path: Chemin vers le fichier SQLite (optionnel)
                         Si None, utilise le chemin par défaut
        """
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            home_dir = Path.home()
            self.storage_path = home_dir / self.DEFAULT_DIR / self.DEFAULT_FILE
        
        # Créer le répertoire si nécessaire
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialiser la base de données
        self._initialize_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """
        Retourne une connexion à la base de données.
        
        Returns:
            Connexion SQLite
        """
        conn = sqlite3.connect(str(self.storage_path))
        conn.row_factory = sqlite3.Row
        return conn
    
    def _initialize_database(self):
        """Initialise les tables de la base de données."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Table pour l'état
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS calculator_state (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    state_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table pour l'historique
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS calculation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT NOT NULL,
                    result TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Index pour optimiser les requêtes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_history_created ON calculation_history(created_at)")
            
            conn.commit()
    
    def save_state(self, state: Dict[str, Any]):
        """
        Sauvegarde l'état de la calculatrice.
        
        Args:
            state: État complet de la calculatrice
        """
        state_json = json.dumps(state, ensure_ascii=False)
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Supprimer l'ancien état (on garde seulement le dernier)
            cursor.execute("DELETE FROM calculator_state")
            
            # Insérer le nouvel état
            cursor.execute(
                "INSERT INTO calculator_state (state_data) VALUES (?)",
                (state_json,)
            )
            
            conn.commit()
    
    def load_state(self) -> Optional[Dict[str, Any]]:
        """
        Charge l'état de la calculatrice.
        
        Returns:
            État sauvegardé ou None s'il n'existe pas
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT state_data FROM calculator_state ORDER BY created_at DESC LIMIT 1"
            )
            row = cursor.fetchone()
            
            if row:
                return json.loads(row["state_data"])
            return None
    
    def save_history_entry(self, expression: str, result: str):
        """
        Sauvegarde une entrée dans l'historique.
        
        Args:
            expression: Expression mathématique
            result: Résultat du calcul
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calculation_history (expression, result) VALUES (?, ?)",
                (expression, result)
            )
            conn.commit()
    
    def save_history(self, history: List[str]):
        """
        Sauvegarde l'historique complet.
        
        Args:
            history: Liste des entrées de l'historique (format: "expression = result")
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Effacer l'ancien historique
            cursor.execute("DELETE FROM calculation_history")
            
            # Insérer les nouvelles entrées
            for entry in history:
                if " = " in entry:
                    expression, result = entry.split(" = ", 1)
                    cursor.execute(
                        "INSERT INTO calculation_history (expression, result) VALUES (?, ?)",
                        (expression, result)
                    )
            
            conn.commit()
    
    def load_history(self) -> List[str]:
        """
        Charge l'historique des calculs.
        
        Returns:
            Liste des entrées de l'historique (format: "expression = result")
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT expression, result FROM calculation_history ORDER BY created_at ASC"
            )
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                history.append(f"{row['expression']} = {row['result']}")
            
            return history
    
    def save_all(self, state: Dict[str, Any], history: List[str]):
        """
        Sauvegarde l'état et l'historique.
        
        Args:
            state: État de la calculatrice
            history: Historique des calculs
        """
        self.save_state(state)
        self.save_history(history)
    
    def load_all(self) -> Dict[str, Any]:
        """
        Charge toutes les données.
        
        Returns:
            Dictionnaire contenant state et history
        """
        return {
            "state": self.load_state() or {},
            "history": self.load_history(),
        }
    
    def clear(self):
        """Efface toutes les données."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM calculator_state")
            cursor.execute("DELETE FROM calculation_history")
            conn.commit()
    
    def delete(self):
        """Supprime le fichier de la base de données."""
        if self.storage_path.exists():
            self.storage_path.unlink()
    
    def get_history_count(self) -> int:
        """
        Retourne le nombre d'entrées dans l'historique.
        
        Returns:
            Nombre d'entrées
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM calculation_history")
            return cursor.fetchone()[0]
    
    def get_recent_history(self, limit: int = 10) -> List[str]:
        """
        Retourne les entrées récentes de l'historique.
        
        Args:
            limit: Nombre maximum d'entrées à retourner
        
        Returns:
            Liste des entrées récentes
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT expression, result FROM calculation_history 
                   ORDER BY created_at DESC LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            
            history = []
            for row in reversed(rows):  # Pour garder l'ordre chronologique
                history.append(f"{row['expression']} = {row['result']}")
            
            return history
    
    @property
    def exists(self) -> bool:
        """Vérifie si le fichier de la base de données existe."""
        return self.storage_path.exists()
