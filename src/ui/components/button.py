"""
CalculatorButton - Bouton personnalisé pour la calculatrice

Ce module contient la classe CalculatorButton qui étend QPushButton
avec des styles et comportements personnalisés.
"""

from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import QPushButton


class CalculatorButton(QPushButton):
    """
    Bouton personnalisé pour la calculatrice.
    
    Ce bouton étend QPushButton avec :
    - Des styles personnalisés
    - Des signaux supplémentaires
    - Une taille fixe
    """
    
    # Signaux personnalisés
    clicked_with_value = Signal(str)
    
    def __init__(self, text: str = "", button_type: str = "digit", parent=None):
        """
        Initialise le bouton.
        
        Args:
            text: Texte du bouton
            button_type: Type du bouton (digit, operation, control, equals, decimal)
            parent: Widget parent
        """
        super().__init__(text, parent)
        
        self.button_type = button_type
        self._setup_style()
        self._setup_size()
        
        # Connecter le signal clicked
        self.clicked.connect(self._on_clicked)
    
    def _setup_style(self):
        """Configure le style du bouton."""
        # Le style est appliqué via CSS dans le parent
        # On définit ici les propriétés de base
        self.setProperty("buttonType", self.button_type)
    
    def _setup_size(self):
        """Configure la taille du bouton."""
        # Taille standard pour les boutons
        self.setMinimumSize(QSize(80, 80))
        self.setMaximumSize(QSize(100, 100))
    
    def _on_clicked(self):
        """Gère le clic sur le bouton."""
        self.clicked_with_value.emit(self.text())
    
    def set_button_type(self, button_type: str):
        """
        Change le type du bouton.
        
        Args:
            button_type: Nouveau type de bouton
        """
        self.button_type = button_type
        self.setProperty("buttonType", button_type)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def set_object_name(self, name: str):
        """
        Définit le nom de l'objet pour le styling CSS.
        
        Args:
            name: Nom de l'objet
        """
        super().setObjectName(name)
        self.style().unpolish(self)
        self.style().polish(self)
