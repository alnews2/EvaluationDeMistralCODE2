"""
Main - Point d'entrée principal de l'application CalculatorApp

Ce module est le point d'entrée de l'application. Il initialise :
- L'application Qt
- Le ViewModel
- La Vue (MainWindow)
- Les connexions entre Vue et ViewModel
"""

import sys

from PySide6.QtWidgets import QApplication

from app.viewmodel.calculator_viewmodel import CalculatorViewModel
from ui.main_window import MainWindow


def main():
    """
    Fonction principale de l'application.
    
    Cette fonction :
    1. Crée l'application Qt
    2. Initialise le ViewModel
    3. Crée la fenêtre principale
    4. Connecte les signaux
    5. Démarre l'application
    """
    # Créer l'application Qt
    app = QApplication(sys.argv)
    app.setApplicationName("CalculatorApp")
    app.setOrganizationName("VibeCode")
    app.setOrganizationDomain("mistral.ai")
    
    # Créer le ViewModel
    viewmodel = CalculatorViewModel()
    
    # Créer la fenêtre principale
    window = MainWindow(viewmodel)
    
    # Connecter les signaux de la Vue au ViewModel
    window.digit_clicked.connect(viewmodel.on_digit_clicked)
    window.decimal_clicked.connect(viewmodel.on_decimal_clicked)
    window.operation_clicked.connect(viewmodel.on_operation_clicked)
    window.clear_clicked.connect(viewmodel.on_clear_clicked)
    window.clear_all_clicked.connect(viewmodel.on_clear_all_clicked)
    window.backspace_clicked.connect(viewmodel.on_backspace_clicked)
    window.history_cleared.connect(viewmodel.on_history_cleared)
    
    # Mettre à jour l'interface initiale
    window.update_display(viewmodel.display_value)
    window.update_operation_display(viewmodel.operation_display)
    window.update_history(viewmodel.history)
    window.update_storage_info(viewmodel.get_storage_info())
    
    # Configurer le bouton de stockage
    window.set_storage_button_text("JSON")
    
    # Fonction pour mettre à jour l'interface
    def update_ui():
        """Met à jour l'interface utilisateur."""
        window.update_display(viewmodel.display_value)
        window.update_operation_display(viewmodel.operation_display)
        window.update_history(viewmodel.history)
        window.update_storage_info(viewmodel.get_storage_info())
        
        # Gérer les erreurs
        if viewmodel.error:
            window.show_error(viewmodel.error)
        else:
            window.clear_error()
    
    # Connecter les propriétés du ViewModel aux mises à jour de l'UI
    # (Dans une application réelle, on utiliserait des signaux Qt pour ça)
    # Pour simplifier, on met à jour l'UI après chaque action
    
    # Afficher la fenêtre
    window.show()
    
    # Démarrer l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
