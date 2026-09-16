"""
Display - Composants d'affichage pour la calculatrice

Ce module contient les composants d'affichage personnalisés :
- Display: Affiche la valeur actuelle
- OperationDisplay: Affiche l'opération en cours
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class Display(QLabel):
    """
    Composant d'affichage pour la valeur actuelle.
    
    Ce composant affiche la valeur actuelle de la calculatrice
    avec un style personnalisé.
    """
    
    def __init__(self, parent=None):
        """
        Initialise l'affichage.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent)
        
        self._setup_properties()
        self._setup_style()
    
    def _setup_properties(self):
        """Configure les propriétés de base."""
        self.setObjectName("DisplayLabel")
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setText("0")
        self.setMinimumHeight(80)
    
    def _setup_style(self):
        """Configure le style."""
        # Le style est appliqué via CSS
        pass
    
    def set_value(self, value: str):
        """
        Définit la valeur à afficher.
        
        Args:
            value: Valeur à afficher
        """
        self.setText(value)
    
    def set_error(self, error: str):
        """
        Affiche une erreur.
        
        Args:
            error: Message d'erreur
        """
        self.setText(error)
        self.setStyleSheet("color: #f38ba8;")
    
    def clear_error(self):
        """Efface l'erreur."""
        self.setStyleSheet("")


class OperationDisplay(QLabel):
    """
    Composant d'affichage pour l'opération en cours.
    
    Ce composant affiche l'opération en cours (ex: "5 + 3").
    """
    
    def __init__(self, parent=None):
        """
        Initialise l'affichage de l'opération.
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent)
        
        self._setup_properties()
        self._setup_style()
    
    def _setup_properties(self):
        """Configure les propriétés de base."""
        self.setObjectName("OperationLabel")
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setText("")
        self.setMinimumHeight(40)
    
    def _setup_style(self):
        """Configure le style."""
        # Le style est appliqué via CSS
        pass
    
    def set_operation(self, operation: str):
        """
        Définit l'opération à afficher.
        
        Args:
            operation: Opération à afficher
        """
        self.setText(operation)
    
    def clear(self):
        """Efface l'opération."""
        self.setText("")
