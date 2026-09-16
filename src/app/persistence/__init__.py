"""
Persistence package - Gestion de la persistance des données

Ce package contient les implémentations de persistance :
- JSON (fichier)
- SQLite (base de données)
"""

from .json_repository import JsonRepository
from .sqlite_repository import SQLiteRepository

__all__ = ["JsonRepository", "SQLiteRepository"]
