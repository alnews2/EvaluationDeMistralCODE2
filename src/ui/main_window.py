"""
MainWindow - Fenêtre principale de l'application calculatrice

Ce module contient la classe MainWindow qui représente la vue principale
de l'application calculatrice. Elle utilise le ViewModel pour interagir
avec le modèle.
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .components.button import CalculatorButton
from .components.display import Display, OperationDisplay
from .styles.dark_theme import DARK_THEME

class MainWindow(QMainWindow):
    """
    Fenêtre principale de la calculatrice.

    Cette classe gère :
    - La création de l'interface utilisateur
    - Les interactions avec l'utilisateur
    - La communication avec le ViewModel
    """

    # Signaux pour communiquer avec le ViewModel
    digit_clicked = Signal(str)
    decimal_clicked = Signal()
    operation_clicked = Signal(str)
    clear_clicked = Signal()
    clear_all_clicked = Signal()
    backspace_clicked = Signal()
    history_cleared = Signal()

    def __init__(self, viewmodel=None, parent=None):
        """
        Initialise la fenêtre principale.

        Args:
            viewmodel: Le ViewModel à utiliser
            parent: Widget parent
        """
        super().__init__(parent)

        self.viewmodel = viewmodel
        self._setup_window()
        self._setup_ui()
        self._connect_signals()

        # Appliquer le thème
        self._apply_theme()

    def _setup_window(self):
        """Configure les propriétés de la fenêtre."""
        self.setWindowTitle("CalculatorApp")
        self.setFixedSize(400, 700)
        self.setWindowIconName("calculator")

    def _setup_ui(self):
        """Crée l'interface utilisateur."""
        # Widget central
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Zone d'affichage
        self._setup_display_section(main_layout)

        # Zone des boutons
        self._setup_buttons_section(main_layout)

        # Zone de l'historique
        self._setup_history_section(main_layout)

        # Info de stockage
        self._setup_storage_info(main_layout)

    def _setup_display_section(self, layout):
        """Crée la zone d'affichage."""
        display_layout = QVBoxLayout()
        display_layout.setSpacing(5)

        # Affichage de l'opération
        self.operation_display = OperationDisplay()
        display_layout.addWidget(self.operation_display)

        # Affichage principal
        self.display = Display()
        display_layout.addWidget(self.display)

        layout.addLayout(display_layout)

    def _setup_buttons_section(self, layout):
        """Crée la zone des boutons."""
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Créer les boutons
        self._create_button(buttons_layout, "7", 0, 0, "DigitButton", "7")
        self._create_button(buttons_layout, "8", 0, 1, "DigitButton", "8")
        self._create_button(buttons_layout, "9", 0, 2, "DigitButton", "9")
        self._create_button(buttons_layout, "/", 0, 3, "OperationButton", "/")

        self._create_button(buttons_layout, "4", 1, 0, "DigitButton", "4")
        self._create_button(buttons_layout, "5", 1, 1, "DigitButton", "5")
        self._create_button(buttons_layout, "6", 1, 2, "DigitButton", "6")
        self._create_button(buttons_layout, "*", 1, 3, "OperationButton", "*")

        self._create_button(buttons_layout, "1", 2, 0, "DigitButton", "1")
        self._create_button(buttons_layout, "2", 2, 1, "DigitButton", "2")
        self._create_button(buttons_layout, "3", 2, 2, "DigitButton", "3")
        self._create_button(buttons_layout, "-", 2, 3, "OperationButton", "-")

        self._create_button(buttons_layout, "0", 3, 0, "DigitButton", "0")
        self._create_button(buttons_layout, ".", 3, 1, "DecimalButton", ".")
        self._create_button(buttons_layout, "=", 3, 2, "OperationButton", "=")
        self._create_button(buttons_layout, "+", 3, 3, "OperationButton", "+")

        # Boutons de contrôle (ligne supplémentaire)
        self._create_button(buttons_layout, "C", 4, 0, "ControlButton", "C")
        self._create_button(
            buttons_layout, "⌫", 4, 2, "ControlButton", "⌫"
        )
        self._create_button(
            buttons_layout, "⌫", 4, 2, "ControlButton", "⌫"
        )

        # Bouton vide pour l'équilibre
        empty_button = QPushButton()
        empty_button.setVisible(False)
        buttons_layout.addWidget(empty_button, 4, 3)

        layout.addWidget(buttons_widget)

    def _create_button(self, layout, text, row, col, button_type, value):
        """
        Crée un bouton et l'ajoute au layout.

        Args:
            layout: Layout où ajouter le bouton
            text: Texte du bouton
            row: Ligne dans le grid
            col: Colonne dans le grid
            button_type: Type du bouton (pour le style)
            value: Valeur associée au bouton
        """
        button = CalculatorButton(text, button_type)
        button.setObjectName(f"{text}Button")

        # Configurer les signaux
        if button_type == "DigitButton":
            button.clicked_with_value.connect(
            lambda v=value: self.digit_clicked.emit(v)
        elif button_type == "DecimalButton":
            button.clicked_with_value.connect(
            lambda: self.decimal_clicked.emit()
        elif button_type == "OperationButton":
            button.clicked_with_value.connect(
            lambda v=value: self.operation_clicked.emit(v)
        elif button_type == "ControlButton":
            if value == "C":
                button.clicked_with_value.connect(
            lambda: self.clear_clicked.emit()
            elif value == "CE":
                button.clicked_with_value.connect(
            lambda: self.clear_all_clicked.emit()
            elif value == "⌫":
                button.clicked_with_value.connect(
            lambda: self.backspace_clicked.emit()

        layout.addWidget(button, row, col)

    def _setup_history_section(self, layout):
        """Crée la zone de l'historique."""
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setSpacing(5)

        # Titre
        history_title = QLabel("Historique")
        history_title.setObjectName("HistoryTitle")
        history_title.setStyleSheet("color: #6c7086; font-size: 12px;")
        history_layout.addWidget(history_title)

        # Liste de l'historique
        self.history_list = QListWidget()
        self.history_list.setObjectName("HistoryList")
        self.history_list.setMaximumHeight(100)
        history_layout.addWidget(self.history_list)

        # Bouton pour effacer l'historique
        clear_history_btn = QPushButton("Effacer")
        clear_history_btn.setObjectName("ClearHistoryButton")
        clear_history_btn.clicked.connect(self.history_cleared.emit)
        history_layout.addWidget(clear_history_btn)

        layout.addWidget(history_widget)

    def _setup_storage_info(self, layout):
        """Crée la zone d'information de stockage."""
        storage_info_layout = QHBoxLayout()
        storage_info_layout.setSpacing(10)

        # Label d'information
        self.storage_info_label = QLabel()
        self.storage_info_label.setObjectName("StorageInfoLabel")
        storage_info_layout.addWidget(self.storage_info_label)

        # Bouton pour changer de stockage
        self.storage_button = QPushButton("JSON")
        self.storage_button.setObjectName("StorageButton")
        self.storage_button.setToolTip("Changer de type de stockage")
        storage_info_layout.addWidget(self.storage_button)

        layout.addLayout(storage_info_layout)

    def _connect_signals(self):
        """Connecte les signaux du ViewModel aux slots de la Vue."""
        if self.viewmodel:
            # Connexion des propriétés
            pass

    def _apply_theme(self):
        """Applique le thème CSS."""
        self.setStyleSheet(DARK_THEME)

    def update_display(self, value: str):
        """
        Met à jour l'affichage principal.

        Args:
            value: Valeur à afficher
        """
        self.display.set_value(value)

    def update_operation_display(self, operation: str):
        """
        Met à jour l'affichage de l'opération.

        Args:
            operation: Opération à afficher
        """
        self.operation_display.set_operation(operation)

    def update_history(self, history: list):
        """
        Met à jour l'historique.

        Args:
            history: Liste des entrées de l'historique
        """
        self.history_list.clear()
        for entry in history:
            self.history_list.addItem(entry)

    def update_storage_info(self, info: str):
        """
        Met à jour l'information de stockage.

        Args:
            info: Information à afficher
        """
        self.storage_info_label.setText(info)

    def show_error(self, error: str):
        """
        Affiche une erreur.

        Args:
            error: Message d'erreur
        """
        self.display.set_error(error)

    def clear_error(self):
        """Efface l'erreur."""
        self.display.clear_error()

    def set_storage_button_text(self, text: str):
        """
        Définit le texte du bouton de stockage.

        Args:
            text: Texte à afficher
        """
        self.storage_button.setText(text)

    def closeEvent(self, event):
        """
        Gère la fermeture de la fenêtre.

        Args:
            event: Événement de fermeture
        """
        # Sauvegarder l'état avant de fermer
        if self.viewmodel:
            pass  # La sauvegarde est gérée par le ViewModel
        event.accept()

