# 🏗️ Architecture de CalculatorApp

Ce document décrit en détail l'architecture logicielle de **CalculatorApp**, une calculatrice 4 opérations développée avec **PySide6** en suivant le pattern **MVVM** (Model-View-ViewModel).

---

## 📐 Vue d'ensemble

CalculatorApp est structurée selon une **architecture en couches** qui sépare clairement :
- **La logique métier** (Model)
- **La logique de présentation** (ViewModel)
- **L'interface utilisateur** (View)
- **La persistance des données** (Repositories)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CalculatorApp                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
│  │      View        │    │   ViewModel      │    │      Model       │      │
│  │   (main_window)  │◄──►│ (calculator_vm)  │◄──►│   (calculator)   │      │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘      │
│           ▲                         ▲                         ▲            │
│           │                         │                         │            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐      │
│  │   Qt Widgets     │    │   Business Logic │    │   Calculations   │      │
│  │   (PySide6)      │    │   (Operations)   │    │   (Math)         │      │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘      │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Persistence Layer                              │   │
│  │  ┌─────────────────┐    ┌─────────────────┐                         │   │
│  │  │  JsonRepository  │    │ SQLiteRepository │                         │   │
│  │  │  (JSON file)     │    │  (SQLite DB)     │                         │   │
│  │  └─────────────────┘    └─────────────────┘                         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Structure du projet

```
CalculatorApp/
├── src/
│   ├── __init__.py
│   ├── main.py                          # Point d'entrée de l'application
│   │
│   ├── app/                             # Package de la logique métier
│   │   ├── __init__.py
│   │   ├── calculator.py                # Modèle (Calculator)
│   │   │
│   │   ├── persistence/                 # Package de persistance
│   │   │   ├── __init__.py
│   │   │   ├── json_repository.py      # Repository JSON
│   │   │   └── sqlite_repository.py    # Repository SQLite
│   │   │
│   │   └── viewmodel/                  # Package ViewModel
│   │       ├── __init__.py
│   │       └── calculator_viewmodel.py # ViewModel de la calculatrice
│   │
│   └── ui/                              # Package de l'interface utilisateur
│       ├── __init__.py
│       ├── main_window.py              # Fenêtre principale
│       │
│       ├── components/                 # Composants UI personnalisés
│       │   ├── __init__.py
│       │   ├── button.py                # Bouton personnalisé
│       │   └── display.py               # Composants d'affichage
│       │
│       └── styles/                     # Styles CSS
│           ├── __init__.py
│           └── dark_theme.py            # Thème sombre personnalisé
│
├── tests/                            # Tests automatiques
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures pytest
│   ├── test_calculator.py             # Tests du modèle
│   ├── test_persistence.py            # Tests de la persistance
│   └── test_ui.py                     # Tests de l'UI
│
├── docs/                             # Documentation
│   ├── ARCHITECTURE.md                # Ce document
│   ├── DEVELOPMENT.md                 # Guide de développement
│   └── USER_GUIDE.md                  # Guide utilisateur
│
├── scripts/                          # Scripts utilitaires
│   ├── build.py                       # Script de build
│   └── package.py                     # Script de packaging
│
├── .github/                          # Configuration GitHub
│   └── workflows/
│       └── ci-cd.yml                  # Pipeline CI/CD
│
├── pyproject.toml                    # Configuration Poetry
├── pytest.ini                         # Configuration pytest
├── .coveragerc                        # Configuration coverage
├── requirements.txt                   # Dépendances pip
├── README.md                          # Documentation principale
└── LICENSE                            # License MIT
```

---

## 🏗️ Couches architecturales

### 1. Model (Couche métier)

**Fichier** : `src/app/calculator.py`

**Responsabilités** :
- Gestion de l'état de la calculatrice
- Implémentation des opérations mathématiques (+, -, *, /)
- Gestion de l'historique des calculs
- Gestion des erreurs (division par zéro, etc.)
- Formatage des nombres pour l'affichage

**Classes principales** :

```python
class Calculator:
    # Gère l'état et les opérations
    
class CalculationHistory:
    # Gère l'historique des calculs
    
class OperationType(Enum):
    # Types d'opérations supportées
```

**Diagramme de classes** :

```
┌─────────────────────────────────────────────────────────────┐
│                          Calculator                              │
├─────────────────────────────────────────────────────────────┤
│ + current_value: str                                      │
│ + previous_value: Optional[str]                            │
│ + current_operation: Optional[OperationType]               │
│ + waiting_for_operand: bool                                │
│ + error: Optional[str]                                    │
│ + history: CalculationHistory                              │
├─────────────────────────────────────────────────────────────┤
│ + append_digit(digit: str)                                │
│ + append_decimal()                                        │
│ + set_operation(op_type: OperationType)                   │
│ + backspace()                                             │
│ + reset()                                                 │
│ + clear_all()                                             │
│ + get_state() -> dict                                     │
│ + set_state(state: dict)                                 │
└─────────────────────────────────────────────────────────────┘
              ▲
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                     CalculationHistory                          │
├─────────────────────────────────────────────────────────────┤
│ + entries: List[str]                                       │
├─────────────────────────────────────────────────────────────┤
│ + add(expression: str, result: str)                        │
│ + clear()                                                 │
│ + get_all() -> List[str]                                  │
│ + get_last(n: int) -> List[str]                          │
└─────────────────────────────────────────────────────────────┘
```

**Caractéristiques** :
- ✅ **Indépendant de l'UI** : Peut être testé unitairement
- ✅ **Gestion d'état complète** : Sauvegarde et restauration de l'état
- ✅ **Historique des calculs** : Stockage des opérations effectuées
- ✅ **Gestion des erreurs** : Détection et récupération des erreurs
- ✅ **Formatage intelligent** : Gestion des grands nombres et décimaux

---

### 2. ViewModel (Couche de présentation)

**Fichier** : `src/app/viewmodel/calculator_viewmodel.py`

**Responsabilités** :
- Interface entre Model et View
- Gestion de la persistance (JSON ou SQLite)
- Exposition des propriétés pour la Vue
- Gestion des commandes utilisateur
- Synchronisation entre Model et View

**Classes principales** :

```python
class CalculatorViewModel:
    # Fait l'interface entre Calculator et MainWindow
    
class StorageType:
    # Types de stockage supportés (JSON, SQLite)
```

**Diagramme de classes** :

```
┌─────────────────────────────────────────────────────────────┐
│                   CalculatorViewModel                          │
├─────────────────────────────────────────────────────────────┤
│ - calculator: Calculator                                    │
│ - _storage_type: str                                       │
│ - _repository: AbstractRepository                           │
├─────────────────────────────────────────────────────────────┤
│ + display_value: str (property)                             │
│ + operation_display: str (property)                         │
│ + error: Optional[str] (property)                           │
│ + history: List[str] (property)                             │
│ + has_history: bool (property)                             │
├─────────────────────────────────────────────────────────────┤
│ + on_digit_clicked(digit: str)                            │
│ + on_decimal_clicked()                                    │
│ + on_operation_clicked(operation: str)                    │
│ + on_clear_clicked()                                       │
│ + on_clear_all_clicked()                                   │
│ + on_backspace_clicked()                                   │
│ + on_history_cleared()                                     │
│ + get_storage_info() -> str                                │
│ + switch_storage(storage_type: str)                       │
└─────────────────────────────────────────────────────────────┘
              ▲
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AbstractRepository                         │
├─────────────────────────────────────────────────────────────┤
│ + save_state(state: dict)                                  │
│ + load_state() -> Optional[dict]                           │
│ + save_history(history: List[str])                         │
│ + load_history() -> List[str]                              │
│ + save_all(state: dict, history: List[str])                 │
│ + load_all() -> dict                                       │
│ + clear()                                                  │
│ + delete()                                                │
└─────────────────────────────────────────────────────────────┘
              ▲                              ▲
              │                              │
┌─────────────────┐              ┌─────────────────┐
│ JsonRepository  │              │ SQLiteRepository │
└─────────────────┘              └─────────────────┘
```

**Caractéristiques** :
- ✅ **Abstraction de la persistance** : Permet de changer de backend facilement
- ✅ **Exposition des propriétés** : Données accessibles par la Vue
- ✅ **Gestion des commandes** : Traitement des actions utilisateur
- ✅ **Synchronisation automatique** : Sauvegarde de l'état après chaque action
- ✅ **Support multi-storage** : JSON et SQLite interchangeables

---

### 3. View (Couche d'interface)

**Fichier** : `src/ui/main_window.py`

**Responsabilités** :
- Affichage de l'interface utilisateur
- Gestion des interactions utilisateur
- Communication avec le ViewModel via signaux
- Application du style CSS

**Classes principales** :

```python
class MainWindow(QMainWindow):
    # Fenêtre principale de l'application
    
class CalculatorButton(QPushButton):
    # Bouton personnalisé
    
class Display(QLabel):
    # Composant d'affichage principal
    
class OperationDisplay(QLabel):
    # Composant d'affichage de l'opération
```

**Diagramme de classes** :

```
┌─────────────────────────────────────────────────────────────┐
│                        MainWindow                             │
├─────────────────────────────────────────────────────────────┤
│ - viewmodel: CalculatorViewModel                            │
│ - display: Display                                          │
│ - operation_display: OperationDisplay                       │
│ - history_list: QListWidget                                 │
│ - storage_info_label: QLabel                               │
│ - storage_button: QPushButton                              │
├─────────────────────────────────────────────────────────────┤
│ # Signaux                                                  │
│ + digit_clicked: Signal(str)                               │
│ + decimal_clicked: Signal()                                │
│ + operation_clicked: Signal(str)                           │
│ + clear_clicked: Signal()                                  │
│ + clear_all_clicked: Signal()                              │
│ + backspace_clicked: Signal()                              │
│ + history_cleared: Signal()                                │
├─────────────────────────────────────────────────────────────┤
│ # Slots                                                    │
│ + update_display(value: str)                               │
│ + update_operation_display(operation: str)                 │
│ + update_history(history: List[str])                      │
│ + update_storage_info(info: str)                           │
│ + show_error(error: str)                                  │
│ + clear_error()                                            │
│ + set_storage_button_text(text: str)                       │
└─────────────────────────────────────────────────────────────┘
```

**Hiérarchie des composants UI** :

```
MainWindow (QMainWindow)
└── CentralWidget (QWidget)
    ├── DisplaySection (QVBoxLayout)
    │   ├── OperationDisplay (QLabel)
    │   └── Display (QLabel)
    │
    ├── ButtonsSection (QGridLayout)
    │   ├── CalculatorButton (7)
    │   ├── CalculatorButton (8)
    │   ├── CalculatorButton (9)
    │   ├── CalculatorButton (/)
    │   ├── CalculatorButton (4)
    │   ├── CalculatorButton (5)
    │   ├── CalculatorButton (6)
    │   ├── CalculatorButton (*)
    │   ├── CalculatorButton (1)
    │   ├── CalculatorButton (2)
    │   ├── CalculatorButton (3)
    │   ├── CalculatorButton (-)
    │   ├── CalculatorButton (0)
    │   ├── CalculatorButton (.)
    │   ├── CalculatorButton (=)
    │   └── CalculatorButton (+)
    │
    ├── ControlButtons (QGridLayout)
    │   ├── CalculatorButton (C)
    │   ├── CalculatorButton (CE)
    │   └── CalculatorButton (⌫)
    │
    ├── HistorySection (QVBoxLayout)
    │   ├── HistoryTitle (QLabel)
    │   ├── HistoryList (QListWidget)
    │   └── ClearHistoryButton (QPushButton)
    │
    └── StorageInfoSection (QHBoxLayout)
        ├── StorageInfoLabel (QLabel)
        └── StorageButton (QPushButton)
```

**Caractéristiques** :
- ✅ **Style CSS personnalisé** : Thème sombre avec effets hover/pressed
- ✅ **Composants réutilisables** : Boutons et affichages personnalisés
- ✅ **Signaux Qt** : Communication asynchrone avec le ViewModel
- ✅ **Responsive design** : Adapté à différentes tailles d'écran
- ✅ **Accessibilité** : Boutons avec tooltips

---

## 🔄 Flux de données

### Flux utilisateur → Application

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Utilisateur│     │    Main     │     │ Calculator  │
│   (Clic)     │────►│   Window    │────►│  ViewModel   │
└─────────────┘     └─────────────┘     └─────────────┘
                                      │
                                      ▼
                                ┌─────────────┐
                                │  Calculator  │
                                │   (Model)    │
                                └─────────────┘
                                      │
                                      ▼
                                ┌─────────────┐
                                │ Repository  │
                                │ (JSON/SQLite)│
                                └─────────────┘
```

1. **L'utilisateur clique** sur un bouton (ex: "5")
2. **MainWindow** émet le signal `digit_clicked("5")`
3. **CalculatorViewModel** reçoit le signal et appelle `on_digit_clicked("5")`
4. **CalculatorViewModel** appelle `calculator.append_digit("5")`
5. **Calculator** met à jour son état (`current_value = "5"`)
6. **CalculatorViewModel** sauvegarde l'état via le repository
7. **CalculatorViewModel** expose la nouvelle valeur via la propriété `display_value`
8. **MainWindow** met à jour l'affichage via `update_display("5")`

### Flux Application → Utilisateur

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Calculator  │     │ Calculator  │     │   Main      │
│   (Model)    │────►│  ViewModel   │────►│   Window    │
└─────────────┘     └─────────────┘     └─────────────┘
                                      │
                                      ▼
                                ┌─────────────┐
                                │   Utilisateur│
                                │   (Affichage)│
                                └─────────────┘
```

1. **Calculator** a un nouvel état (`current_value = "8"`)
2. **CalculatorViewModel** expose `display_value = "8"`
3. **MainWindow** récupère la valeur et appelle `update_display("8")`
4. **L'utilisateur voit** "8" affiché à l'écran

---

## 🗃️ Persistance des données

### Architecture de la persistance

```
┌─────────────────────────────────────────────────────────────┐
│                    CalculatorViewModel                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AbstractRepository                           │
│  (Interface commune pour tous les repositories)                │
└─────────────────────────────────────────────────────────────┘
              ▲                              ▲
              │                              │
┌─────────────────┐              ┌─────────────────┐
│ JsonRepository  │              │ SQLiteRepository │
│                 │              │                 │
│ + storage_path │              │ + storage_path │
│ + save_state() │              │ + save_state() │
│ + load_state() │              │ + load_state() │
│ + save_history()│              │ + save_history()│
│ + load_history()│              │ + load_history()│
│ + save_all()   │              │ + save_all()   │
│ + load_all()   │              │ + load_all()   │
└─────────────────┘              └─────────────────┘
              │                              │
              ▼                              ▼
┌─────────────────┐              ┌─────────────────┐
│ ~/.calculatorapp/│              │ ~/.calculatorapp/│
│ history.json    │              │ calculator.db   │
└─────────────────┘              └─────────────────┘
```

### Comparaison JSON vs SQLite

| Critère | JSON | SQLite |
|---------|------|--------|
| **Format** | Texte (JSON) | Base de données |
| **Lisibilité** | ✅ Très lisible | ❌ Requiert un outil |
| **Taille** | ❌ Croît avec l'historique | ✅ Optimisé |
| **Requêtes** | ❌ Limité | ✅ Puissant (SQL) |
| **Portabilité** | ✅ Simple à copier | ✅ Simple à copier |
| **Vitesse** | ✅ Rapide | ✅ Rapide |
| **Complexité** | ✅ Simple | ⚠️ Moyenne |

### Configuration du stockage

Le type de stockage peut être configuré via :

1. **Variable d'environnement** :
   ```bash
   export CALCULATOR_STORAGE=json    # Utiliser JSON
   export CALCULATOR_STORAGE=sqlite  # Utiliser SQLite
   ```

2. **Paramètre du ViewModel** :
   ```python
   viewmodel = CalculatorViewModel(storage_type="json")
   viewmodel = CalculatorViewModel(storage_type="sqlite")
   ```

---

## 🎨 Architecture UI

### Thème CSS

L'application utilise un **thème sombre personnalisé** défini dans `src/ui/styles/dark_theme.py`.

**Palettes de couleurs** :
- Fond principal : `#1e1e2e`
- Fond secondaire : `#181825`
- Fond des boutons : `#313244`
- Texte principal : `#cdd6f4`
- Texte secondaire : `#6c7086`
- Accent : `#cba6f7`
- Bouton = : `#6c7086` (texte blanc)

**Effets** :
- Hover : Changement de couleur de fond
- Pressed : Changement de couleur de fond + bordure
- Focus : Bordure colorée

### Disposition de l'UI

```
┌─────────────────────────────────────────┐
│  CalculatorApp                          [X] │
├─────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────────────────────┐ │
│  │  5 + 3                              8 │ │
│  │ ┌─────────────────────────────────┐ │ │
│  │ │         8                       │ │ │
│  │ └─────────────────────────────────┘ │ │
│  └─────────────────────────────────────┘ │
│                                                 │
│  ┌─────────────────────────────────────┐ │
│  │ ┌───┐ ┌───┐ ┌───┐ ┌───┐             │ │
│  │ │ 7 │ │ 8 │ │ 9 │ │ / │             │ │
│  │ ├───┤ ├───┤ ├───┤ ├───┤             │ │
│  │ │ 4 │ │ 5 │ │ 6 │ │ * │             │ │
│  │ ├───┤ ├───┤ ├───┤ ├───┤             │ │
│  │ │ 1 │ │ 2 │ │ 3 │ │ - │             │ │
│  │ ├───┤ ├───┤ ├───┤ ├───┤             │ │
│  │ │ 0 │ │ . │ │ = │ │ + │             │ │
│  │ └───┘ └───┘ └───┘ └───┘             │ │
│  └─────────────────────────────────────┘ │
│                                                 │
│  ┌─────────────────────────────────────┐ │
│  │ [C] [CE] [⌫]                           │ │
│  └─────────────────────────────────────┘ │
│                                                 │
│  ┌─────────────────────────────────────┐ │
│  │ Historique                              │ │
│  │ ┌─────────────────────────────────┐ │ │
│  │ │ 5 + 3 = 8                        │ │ │
│  │ │ 10 - 4 = 6                       │ │ │
│  │ └─────────────────────────────────┘ │ │
│  │ [Effacer]                             │ │
│  └─────────────────────────────────────┘ │
│                                                 │
│  JSON: ~/.calculatorapp/history.json    [JSON] │
└─────────────────────────────────────────┘
```

### Composants personnalisés

1. **CalculatorButton** : Bouton avec style personnalisé
   - Types : digit, operation, control, decimal, equals
   - Taille fixe : 80x80 pixels
   - Signaux : `clicked_with_value`

2. **Display** : Zone d'affichage principal
   - Taille minimale : 80 pixels de hauteur
   - Alignement : Droite
   - Style : Fond sombre, texte coloré

3. **OperationDisplay** : Zone d'affichage de l'opération
   - Taille minimale : 40 pixels de hauteur
   - Alignement : Droite
   - Style : Fond sombre, texte gris

---

## 🔧 Communication entre couches

### Signaux Qt

L'application utilise les **signaux Qt** pour une communication asynchrone entre la Vue et le ViewModel :

```python
# Dans MainWindow
class MainWindow(QMainWindow):
    digit_clicked = Signal(str)
    operation_clicked = Signal(str)
    clear_clicked = Signal()
    # ...

# Dans main.py
window.digit_clicked.connect(viewmodel.on_digit_clicked)
window.operation_clicked.connect(viewmodel.on_operation_clicked)
# ...
```

### Propriétés exposées

Le ViewModel expose des propriétés que la Vue peut lire :

```python
class CalculatorViewModel:
    @property
    def display_value(self) -> str:
        return self.calculator.current_value
    
    @property
    def operation_display(self) -> str:
        # Retourne l'opération en cours
        
    @property
    def error(self) -> Optional[str]:
        return self.calculator.error
    
    @property
    def history(self) -> list:
        return self.calculator.history.get_all()
```

### Synchronisation des données

La synchronisation entre les couches se fait de manière **automatique** :

1. **Vue → ViewModel** : Via les signaux Qt
2. **ViewModel → Model** : Appels de méthodes directes
3. **Model → ViewModel** : Via les propriétés
4. **ViewModel → Persistance** : Après chaque action utilisateur
5. **ViewModel → Vue** : La Vue interroge les propriétés

---

## 📊 Diagrammes complémentaires

### Diagramme de séquence (Calcul simple)

```
Utilisateur       MainWindow          CalculatorViewModel       Calculator
    │                  │                      │                   │
    │ Clic sur "5"    │                      │                   │
    │────────────────►│                      │                   │
    │                  │ digit_clicked("5")  │                   │
    │                  │─────────────────────►│                   │
    │                  │                      │ on_digit_clicked("5")
    │                  │                      │──────────────────►│
    │                  │                      │                   │ append_digit("5")
    │                  │                      │◄──────────────────│
    │                  │                      │                   │
    │                  │                      │ save_state()
    │                  │                      │──────────────────►│
    │                  │                      │                   │ (Repository)
    │                  │                      │◄──────────────────│
    │                  │                      │
    │                  │ update_display("5") │                   │
    │◄─────────────────│                      │                   │
    │ Affichage "5"    │                      │                   │
```

### Diagramme de séquence (Opération)

```
Utilisateur       MainWindow          CalculatorViewModel       Calculator
    │                  │                      │                   │
    │ Clic sur "+"    │                      │                   │
    │────────────────►│                      │                   │
    │                  │ operation_clicked("+")│                   │
    │                  │─────────────────────►│                   │
    │                  │                      │ on_operation_clicked("+")
    │                  │                      │──────────────────►│
    │                  │                      │                   │ set_operation(ADDITION)
    │                  │                      │◄──────────────────│
    │                  │                      │
    │ Clic sur "3"    │                      │                   │
    │────────────────►│                      │                   │
    │                  │ digit_clicked("3")   │                   │
    │                  │─────────────────────►│                   │
    │                  │                      │ on_digit_clicked("3")
    │                  │                      │──────────────────►│
    │                  │                      │                   │ append_digit("3")
    │                  │                      │◄──────────────────│
    │                  │                      │
    │ Clic sur "="    │                      │                   │
    │────────────────►│                      │                   │
    │                  │ operation_clicked("=")│                   │
    │                  │─────────────────────►│                   │
    │                  │                      │ on_operation_clicked("=")
    │                  │                      │──────────────────►│
    │                  │                      │                   │ _calculate_result()
    │                  │                      │◄──────────────────│
    │                  │                      │
    │                  │ update_display("8") │                   │
    │◄─────────────────│                      │                   │
    │ Affichage "8"    │                      │                   │
```

---

## 🎯 Bonnes pratiques implémentées

### 1. **Séparation des responsabilités**
- ✅ Chaque couche a une responsabilité unique
- ✅ Pas de logique métier dans l'UI
- ✅ Pas de code UI dans le modèle

### 2. **Testabilité**
- ✅ Modèle indépendant de l'UI → tests unitaires faciles
- ✅ ViewModel testable sans UI → tests d'intégration
- ✅ Injections de dépendances pour les tests

### 3. **Maintenabilité**
- ✅ Code bien structuré et documenté
- ✅ Noms de classes et méthodes explicites
- ✅ Respect des principes SOLID

### 4. **Extensibilité**
- ✅ Architecture modulaire
- ✅ Facile d'ajouter de nouvelles fonctionnalités
- ✅ Support de nouveaux types de persistance

### 5. **Robustesse**
- ✅ Gestion des erreurs à tous les niveaux
- ✅ Validation des entrées
- ✅ Récupération après les erreurs

### 6. **Performance**
- ✅ Persistance asynchrone (ne bloque pas l'UI)
- ✅ Mise en cache des données
- ✅ Optimisation des requêtes

---

## 📚 Références

- [Qt Documentation](https://doc.qt.io/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [MVVM Pattern](https://en.wikipedia.org/wiki/Model–view–viewmodel)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

## 🔗 Voir aussi

- [DEVELOPMENT.md](DEVELOPMENT.md) - Guide de développement
- [USER_GUIDE.md](USER_GUIDE.md) - Guide utilisateur
- [README.md](../README.md) - Documentation principale
