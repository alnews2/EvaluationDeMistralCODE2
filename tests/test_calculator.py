"""
test_calculator.py - Tests unitaires pour le modèle Calculator

Ce module contient tous les tests unitaires pour la classe Calculator.
"""

import pytest

from src.app.calculator import Calculator, CalculationHistory, OperationType


class TestCalculatorInitialization:
    """Tests pour l'initialisation de la calculatrice."""
    
    def test_initial_state(self, calculator):
        """Test que l'état initial est correct."""
        state = calculator.get_state()
        
        assert state["current_value"] == "0"
        assert state["previous_value"] is None
        assert state["current_operation"] is None
        assert state["waiting_for_operand"] is False
        assert state["error"] is None
        assert state["history"] == []
    
    def test_initial_display(self, calculator):
        """Test que la valeur initiale à afficher est '0'."""
        assert calculator.current_value == "0"


class TestCalculatorDigits:
    """Tests pour l'ajout de chiffres."""
    
    def test_append_single_digit(self, calculator):
        """Test l'ajout d'un seul chiffre."""
        calculator.append_digit("5")
        assert calculator.current_value == "5"
    
    def test_append_multiple_digits(self, calculator):
        """Test l'ajout de plusieurs chiffres."""
        calculator.append_digit("1")
        calculator.append_digit("2")
        calculator.append_digit("3")
        assert calculator.current_value == "123"
    
    def test_append_digit_to_zero(self, calculator):
        """Test l'ajout d'un chiffre quand la valeur est '0'."""
        calculator.append_digit("7")
        assert calculator.current_value == "7"
    
    def test_append_zero_to_nonzero(self, calculator):
        """Test l'ajout de zéro à une valeur non nulle."""
        calculator.append_digit("5")
        calculator.append_digit("0")
        assert calculator.current_value == "50"
    
    def test_append_digit_after_operation(self, calculator):
        """Test l'ajout d'un chiffre après une opération."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        assert calculator.current_value == "3"


class TestCalculatorDecimal:
    """Tests pour le point décimal."""
    
    def test_append_decimal_to_zero(self, calculator):
        """Test l'ajout d'un point décimal à zéro."""
        calculator.append_decimal()
        assert calculator.current_value == "0."
    
    def test_append_decimal_to_integer(self, calculator):
        """Test l'ajout d'un point décimal à un entier."""
        calculator.append_digit("42")
        calculator.append_decimal()
        assert calculator.current_value == "42."
    
    def test_append_decimal_to_decimal(self, calculator):
        """Test l'ajout d'un point décimal à un nombre déjà décimal."""
        calculator.append_digit("3")
        calculator.append_decimal()
        calculator.append_decimal()  # Devrait être ignoré
        assert calculator.current_value == "3."
    
    def test_append_digit_after_decimal(self, calculator):
        """Test l'ajout de chiffres après un point décimal."""
        calculator.append_digit("3")
        calculator.append_decimal()
        calculator.append_digit("1")
        calculator.append_digit("4")
        assert calculator.current_value == "3.14"


class TestCalculatorOperations:
    """Tests pour les opérations mathématiques."""
    
    def test_addition(self, calculator):
        """Test l'addition."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        assert calculator.current_value == "8"
    
    def test_subtraction(self, calculator):
        """Test la soustraction."""
        calculator.append_digit("10")
        calculator.set_operation(OperationType.SUBTRACTION)
        calculator.append_digit("4")
        calculator.set_operation(OperationType.EQUALS)
        
        assert calculator.current_value == "6"
    
    def test_multiplication(self, calculator):
        """Test la multiplication."""
        calculator.append_digit("7")
        calculator.set_operation(OperationType.MULTIPLICATION)
        calculator.append_digit("6")
        calculator.set_operation(OperationType.EQUALS)
        
        assert calculator.current_value == "42"
    
    def test_division(self, calculator):
        """Test la division."""
        calculator.append_digit("20")
        calculator.set_operation(OperationType.DIVISION)
        calculator.append_digit("4")
        calculator.set_operation(OperationType.EQUALS)
        
        assert calculator.current_value == "5.0"
    
    def test_division_by_zero(self, calculator):
        """Test la division par zéro."""
        calculator.append_digit("10")
        calculator.set_operation(OperationType.DIVISION)
        calculator.append_digit("0")
        calculator.set_operation(OperationType.EQUALS)
        
        assert calculator.current_value == "Erreur"
        assert calculator.error == "Division par zéro"
    
    def test_chained_operations(self, calculator):
        """Test les opérations en chaîne."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.MULTIPLICATION)
        calculator.append_digit("2")
        calculator.set_operation(OperationType.EQUALS)
        
        # (5 + 3) * 2 = 16
        assert calculator.current_value == "16"
    
    def test_operation_display(self, calculator):
        """Test l'affichage de l'opération."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        
        state = calculator.get_state()
        assert state["current_operation"] == "ADDITION"
        assert state["previous_value"] == "5"


class TestCalculatorControl:
    """Tests pour les fonctions de contrôle."""
    
    def test_clear(self, calculator):
        """Test la fonction Clear."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        
        calculator.reset()
        
        state = calculator.get_state()
        assert state["current_value"] == "0"
        assert state["previous_value"] is None
        assert state["current_operation"] is None
    
    def test_clear_all(self, calculator):
        """Test la fonction Clear All."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        calculator.clear_all()
        
        state = calculator.get_state()
        assert state["current_value"] == "0"
        assert state["history"] == []
    
    def test_backspace(self, calculator):
        """Test la fonction Backspace."""
        calculator.append_digit("123")
        calculator.backspace()
        
        assert calculator.current_value == "12"
    
    def test_backspace_single_digit(self, calculator):
        """Test Backspace sur un seul chiffre."""
        calculator.append_digit("5")
        calculator.backspace()
        
        assert calculator.current_value == "0"


class TestCalculatorHistory:
    """Tests pour l'historique des calculs."""
    
    def test_history_addition(self, calculator):
        """Test l'ajout d'une entrée dans l'historique."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        history = calculator.history.get_all()
        assert len(history) == 1
        assert "5 + 3 = 8" in history[0]
    
    def test_history_multiple_entries(self, calculator):
        """Test plusieurs entrées dans l'historique."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        calculator.append_digit("10")
        calculator.set_operation(OperationType.SUBTRACTION)
        calculator.append_digit("4")
        calculator.set_operation(OperationType.EQUALS)
        
        history = calculator.history.get_all()
        assert len(history) == 2
    
    def test_history_clear(self, calculator):
        """Test l'effacement de l'historique."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        calculator.history.clear()
        
        assert len(calculator.history.get_all()) == 0
    
    def test_history_get_last(self, calculator):
        """Test la récupération des dernières entrées."""
        calculator.append_digit("5")
        calculator.set_operation(OperationType.ADDITION)
        calculator.append_digit("3")
        calculator.set_operation(OperationType.EQUALS)
        
        calculator.append_digit("10")
        calculator.set_operation(OperationType.MULTIPLICATION)
        calculator.append_digit("2")
        calculator.set_operation(OperationType.EQUALS)
        
        last = calculator.history.get_last(1)
        assert len(last) == 1
        assert "10 * 2 = 20" in last[0]


class TestCalculatorState:
    """Tests pour la gestion de l'état."""
    
    def test_get_state(self, calculator_with_state):
        """Test la récupération de l'état."""
        state = calculator_with_state.get_state()
        
        assert state["current_value"] == "25"
        assert state["previous_value"] == "50"
        assert state["current_operation"] == "ADDITION"
    
    def test_set_state(self, calculator):
        """Test la restauration de l'état."""
        state = {
            "current_value": "42",
            "previous_value": "10",
            "current_operation": "ADDITION",
            "waiting_for_operand": False,
            "error": None,
            "history": ["10 + 20 = 30"],
        }
        
        calculator.set_state(state)
        
        new_state = calculator.get_state()
        assert new_state["current_value"] == "42"
        assert new_state["previous_value"] == "10"
        assert new_state["current_operation"] == "ADDITION"


class TestCalculatorEdgeCases:
    """Tests pour les cas particuliers."""
    
    def test_very_long_number(self, calculator):
        """Test les nombres très longs."""
        for _ in range(20):
            calculator.append_digit("1")
        
        # Devrait être tronqué à MAX_DISPLAY_LENGTH
        assert len(calculator.current_value) <= Calculator.MAX_DISPLAY_LENGTH
    
    def test_decimal_operations(self, calculator):
        """Test les opérations avec des décimaux."""
        calculator.append_digit("3")
        calculator.append_decimal()
        calculator.append_digit("14")
        calculator.set_operation(OperationType.MULTIPLICATION)
        calculator.append_digit("2")
        calculator.set_operation(OperationType.EQUALS)
        
        # 3.14 * 2 = 6.28
        assert calculator.current_value.startswith("6.28")
    
    def test_error_recovery(self, calculator):
        """Test la récupération après une erreur."""
        calculator.append_digit("10")
        calculator.set_operation(OperationType.DIVISION)
        calculator.append_digit("0")
        calculator.set_operation(OperationType.EQUALS)
        
        # Devrait être en état d'erreur
        assert calculator.current_value == "Erreur"
        
        # Appuyer sur un chiffre devrait réinitialiser
        calculator.append_digit("5")
        assert calculator.current_value == "5"
        assert calculator.error is None
    
    def test_operation_after_error(self, calculator):
        """Test une opération après une erreur."""
        calculator.append_digit("10")
        calculator.set_operation(OperationType.DIVISION)
        calculator.append_digit("0")
        calculator.set_operation(OperationType.EQUALS)
        
        # Devrait être en état d'erreur
        assert calculator.current_value == "Erreur"
        
        # Appuyer sur une opération devrait réinitialiser
        calculator.set_operation(OperationType.ADDITION)
        assert calculator.current_value == "0"
        assert calculator.error is None


class TestCalculationHistory:
    """Tests pour la classe CalculationHistory."""
    
    def test_history_initialization(self):
        """Test l'initialisation de l'historique."""
        history = CalculationHistory()
        assert history.get_all() == []
    
    def test_history_add(self):
        """Test l'ajout d'entrées dans l'historique."""
        history = CalculationHistory()
        history.add("5 + 3", "8")
        
        assert len(history.get_all()) == 1
        assert "5 + 3 = 8" in history.get_all()[0]
    
    def test_history_clear(self):
        """Test l'effacement de l'historique."""
        history = CalculationHistory()
        history.add("5 + 3", "8")
        history.clear()
        
        assert len(history.get_all()) == 0
    
    def test_history_get_last_empty(self):
        """Test get_last sur un historique vide."""
        history = CalculationHistory()
        
        assert history.get_last(1) == []
    
    def test_history_get_last_multiple(self):
        """Test get_last avec plusieurs entrées."""
        history = CalculationHistory()
        history.add("1 + 1", "2")
        history.add("2 + 2", "4")
        history.add("3 + 3", "6")
        
        last_two = history.get_last(2)
        assert len(last_two) == 2
        assert "2 + 2 = 4" in last_two[0]
        assert "3 + 3 = 6" in last_two[1]
