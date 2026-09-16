"""
Dark Theme - Style CSS personnalisé pour la calculatrice

Ce module contient le style CSS pour un thème sombre personnalisé.
"""

DARK_THEME = """
/* Thème sombre personnalisé pour CalculatorApp */

/* Fenêtre principale */
QMainWindow {
    background-color: #1e1e2e;
    color: #cdd6f4;
    border: none;
}

/* Widget central */
QWidget#CentralWidget {
    background-color: #1e1e2e;
    margin: 0;
    padding: 0;
}

/* Zone d'affichage */
QLabel#DisplayLabel {
    background-color: #181825;
    color: #cba6f7;
    font-size: 48px;
    font-weight: bold;
    padding: 20px;
    margin: 0;
    border: 2px solid #313244;
    border-radius: 8px;
    text-align: right;
    min-height: 80px;
}

/* Zone d'opération */
QLabel#OperationLabel {
    background-color: #181825;
    color: #6c7086;
    font-size: 24px;
    padding: 10px 20px;
    margin: 0;
    border: none;
    text-align: right;
    min-height: 40px;
}

/* Boutons - Style de base */
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    font-size: 24px;
    font-weight: bold;
    border: 2px solid #45475a;
    border-radius: 8px;
    padding: 15px;
    min-width: 80px;
    min-height: 80px;
    transition: all 0.2s ease;
}

/* Boutons - Effet hover */
QPushButton:hover {
    background-color: #45475a;
    border-color: #6c7086;
}

/* Boutons - Effet pressed */
QPushButton:pressed {
    background-color: #181825;
    border-color: #cba6f7;
}

/* Boutons - Effet disabled */
QPushButton:disabled {
    background-color: #181825;
    color: #6c7086;
    border-color: #313244;
}

/* Boutons numériques (0-9) */
QPushButton.DigitButton {
    background-color: #313244;
    color: #cdd6f4;
}

QPushButton.DigitButton:hover {
    background-color: #45475a;
    color: #f5e0dc;
}

QPushButton.DigitButton:pressed {
    background-color: #181825;
    color: #f5e0dc;
}

/* Boutons d'opération (+, -, *, /, =) */
QPushButton.OperationButton {
    background-color: #313244;
    color: #f5e0dc;
    border-color: #f5e0dc;
}

QPushButton.OperationButton:hover {
    background-color: #45475a;
    color: #f5e0dc;
    border-color: #f5e0dc;
}

QPushButton.OperationButton:pressed {
    background-color: #181825;
    color: #f5e0dc;
    border-color: #f5e0dc;
}

/* Bouton = (spécial) */
QPushButton#EqualsButton {
    background-color: #6c7086;
    color: #1e1e2e;
    border-color: #6c7086;
    font-weight: bold;
}

QPushButton#EqualsButton:hover {
    background-color: #7c7f96;
    color: #1e1e2e;
    border-color: #7c7f96;
}

QPushButton#EqualsButton:pressed {
    background-color: #5c5f76;
    color: #1e1e2e;
    border-color: #5c5f76;
}

/* Boutons de contrôle (C, CE, ⌫) */
QPushButton.ControlButton {
    background-color: #45475a;
    color: #cdd6f4;
    border-color: #6c7086;
}

QPushButton.ControlButton:hover {
    background-color: #5c5f76;
    color: #f5e0dc;
    border-color: #7c7f96;
}

QPushButton.ControlButton:pressed {
    background-color: #313244;
    color: #f5e0dc;
    border-color: #6c7086;
}

/* Bouton point décimal */
QPushButton#DecimalButton {
    background-color: #313244;
    color: #cdd6f4;
}

QPushButton#DecimalButton:hover {
    background-color: #45475a;
    color: #f5e0dc;
}

QPushButton#DecimalButton:pressed {
    background-color: #181825;
    color: #f5e0dc;
}

/* Zone de l'historique */
QListWidget#HistoryList {
    background-color: #181825;
    color: #cdd6f4;
    border: 2px solid #313244;
    border-radius: 8px;
    padding: 10px;
    font-size: 14px;
}

QListWidget#HistoryList::item {
    padding: 8px;
    border-bottom: 1px solid #313244;
}

QListWidget#HistoryList::item:selected {
    background-color: #313244;
    color: #f5e0dc;
}

/* Bouton de basculement de stockage */
QPushButton#StorageButton {
    background-color: #313244;
    color: #cba6f7;
    font-size: 12px;
    padding: 8px;
    min-width: 40px;
    min-height: 40px;
    border-radius: 6px;
}

QPushButton#StorageButton:hover {
    background-color: #45475a;
    color: #cba6f7;
}

/* Grille des boutons */
QGridLayout {
    spacing: 10px;
    margin: 15px;
}

/* Layout principal */
QVBoxLayout {
    spacing: 15px;
    margin: 15px;
}

/* Info de stockage */
QLabel#StorageInfoLabel {
    background-color: #181825;
    color: #6c7086;
    font-size: 10px;
    padding: 5px;
    border: none;
    text-align: center;
}

/* Bouton Clear History */
QPushButton#ClearHistoryButton {
    background-color: #45475a;
    color: #cdd6f4;
    font-size: 12px;
    padding: 8px;
    min-width: 60px;
    border-radius: 6px;
}

QPushButton#ClearHistoryButton:hover {
    background-color: #5c5f76;
    color: #f5e0dc;
}

/* Scrollbar pour l'historique */
QScrollBar:vertical {
    background: #181825;
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: #313244;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #45475a;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    background: none;
    border: none;
}

/* Effet de focus pour tous les boutons */
QPushButton:focus {
    outline: 2px solid #cba6f7;
}

/* Style pour les tooltips */
QToolTip {
    background-color: #181825;
    color: #cdd6f4;
    border: 2px solid #313244;
    padding: 5px;
    font-size: 12px;
}
"""
