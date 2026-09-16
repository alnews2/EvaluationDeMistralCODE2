"""
test_ui.py - Tests pour l'interface utilisateur

Ce module contient les tests pour les composants UI de l'application.
"""

import pytest

from PySide6.QtCore import Qt


class TestMainWindow:
    """Tests pour la fenêtre principale."""

    def test_window_initialization(self, main_window):
        """Test l'initialisation de la fenêtre principale."""
        assert main_window is not None
        assert main_window.windowTitle() == "CalculatorApp"
        assert main_window.width() == 400
        assert main_window.height() == 700

    def test_display_widgets_exist(self, main_window):
        """Test que les widgets d'affichage existent."""
        assert hasattr(main_window, "display")
        assert hasattr(main_window, "operation_display")
        assert hasattr(main_window, "history_list")

    def test_display_initial_value(self, main_window):
        """Test la valeur initiale de l'affichage."""
        # La valeur initiale devrait être "0"
        assert main_window.display.text() == "0"

    def test_buttons_exist(self, main_window):
        """Test que les boutons existent."""
        # Vérifier que les signaux sont connectés
        assert hasattr(main_window, "digit_clicked")
        assert hasattr(main_window, "decimal_clicked")
        assert hasattr(main_window, "operation_clicked")
        assert hasattr(main_window, "clear_clicked")
        assert hasattr(main_window, "clear_all_clicked")
        assert hasattr(main_window, "backspace_clicked")
        assert hasattr(main_window, "history_cleared")


class TestDisplayComponent:
    """Tests pour le composant Display."""

    def test_display_creation(self, qtbot):
        """Test la création du composant Display."""
        from src.ui.components.display import Display

        display = Display()
        qtbot.addWidget(display)

        assert display.text() == "0"
        assert display.alignment() == (Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def test_display_set_value(self, qtbot):
        """Test la mise à jour de la valeur du Display."""
        from src.ui.components.display import Display

        display = Display()
        qtbot.addWidget(display)

        display.set_value("42")
        assert display.text() == "42"

    def test_display_error(self, qtbot):
        """Test l'affichage d'une erreur."""
        from src.ui.components.display import Display

        display = Display()
        qtbot.addWidget(display)

        display.set_error("Erreur")
        assert display.text() == "Erreur"

    def test_display_clear_error(self, qtbot):
        """Test l'effacement de l'erreur."""
        from src.ui.components.display import Display

        display = Display()
        qtbot.addWidget(display)

        display.set_error("Erreur")
        display.clear_error()

        # Après clear_error, le style devrait être réinitialisé
        assert display.styleSheet() == ""


class TestOperationDisplayComponent:
    """Tests pour le composant OperationDisplay."""

    def test_operation_display_creation(self, qtbot):
        """Test la création du composant OperationDisplay."""
        from src.ui.components.display import OperationDisplay

        op_display = OperationDisplay()
        qtbot.addWidget(op_display)

        assert op_display.text() == ""

    def test_operation_display_set_operation(self, qtbot):
        """Test la mise à jour de l'opération."""
        from src.ui.components.display import OperationDisplay

        op_display = OperationDisplay()
        qtbot.addWidget(op_display)

        op_display.set_operation("5 + 3")
        assert op_display.text() == "5 + 3"

    def test_operation_display_clear(self, qtbot):
        """Test l'effacement de l'opération."""
        from src.ui.components.display import OperationDisplay

        op_display = OperationDisplay()
        qtbot.addWidget(op_display)

        op_display.set_operation("5 + 3")
        op_display.clear()

        assert op_display.text() == ""


class TestCalculatorButton:
    """Tests pour le composant CalculatorButton."""

    def test_button_creation(self, qtbot):
        """Test la création du bouton."""
        from src.ui.components.button import CalculatorButton

        button = CalculatorButton("5", "digit")
        qtbot.addWidget(button)

        assert button.text() == "5"
        assert button.button_type == "digit"

    def test_button_size(self, qtbot):
        """Test la taille du bouton."""
        from src.ui.components.button import CalculatorButton

        button = CalculatorButton("5", "digit")
        qtbot.addWidget(button)

        # Le bouton devrait avoir une taille minimale
        assert button.minimumWidth() == 80
        assert button.minimumHeight() == 80

    def test_button_signal(self, qtbot):
        """Test le signal du bouton."""
        from src.ui.components.button import CalculatorButton

        button = CalculatorButton("5", "digit")
        qtbot.addWidget(button)

        # Capturer le signal
        received_value = None

        def on_clicked(value):
            nonlocal received_value
            received_value = value

        button.clicked_with_value.connect(on_clicked)

        # Simuler un clic
        qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

        assert received_value == "5"


class TestViewModelIntegration:
    """Tests d'intégration entre Vue et ViewModel."""

    def test_viewmodel_initialization(self, viewmodel_json):
        """Test l'initialisation du ViewModel."""
        assert viewmodel_json is not None
        assert viewmodel_json.display_value == "0"
        assert viewmodel_json.error is None

    def test_viewmodel_digit_clicked(self, viewmodel_json):
        """Test le clic sur un chiffre dans le ViewModel."""
        viewmodel_json.on_digit_clicked("5")

        assert viewmodel_json.display_value == "5"

    def test_viewmodel_operation_clicked(self, viewmodel_json):
        """Test le clic sur une opération dans le ViewModel."""
        viewmodel_json.on_digit_clicked("5")
        viewmodel_json.on_operation_clicked("+")
        viewmodel_json.on_digit_clicked("3")
        viewmodel_json.on_operation_clicked("=")

        assert viewmodel_json.display_value == "8"

    def test_viewmodel_clear(self, viewmodel_json):
        """Test la fonction Clear dans le ViewModel."""
        viewmodel_json.on_digit_clicked("5")
        viewmodel_json.on_clear_clicked()

        assert viewmodel_json.display_value == "0"

    def test_viewmodel_clear_all(self, viewmodel_json):
        """Test la fonction Clear All dans le ViewModel."""
        viewmodel_json.on_digit_clicked("5")
        viewmodel_json.on_operation_clicked("+")
        viewmodel_json.on_digit_clicked("3")
        viewmodel_json.on_operation_clicked("=")
        viewmodel_json.on_clear_all_clicked()

        assert viewmodel_json.display_value == "0"
        assert len(viewmodel_json.history) == 0

    def test_viewmodel_backspace(self, viewmodel_json):
        """Test la fonction Backspace dans le ViewModel."""
        viewmodel_json.on_digit_clicked("123")
        viewmodel_json.on_backspace_clicked()

        assert viewmodel_json.display_value == "12"


class TestWindowUpdateMethods:
    """Tests pour les méthodes de mise à jour de la fenêtre."""

    def test_update_display(self, main_window):
        """Test la mise à jour de l'affichage."""
        main_window.update_display("42")

        assert main_window.display.text() == "42"

    def test_update_operation_display(self, main_window):
        """Test la mise à jour de l'affichage de l'opération."""
        main_window.update_operation_display("5 + 3")

        assert main_window.operation_display.text() == "5 + 3"

    def test_update_history(self, main_window):
        """Test la mise à jour de l'historique."""
        history = ["5 + 3 = 8", "10 - 4 = 6"]
        main_window.update_history(history)

        assert main_window.history_list.count() == 2
        assert main_window.history_list.item(0).text() == "5 + 3 = 8"
        assert main_window.history_list.item(1).text() == "10 - 4 = 6"

    def test_show_error(self, main_window):
        """Test l'affichage d'une erreur."""
        main_window.show_error("Division par zéro")

        assert main_window.display.text() == "Division par zéro"

    def test_clear_error(self, main_window):
        """Test l'effacement de l'erreur."""
        main_window.show_error("Division par zéro")
        main_window.clear_error()

        # Après clear_error, le texte devrait être réinitialisé
        assert main_window.display.styleSheet() == ""


class TestStorageInfo:
    """Tests pour l'information de stockage."""

    def test_storage_info_json(self, viewmodel_json):
        """Test l'information de stockage pour JSON."""
        info = viewmodel_json.get_storage_info()

        assert "JSON" in info

    def test_storage_info_sqlite(self, viewmodel_sqlite):
        """Test l'information de stockage pour SQLite."""
        info = viewmodel_sqlite.get_storage_info()

        assert "SQLite" in info


class TestSignalConnections:
    """Tests pour les connexions de signaux."""

    def test_digit_signal_connection(self, main_window, qtbot):
        """Test la connexion du signal digit_clicked."""
        received_digit = None

        def on_digit(digit):
            nonlocal received_digit
            received_digit = digit

        main_window.digit_clicked.connect(on_digit)

        # Simuler l'émission du signal
        main_window.digit_clicked.emit("5")

        assert received_digit == "5"

    def test_operation_signal_connection(self, main_window, qtbot):
        """Test la connexion du signal operation_clicked."""
        received_operation = None

        def on_operation(op):
            nonlocal received_operation
            received_operation = op

        main_window.operation_clicked.connect(on_operation)

        # Simuler l'émission du signal
        main_window.operation_clicked.emit("+")

        assert received_operation == "+"
