"""
MainWindow - Fen\u00eatre principale de l'application calculatrice

Ce module contient la classe MainWindow qui repr\u00e9sente la vue principale
de l'application calculatrice. Elle utilise le ViewModel pour interagir
avec le mod\u00e8le.
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
    Fen\u00eatre principale de la calculatrice.

    Cette classe g\u00e8re :
    - La cr\u00e9ation de l'interface utilisateur
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
        Initialise la fen\u00eatre principale.

        Args:
            viewmodel: Le ViewModel \u00e0 utiliser
            parent: Widget parent
        """
        super().__init__(parent)

        self.viewmodel = viewmodel
        self._setup_window()
        self._setup_ui()
        self._connect_signals()

        # Appliquer le th\u00e8me
        self._apply_theme()

    def _setup_window(self):
        """Configure les propri\u00e9t\u00e9s de la fen\u00eatre."""
        self.setWindowTitle("CalculatorApp")
        self.setFixedSize(400, 700)
        self.setWindowIconName("calculator")

    def _setup_ui(self):
        """Cr\u00e9e l'interface utilisateur."""
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
        """Cr\u00e9e la zone d'affichage."""
        display_layout = QVBoxLayout()
        display_layout.setSpacing(5)

        # Affichage de l'op\u00e9ration
        self.operation_display = OperationDisplay()
        display_layout.addWidget(self.operation_display)

        # Affichage principal
        self.display = Display()
        display_layout.addWidget(self.display)

        layout.addLayout(display_layout)

    def _setup_buttons_section(self, layout):
        """Cr\u00e9e la zone des boutons."""
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Cr\u00e9er les boutons
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

        # Boutons de contr\u00f4le (ligne suppl\u00e9mentaire)
        self._create_button(buttons_layout, "C", 4, 0, "ControlButton", "C")
        self._create_button(buttons_layout, "CE", 4, 1, "ControlButton", "CE")
        self._create_button(buttons_layout, "\u232b", 4, 2, "ControlButton", "\u232b")

        # Bouton vide pour l'\u00e9quilibre
        empty_button = QPushButton()
        empty_button.setVisible(False)
        buttons_layout.addWidget(empty_button, 4, 3)

        layout.addWidget(buttons_widget)

    def _create_button(self, layout, text, row, col, button_type, value):
        """
        Cr\u00e9e un bouton et l'ajoute au layout.

        Args:
            layout: Le layout parent
            text: Texte du bouton
            row: Ligne dans le grid
            col: Colonne dans le grid
            button_type: Type du bouton (pour le style)
            value: Valeur associ\u00e9e au bouton
        """
        button = CalculatorButton(text, button_type)
        button.setObjectName(f"{text}Button")

        # Configurer les signaux
        if button_type == "DigitButton":
            button.clicked_with_value.connect(lambda v=value: self.digit_clicked.emit(v))
        elif button_type == "DecimalButton":
            button.clicked_with_value.connect(lambda: self.decimal_clicked.emit())
        elif button_type == "OperationButton":
            button.clicked_with_value.connect(lambda v=value: self.operation_clicked.emit(v))
        elif button_type == "ControlButton":
            if value == "C":
                button.clicked_with_value.connect(lambda: self.clear_clicked.emit())
            elif value == "CE":
                button.clicked_with_value.connect(lambda: self.clear_all_clicked.emit())
            elif value == "\u232b":
                button.clicked_with_value.connect(lambda: self.backspace_clicked.emit())

        layout.addWidget(button, row, col)

    def _setup_history_section(self, layout):
        """Cr\u00e9e la zone de l'historique."""
        # Cr\u00e9er le widget de l'historique
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)
        history_layout.setContentsMargins(0, 0, 0, 0)

        # Label de l'historique
        history_label = QLabel("Historique :")
        history_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        history_layout.addWidget(history_label)

        # Liste de l'historique
        self.history_list = QListWidget()
        self.history_list.setStyleSheet(
            "QListWidget { background-color: #2d2d2d; border: 1px solid #444; "
            "border-radius: 5px; padding: 5px; }"
            "QListWidget::item { padding: 5px; }"
            "QListWidget::item:selected { background-color: #444; }"
        )
        history_layout.addWidget(self.history_list)

        # Bouton pour effacer l'historique
        clear_history_btn = CalculatorButton("Effacer", "ControlButton")
        clear_history_btn.clicked.connect(self._on_clear_history_clicked)
        history_layout.addWidget(clear_history_btn)

        layout.addWidget(history_widget)

    def _setup_storage_info(self, layout):
        """Affiche les informations de stockage."""
        storage_widget = QWidget()
        storage_layout = QHBoxLayout(storage_widget)
        storage_layout.setContentsMargins(0, 0, 0, 0)

        storage_label = QLabel("Stockage :")
        storage_label.setStyleSheet("font-size: 12px;")
        storage_layout.addWidget(storage_label)

        self.storage_info_label = QLabel()
        self.storage_info_label.setStyleSheet("font-size: 12px; color: #aaa;")
        storage_layout.addWidget(self.storage_info_label)

        layout.addWidget(storage_widget)

    def _connect_signals(self):
        """Connecte les signaux aux slots."""
        # Connecter les signaux du ViewModel
        if self.viewmodel:
            self.digit_clicked.connect(self.viewmodel.on_digit_clicked)
            self.decimal_clicked.connect(self.viewmodel.on_decimal_clicked)
            self.operation_clicked.connect(self.viewmodel.on_operation_clicked)
            self.clear_clicked.connect(self.viewmodel.on_clear_clicked)
            self.clear_all_clicked.connect(self.viewmodel.on_clear_all_clicked)
            self.backspace_clicked.connect(self.viewmodel.on_backspace_clicked)
            self.history_cleared.connect(self.viewmodel.on_history_cleared)

    def _apply_theme(self):
        """Applique le th\u00e8me \u00e0 l'application."""
        self.setStyleSheet(DARK_THEME)

    def update_display(self, value: str):
        """Met \u00e0 jour l'affichage principal."""
        self.display.set_value(value)

    def update_operation_display(self, operation: str):
        """Met \u00e0 jour l'affichage de l'op\u00e9ration."""
        self.operation_display.set_value(operation)

    def update_history(self, history: list):
        """Met \u00e0 jour l'historique."""
        self.history_list.clear()
        for entry in history:
            self.history_list.addItem(entry)

    def update_storage_info(self, info: str):
        """Met \u00e0 jour les informations de stockage."""
        self.storage_info_label.setText(info)

    def show_error(self, error: str):
        """Affiche une erreur."""
        self.display.show_error(error)

    def clear_error(self):
        """Efface l'erreur."""
        self.display.clear_error()

    def set_storage_button_text(self, text: str):
        """D\u00e9finit le texte du bouton de stockage."""
        pass  # Impl\u00e9mentation future

    def _on_clear_history_clicked(self):
        """G\u00e8re le clic sur le bouton Effacer l'historique."""
        self.history_cleared.emit()

    def closeEvent(self, event):
        """G\u00e8re la fermeture de la fen\u00eatre."""
        # Sauvegarder l'\u00e9tat avant de fermer
        if self.viewmodel:
            pass  # La sauvegarde est g\u00e9r\u00e9e par le ViewModel
        event.accept()
