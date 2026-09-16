"""
CalculatorViewModel - ViewModel de la calculatrice

Ce module contient le ViewModel qui fait l'interface entre le Model (Calculator)
et la View (MainWindow). Il gère la logique de présentation et la persistance.
"""

import os
from typing import Optional

from ..calculator import Calculator, OperationType
from ..persistence.json_repository import JsonRepository
from ..persistence.sqlite_repository import SQLiteRepository


class StorageType:
    """Types de stockage supportés."""
    JSON = "json"
    SQLITE = "sqlite"


class CalculatorViewModel:
    """
    ViewModel pour la calculatrice.
    
    Ce ViewModel :
    - Encapsule le modèle Calculator
    - Gère la persistance (JSON ou SQLite)
    - Expose les propriétés et commandes pour la Vue
    - Notifie les changements d'état
    """
    
    def __init__(self, storage_type: Optional[str] = None):
        """
        Initialise le ViewModel.
        
        Args:
            storage_type: Type de stockage (json ou sqlite)
                         Si None, utilise la variable d'environnement
                         ou JSON par défaut
        """
        self.calculator = Calculator()
        self._storage_type = storage_type
        self._repository = self._create_repository()
        
        # Charger l'état initial
        self._load_state()
    
    def _create_repository(self):
        """Crée le repository de persistance approprié."""
        if self._storage_type:
            storage = self._storage_type.lower()
        else:
            storage = os.environ.get("CALCULATOR_STORAGE", StorageType.JSON)
        
        if storage == StorageType.SQLITE:
            return SQLiteRepository()
        else:
            return JsonRepository()
    
    def _load_state(self):
        """Charge l'état depuis la persistance."""
        try:
            data = self._repository.load_all()
            if data.get("state"):
                self.calculator.set_state(data["state"])
            if data.get("history"):
                self.calculator.history.entries = data["history"]
        except Exception:
            # Si le chargement échoue, on continue avec l'état par défaut
            pass
    
    def _save_state(self):
        """Sauvegarde l'état vers la persistance."""
        try:
            state = self.calculator.get_state()
            history = self.calculator.history.get_all()
            self._repository.save_all(state, history)
        except Exception:
            # Ne pas bloquer l'application si la sauvegarde échoue
            pass
    
    # Propriétés exposées à la Vue
    
    @property
    def display_value(self) -> str:
        """Valeur à afficher."""
        return self.calculator.current_value
    
    @property
    def operation_display(self) -> str:
        """Opération en cours à afficher."""
        if self.calculator.current_operation:
            prev = self.calculator.previous_value or "0"
            op_symbol = self._op_to_symbol(self.calculator.current_operation)
            return f"{prev} {op_symbol}"
        return ""
    
    @property
    def error(self) -> Optional[str]:
        """Erreur actuelle."""
        return self.calculator.error
    
    @property
    def history(self) -> list:
        """Historique des calculs."""
        return self.calculator.history.get_all()
    
    @property
    def has_history(self) -> bool:
        """Indique si l'historique contient des entrées."""
        return len(self.calculator.history.entries) > 0
    
    # Commandes exposées à la Vue
    
    def on_digit_clicked(self, digit: str):
        """
        Gère le clic sur un chiffre.
        
        Args:
            digit: Le chiffre cliqué (0-9)
        """
        self.calculator.append_digit(digit)
        self._save_state()
    
    def on_decimal_clicked(self):
        """Gère le clic sur le point décimal."""
        self.calculator.append_decimal()
        self._save_state()
    
    def on_operation_clicked(self, operation: str):
        """
        Gère le clic sur une opération.
        
        Args:
            operation: L'opération cliquée (+, -, *, /, =)
        """
        op_map = {
            "+": OperationType.ADDITION,
            "-": OperationType.SUBTRACTION,
            "*": OperationType.MULTIPLICATION,
            "/": OperationType.DIVISION,
            "=": OperationType.EQUALS,
        }
        
        if operation in op_map:
            self.calculator.set_operation(op_map[operation])
            self._save_state()
    
    def on_clear_clicked(self):
        """Gère le clic sur Clear (C)."""
        self.calculator.reset()
        self._save_state()
    
    def on_clear_all_clicked(self):
        """Gère le clic sur Clear All (CE)."""
        self.calculator.clear_all()
        self._save_state()
    
    def on_backspace_clicked(self):
        """Gère le clic sur Backspace."""
        self.calculator.backspace()
        self._save_state()
    
    def on_history_cleared(self):
        """Gère l'effacement de l'historique."""
        self.calculator.history.clear()
        self._save_state()
    
    def _op_to_symbol(self, op_type: OperationType) -> str:
        """Convertit un type d'opération en symbole."""
        op_map = {
            OperationType.ADDITION: "+",
            OperationType.SUBTRACTION: "-",
            OperationType.MULTIPLICATION: "*",
            OperationType.DIVISION: "/",
        }
        return op_map.get(op_type, "")
    
    def get_storage_info(self) -> str:
        """
        Retourne des informations sur le type de stockage.
        
        Returns:
            Description du stockage utilisé
        """
        if isinstance(self._repository, JsonRepository):
            return f"JSON: {self._repository.storage_path}"
        elif isinstance(self._repository, SQLiteRepository):
            return f"SQLite: {self._repository.storage_path}"
        return "Aucun stockage"
    
    def switch_storage(self, storage_type: str):
        """
        Change le type de stockage.
        
        Args:
            storage_type: Nouveau type de stockage (json ou sqlite)
        """
        if storage_type.lower() not in [StorageType.JSON, StorageType.SQLITE]:
            return
        
        # Sauvegarder l'état actuel
        state = self.calculator.get_state()
        history = self.calculator.history.get_all()
        
        # Changer de repository
        self._storage_type = storage_type.lower()
        self._repository = self._create_repository()
        
        # Sauvegarder dans le nouveau repository
        self._repository.save_all(state, history)
