"""
conftest.py - Configuration pytest pour CalculatorApp

Ce module contient les fixtures pytest utilisées dans tous les tests.
"""

import os
import tempfile
from pathlib import Path

import pytest

from src.app.calculator import Calculator, OperationType
from src.app.persistence.json_repository import JsonRepository
from src.app.persistence.sqlite_repository import SQLiteRepository
from src.app.viewmodel.calculator_viewmodel import CalculatorViewModel


# Fixtures pour le modèle

@pytest.fixture
def calculator():
    """Retourne une instance fraîche de Calculator."""
    return Calculator()


@pytest.fixture
def calculator_with_state():
    """Retourne une calculatrice avec un état pré-rempli."""
    calc = Calculator()
    calc.append_digit("5")
    calc.append_digit("0")
    calc.set_operation(OperationType.ADDITION)
    calc.append_digit("2")
    calc.append_digit("5")
    return calc


# Fixtures pour la persistance

@pytest.fixture
def temp_json_repository():
    """Retourne un JsonRepository temporaire."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonRepository(os.path.join(tmpdir, "test_history.json"))
        yield repo


@pytest.fixture
def temp_sqlite_repository():
    """Retourne un SQLiteRepository temporaire."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = SQLiteRepository(os.path.join(tmpdir, "test_calculator.db"))
        yield repo


@pytest.fixture
def json_repository_with_data(temp_json_repository):
    """Retourne un JsonRepository avec des données pré-chargées."""
    state = {
        "current_value": "42",
        "previous_value": "10",
        "current_operation": "ADDITION",
        "waiting_for_operand": False,
        "error": None,
        "history": ["10 + 20 = 30", "30 + 12 = 42"],
    }
    temp_json_repository.save_all(state, state["history"])
    return temp_json_repository


@pytest.fixture
def sqlite_repository_with_data(temp_sqlite_repository):
    """Retourne un SQLiteRepository avec des données pré-chargées."""
    state = {
        "current_value": "42",
        "previous_value": "10",
        "current_operation": "ADDITION",
        "waiting_for_operand": False,
        "error": None,
        "history": ["10 + 20 = 30", "30 + 12 = 42"],
    }
    temp_sqlite_repository.save_all(state, state["history"])
    return temp_sqlite_repository


# Fixtures pour le ViewModel

@pytest.fixture
def viewmodel_json():
    """Retourne un CalculatorViewModel avec stockage JSON."""
    return CalculatorViewModel(storage_type="json")


@pytest.fixture
def viewmodel_sqlite():
    """Retourne un CalculatorViewModel avec stockage SQLite."""
    return CalculatorViewModel(storage_type="sqlite")


# Fixtures pour les tests Qt

@pytest.fixture
def qapp(qtbot):
    """Retourne une application Qt pour les tests UI."""
    from PySide6.QtWidgets import QApplication
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def main_window(qtbot, viewmodel_json):
    """Retourne une MainWindow pour les tests UI."""
    from src.ui.main_window import MainWindow
    
    window = MainWindow(viewmodel_json)
    qtbot.addWidget(window)
    return window


# Configuration pytest

def pytest_configure(config):
    """Configuration pytest."""
    # Désactiver les warnings pour les tests
    config.addinivalue_line("filterwarnings", "ignore::DeprecationWarning")


# Hook pour nettoyer les fichiers temporaires
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook pour nettoyer après les tests."""
    outcome = yield
    rep = outcome.get_result()
    
    # Nettoyer les fichiers de test
    test_dir = Path.home() / ".calculatorapp"
    if test_dir.exists():
        for file in test_dir.glob("test_*"):
            try:
                file.unlink()
            except Exception:
                pass
