"""
test_persistence.py - Tests pour la persistance (JSON et SQLite)

Ce module contient tous les tests pour les repositories de persistance.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from src.app.calculator import Calculator, OperationType


class TestJsonRepository:
    """Tests pour le JsonRepository."""

    def test_initialization(self, temp_json_repository):
        """Test l'initialisation du repository JSON."""
        assert temp_json_repository.exists
        assert temp_json_repository.storage_path.exists()

    def test_save_and_load_state(self, temp_json_repository):
        """Test la sauvegarde et le chargement de l'état."""
        state = {
            "current_value": "42",
            "previous_value": "10",
            "current_operation": "ADDITION",
            "waiting_for_operand": False,
            "error": None,
            "history": [],
        }

        temp_json_repository.save_state(state)
        loaded_state = temp_json_repository.load_state()

        assert loaded_state == state

    def test_save_and_load_history(self, temp_json_repository):
        """Test la sauvegarde et le chargement de l'historique."""
        history = ["5 + 3 = 8", "10 - 4 = 6"]

        temp_json_repository.save_history(history)
        loaded_history = temp_json_repository.load_history()

        assert loaded_history == history

    def test_save_and_load_all(self, temp_json_repository):
        """Test la sauvegarde et le chargement de toutes les données."""
        state = {
            "current_value": "42",
            "previous_value": "10",
            "current_operation": "ADDITION",
            "waiting_for_operand": False,
            "error": None,
        }
        history = ["5 + 3 = 8", "10 - 4 = 6"]

        temp_json_repository.save_all(state, history)
        data = temp_json_repository.load_all()

        assert data["state"] == state
        assert data["history"] == history

    def test_clear(self, temp_json_repository):
        """Test l'effacement des données."""
        state = {"current_value": "42"}
        history = ["5 + 3 = 8"]

        temp_json_repository.save_all(state, history)
        temp_json_repository.clear()

        data = temp_json_repository.load_all()
        assert data["state"] == {}
        assert data["history"] == []

    def test_delete(self, temp_json_repository):
        """Test la suppression du fichier."""
        temp_json_repository.delete()

        assert not temp_json_repository.exists

    def test_file_content(self, temp_json_repository):
        """Test le contenu du fichier JSON."""
        state = {"current_value": "42"}
        history = ["5 + 3 = 8"]

        temp_json_repository.save_all(state, history)

        with open(temp_json_repository.storage_path, "r") as f:
            content = json.load(f)

        assert "state" in content
        assert "history" in content
        assert content["state"]["current_value"] == "42"


class TestSQLiteRepository:
    """Tests pour le SQLiteRepository."""

    def test_initialization(self, temp_sqlite_repository):
        """Test l'initialisation du repository SQLite."""
        assert temp_sqlite_repository.exists
        assert temp_sqlite_repository.storage_path.exists()

    def test_save_and_load_state(self, temp_sqlite_repository):
        """Test la sauvegarde et le chargement de l'état."""
        state = {
            "current_value": "42",
            "previous_value": "10",
            "current_operation": "ADDITION",
            "waiting_for_operand": False,
            "error": None,
            "history": [],
        }

        temp_sqlite_repository.save_state(state)
        loaded_state = temp_sqlite_repository.load_state()

        assert loaded_state == state

    def test_save_and_load_history(self, temp_sqlite_repository):
        """Test la sauvegarde et le chargement de l'historique."""
        history = ["5 + 3 = 8", "10 - 4 = 6"]

        temp_sqlite_repository.save_history(history)
        loaded_history = temp_sqlite_repository.load_history()

        assert loaded_history == history

    def test_save_and_load_all(self, temp_sqlite_repository):
        """Test la sauvegarde et le chargement de toutes les données."""
        state = {
            "current_value": "42",
            "previous_value": "10",
            "current_operation": "ADDITION",
            "waiting_for_operand": False,
            "error": None,
        }
        history = ["5 + 3 = 8", "10 - 4 = 6"]

        temp_sqlite_repository.save_all(state, history)
        data = temp_sqlite_repository.load_all()

        assert data["state"] == state
        assert data["history"] == history

    def test_clear(self, temp_sqlite_repository):
        """Test l'effacement des données."""
        state = {"current_value": "42"}
        history = ["5 + 3 = 8"]

        temp_sqlite_repository.save_all(state, history)
        temp_sqlite_repository.clear()

        data = temp_sqlite_repository.load_all()
        assert data["state"] == {}
        assert data["history"] == []

    def test_delete(self, temp_sqlite_repository):
        """Test la suppression du fichier."""
        temp_sqlite_repository.delete()

        assert not temp_sqlite_repository.exists

    def test_history_count(self, temp_sqlite_repository):
        """Test le comptage des entrées de l'historique."""
        history = ["5 + 3 = 8", "10 - 4 = 6", "2 * 3 = 6"]

        temp_sqlite_repository.save_history(history)

        assert temp_sqlite_repository.get_history_count() == 3

    def test_recent_history(self, temp_sqlite_repository):
        """Test la récupération de l'historique récent."""
        history = ["1 + 1 = 2", "2 + 2 = 4", "3 + 3 = 6"]

        temp_sqlite_repository.save_history(history)
        recent = temp_sqlite_repository.get_recent_history(2)

        assert len(recent) == 2
        assert "2 + 2 = 4" in recent[0]
        assert "3 + 3 = 6" in recent[1]


class TestPersistenceIntegration:
    """Tests d'intégration entre Calculator et la persistance."""

    def test_calculator_state_persistence_json(self, temp_json_repository):
        """Test la persistance de l'état de la calculatrice avec JSON."""
        # Créer une calculatrice avec un état
        calc = Calculator()
        calc.append_digit("5")
        calc.set_operation(OperationType.ADDITION)
        calc.append_digit("3")
        calc.set_operation(OperationType.EQUALS)

        # Sauvegarder l'état
        state = calc.get_state()
        history = calc.history.get_all()
        temp_json_repository.save_all(state, history)

        # Créer une nouvelle calculatrice et charger l'état
        new_calc = Calculator()
        data = temp_json_repository.load_all()
        new_calc.set_state(data["state"])
        new_calc.history.entries = data["history"]

        assert new_calc.current_value == "8"
        assert len(new_calc.history.get_all()) == 1

    def test_calculator_state_persistence_sqlite(self, temp_sqlite_repository):
        """Test la persistance de l'état de la calculatrice avec SQLite."""
        # Créer une calculatrice avec un état
        calc = Calculator()
        calc.append_digit("5")
        calc.set_operation(OperationType.ADDITION)
        calc.append_digit("3")
        calc.set_operation(OperationType.EQUALS)

        # Sauvegarder l'état
        state = calc.get_state()
        history = calc.history.get_all()
        temp_sqlite_repository.save_all(state, history)

        # Créer une nouvelle calculatrice et charger l'état
        new_calc = Calculator()
        data = temp_sqlite_repository.load_all()
        new_calc.set_state(data["state"])
        new_calc.history.entries = data["history"]

        assert new_calc.current_value == "8"
        assert len(new_calc.history.get_all()) == 1


class TestRepositorySwitching:
    """Tests pour le changement de repository."""

    def test_switch_from_json_to_sqlite(
        self, temp_json_repository, temp_sqlite_repository
    ):
        """Test le passage de JSON à SQLite."""
        # Sauvegarder des données dans JSON
        state = {"current_value": "42"}
        history = ["5 + 3 = 8"]
        temp_json_repository.save_all(state, history)

        # Charger depuis JSON et sauvegarder dans SQLite
        data = temp_json_repository.load_all()
        temp_sqlite_repository.save_all(data["state"], data["history"])

        # Vérifier que les données sont dans SQLite
        sqlite_data = temp_sqlite_repository.load_all()
        assert sqlite_data["state"]["current_value"] == "42"
        assert sqlite_data["history"] == ["5 + 3 = 8"]

    def test_switch_from_sqlite_to_json(
        self, temp_json_repository, temp_sqlite_repository
    ):
        """Test le passage de SQLite à JSON."""
        # Sauvegarder des données dans SQLite
        state = {"current_value": "42"}
        history = ["5 + 3 = 8"]
        temp_sqlite_repository.save_all(state, history)

        # Charger depuis SQLite et sauvegarder dans JSON
        data = temp_sqlite_repository.load_all()
        temp_json_repository.save_all(data["state"], data["history"])

        # Vérifier que les données sont dans JSON
        json_data = temp_json_repository.load_all()
        assert json_data["state"]["current_value"] == "42"
        assert json_data["history"] == ["5 + 3 = 8"]


class TestConcurrentAccess:
    """Tests pour l'accès concurrent (simulé)."""

    def test_multiple_saves_json(self, temp_json_repository):
        """Test plusieurs sauvegardes consécutives avec JSON."""
        for i in range(10):
            state = {"current_value": str(i)}
            history = [f"{i} + 0 = {i}"]
            temp_json_repository.save_all(state, history)

        data = temp_json_repository.load_all()
        assert data["state"]["current_value"] == "9"

    def test_multiple_saves_sqlite(self, temp_sqlite_repository):
        """Test plusieurs sauvegardes consécutives avec SQLite."""
        for i in range(10):
            state = {"current_value": str(i)}
            history = [f"{i} + 0 = {i}"]
            temp_sqlite_repository.save_all(state, history)

        data = temp_sqlite_repository.load_all()
        assert data["state"]["current_value"] == "9"
