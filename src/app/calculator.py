"""
Calculator - Modèle de la calculatrice

Ce module contient la logique métier pure de la calculatrice.
Il est indépendant de l'UI et peut être testé unitairement.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class OperationType(Enum):
    """Types d'opérations supportées par la calculatrice."""
    ADDITION = auto()
    SUBTRACTION = auto()
    MULTIPLICATION = auto()
    DIVISION = auto()
    EQUALS = auto()
    CLEAR = auto()
    CLEAR_ALL = auto()
    BACKSPACE = auto()
    DECIMAL = auto()
    NONE = auto()


class Operation:
    """Représente une opération mathématique."""
    
    def __init__(self, op_type: OperationType, value: Optional[str] = None):
        self.type = op_type
        self.value = value
    
    def __repr__(self):
        return f"Operation(type={self.type.name}, value={self.value})"


@dataclass
class CalculationHistory:
    """Stocke l'historique des calculs."""
    entries: List[str] = field(default_factory=list)
    
    def add(self, expression: str, result: str):
        """Ajoute une entrée à l'historique."""
        entry = f"{expression} = {result}"
        self.entries.append(entry)
    
    def clear(self):
        """Efface l'historique."""
        self.entries.clear()
    
    def get_all(self) -> List[str]:
        """Retourne toutes les entrées."""
        return self.entries.copy()
    
    def get_last(self, n: int = 1) -> List[str]:
        """Retourne les n dernières entrées."""
        return self.entries[-n:] if self.entries else []


class Calculator:
    """
    Calculatrice 4 opérations avec gestion d'état.
    
    Cette classe implémente la logique métier de la calculatrice.
    Elle gère :
    - Les opérations de base (+, -, *, /)
    - La gestion de l'état (current value, previous value, operation)
    - L'historique des calculs
    - Les erreurs (division par zéro, etc.)
    """
    
    MAX_DISPLAY_LENGTH = 15
    
    def __init__(self):
        """Initialise la calculatrice."""
        self._reset_state()
        self.history = CalculationHistory()
    
    def _reset_state(self):
        """Réinitialise l'état de la calculatrice."""
        self.current_value = "0"
        self.previous_value = None
        self.current_operation = None
        self.waiting_for_operand = False
        self.error = None
    
    def reset(self):
        """Réinitialise complètement la calculatrice."""
        self._reset_state()
    
    def clear_all(self):
        """Réinitialise la calculatrice et efface l'historique."""
        self._reset_state()
        self.history.clear()
    
    def _format_number(self, value: str) -> str:
        """Formate un nombre pour l'affichage."""
        # Supprimer les zéros en trop
        if value.endswith(".0"):
            value = value[:-2]
        
        # Limiter la longueur
        if len(value) > self.MAX_DISPLAY_LENGTH:
            if "e" in value.lower():
                # Conserver la notation scientifique
                parts = value.split("e")
                if len(parts[0]) > 8:
                    value = f"{float(value):.8e}"
            else:
                value = value[:self.MAX_DISPLAY_LENGTH]
        
        return value
    
    def _parse_number(self, value: str) -> float:
        """Parse une chaîne en nombre."""
        try:
            return float(value)
        except ValueError:
            return 0.0
    
    def append_digit(self, digit: str):
        """
        Ajoute un chiffre à la valeur actuelle.
        
        Args:
            digit: Le chiffre à ajouter (0-9)
        """
        if self.error:
            self._reset_state()
        
        if self.waiting_for_operand:
            self.current_value = digit
            self.waiting_for_operand = False
        else:
            if self.current_value == "0":
                self.current_value = digit
            else:
                self.current_value += digit
        
        self.current_value = self._format_number(self.current_value)
    
    def append_decimal(self):
        """Ajoute un point décimal à la valeur actuelle."""
        if self.error:
            self._reset_state()
        
        if self.waiting_for_operand:
            self.current_value = "0."
            self.waiting_for_operand = False
        else:
            if "." not in self.current_value:
                self.current_value += "."
        
        self.current_value = self._format_number(self.current_value)
    
    def set_operation(self, op_type: OperationType):
        """
        Définit l'opération à effectuer.
        
        Args:
            op_type: Le type d'opération
        """
        if self.error:
            self._reset_state()
        
        if op_type == OperationType.EQUALS:
            self._calculate_result()
            return
        
        if op_type in (OperationType.ADDITION, OperationType.SUBTRACTION, 
                       OperationType.MULTIPLICATION, OperationType.DIVISION):
            if self.current_operation and not self.waiting_for_operand:
                self._calculate_result()
            
            self.previous_value = self.current_value
            self.current_operation = op_type
            self.waiting_for_operand = True
    
    def _calculate_result(self):
        """Calcule le résultat de l'opération en cours."""
        if self.previous_value is None or self.current_operation is None:
            return
        
        try:
            prev = self._parse_number(self.previous_value)
            curr = self._parse_number(self.current_value)
            
            if self.current_operation == OperationType.ADDITION:
                result = prev + curr
            elif self.current_operation == OperationType.SUBTRACTION:
                result = prev - curr
            elif self.current_operation == OperationType.MULTIPLICATION:
                result = prev * curr
            elif self.current_operation == OperationType.DIVISION:
                if curr == 0:
                    raise ZeroDivisionError("Division par zéro")
                result = prev / curr
            else:
                return
            
            # Formater le résultat
            result_str = str(result)
            result_str = self._format_number(result_str)
            
            # Sauvegarder dans l'historique
            expression = f"{self.previous_value} {self._op_to_symbol()} {self.current_value}"
            self.history.add(expression, result_str)
            
            # Mettre à jour l'état
            self.current_value = result_str
            self.previous_value = None
            self.current_operation = None
            self.waiting_for_operand = True
            self.error = None
            
        except ZeroDivisionError as e:
            self.error = str(e)
            self.current_value = "Erreur"
            self.previous_value = None
            self.current_operation = None
            self.waiting_for_operand = True
        except Exception as e:
            self.error = str(e)
            self.current_value = "Erreur"
            self.previous_value = None
            self.current_operation = None
            self.waiting_for_operand = True
    
    def _op_to_symbol(self) -> str:
        """Convertit l'opération en symbole."""
        if self.current_operation == OperationType.ADDITION:
            return "+"
        elif self.current_operation == OperationType.SUBTRACTION:
            return "-"
        elif self.current_operation == OperationType.MULTIPLICATION:
            return "*"
        elif self.current_operation == OperationType.DIVISION:
            return "/"
        return ""
    
    def backspace(self):
        """Supprime le dernier caractère de la valeur actuelle."""
        if self.error:
            self._reset_state()
            return
        
        if len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
        else:
            self.current_value = "0"
        
        self.current_value = self._format_number(self.current_value)
    
    def get_state(self) -> dict:
        """
        Retourne l'état actuel de la calculatrice.
        
        Returns:
            Un dictionnaire contenant l'état complet
        """
        return {
            "current_value": self.current_value,
            "previous_value": self.previous_value,
            "current_operation": self.current_operation.name if self.current_operation else None,
            "waiting_for_operand": self.waiting_for_operand,
            "error": self.error,
            "history": self.history.get_all(),
        }
    
    def set_state(self, state: dict):
        """
        Restaure l'état de la calculatrice.
        
        Args:
            state: Dictionnaire contenant l'état à restaurer
        """
        self.current_value = state.get("current_value", "0")
        self.previous_value = state.get("previous_value")
        
        op_name = state.get("current_operation")
        if op_name:
            self.current_operation = OperationType[op_name]
        else:
            self.current_operation = None
        
        self.waiting_for_operand = state.get("waiting_for_operand", False)
        self.error = state.get("error")
        
        history_entries = state.get("history", [])
        self.history = CalculationHistory()
        self.history.entries = history_entries
