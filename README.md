# 🧮 CalculatorApp - Calculatrice 4 opérations

[![CI/CD Pipeline](https://github.com/alnews2/EvaluationDeMistralCODE2/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/alnews2/EvaluationDeMistralCODE2/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/Qt-PySide6-green.svg)](https://www.qt.io/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📌 À propos

**CalculatorApp** est une application de calculatrice 4 opérations (addition, soustraction, multiplication, division) développée en **Python** avec **PySide6** (Qt for Python).

Cette application démontre :
- ✅ Architecture **MVVM** (Model-View-ViewModel)
- ✅ **Double persistance** : JSON + SQLite
- ✅ **Design custom** avec CSS Qt
- ✅ **Tests automatiques complets** (pytest + pytest-qt)
- ✅ **CI/CD automatisée** avec GitHub Actions
- ✅ **Build multiplateforme** (Windows/Linux)

---

## 🚀 Installation et exécution

### Prérequis
- Python 3.10 ou supérieur
- Poetry (recommandé) ou pip

### Installation avec Poetry
```bash
# Cloner le dépôt
git clone https://github.com/alnews2/EvaluationDeMistralCODE2.git
cd EvaluationDeMistralCODE2/CalculatorApp

# Installer les dépendances
poetry install

# Exécuter l'application
poetry run python -m src.main
```

### Installation avec pip
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Exécuter l'application
python -m src.main
```

---

## 📦 Structure du projet

```
CalculatorApp/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée
│   ├── app/
│   │   ├── __init__.py
│   │   ├── calculator.py       # Modèle (Calculations)
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── json_repository.py
│   │   │   └── sqlite_repository.py
│   │   └── viewmodel/
│   │       ├── __init__.py
│   │       └── calculator_viewmodel.py
│   └── ui/
│       ├── __init__.py
│       ├── main_window.py      # Vue principale
│       ├── styles/
│       │   └── dark_theme.css  # Style custom
│       └── components/
│           ├── __init__.py
│           ├── button.py        # Boutons custom
│           └── display.py       # Affichage custom
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Fixtures pytest
│   ├── test_calculator.py      # Tests modèle
│   ├── test_persistence.py     # Tests persistance
│   └── test_ui.py              # Tests UI
├── docs/
│   ├── ARCHITECTURE.md         # Documentation architecture
│   ├── DEVELOPMENT.md          # Guide de développement
│   └── USER_GUIDE.md           # Guide utilisateur
├── scripts/
│   ├── build.py                # Script de build
│   └── package.py              # Script de packaging
├── .github/
│   └── workflows/
│       └── ci-cd.yml           # CI/CD GitHub Actions
├── pyproject.toml              # Configuration Poetry
├── pytest.ini                  # Configuration pytest
├── requirements.txt            # Dépendances pip
└── README.md                   # Documentation principale
```

---

## 🏗️ Architecture

L'application suit le pattern **MVVM** (Model-View-ViewModel) :

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│      View        │◄───►│   ViewModel      │◄───►│      Model       │
│   (main_window)  │     │ (calculator_vm)  │     │   (calculator)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Qt Widgets     │     │   Business Logic │     │   Calculations   │
│   (PySide6)      │     │   (Operations)   │     │   (Math)         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Couches

1. **Model** (`src/app/calculator.py`)
   - Contient la logique métier pure
   - Gère les calculs et l'état
   - Indépendant de l'UI

2. **ViewModel** (`src/app/viewmodel/calculator_viewmodel.py`)
   - Interface entre Model et View
   - Expose les données et commandes
   - Gère la persistance

3. **View** (`src/ui/main_window.py`)
   - Interface utilisateur (PySide6)
   - Reçoit les commandes utilisateur
   - Affiche les données

---

## 🔧 Persistance des données

L'application supporte **deux modes de persistance** :

### 1. JSON (Fichier local)
- Stockage dans `~/.calculatorapp/history.json`
- Format léger et lisible
- Idéal pour les petits volumes de données

### 2. SQLite (Base de données)
- Stockage dans `~/.calculatorapp/calculator.db`
- Requêtes structurées
- Idéal pour l'historique et les requêtes complexes

### Configuration
La persistance active peut être configurée via les variables d'environnement :
```bash
# Utiliser JSON (par défaut)
export CALCULATOR_STORAGE=json

# Utiliser SQLite
export CALCULATOR_STORAGE=sqlite
```

---

## 🧪 Tests

### Exécuter les tests
```bash
# Avec Poetry
poetry run pytest

# Avec pip
python -m pytest
```

### Couverture de code
```bash
poetry run pytest --cov=src --cov-report=html
```

### Tests inclus
- ✅ Tests unitaires du modèle
- ✅ Tests d'intégration de la persistance
- ✅ Tests UI avec pytest-qt
- ✅ Tests de régression

---

## 📦 Build et packaging

### Build pour développement
```bash
# Créer un exécutable avec pyinstaller
poetry run python scripts/build.py
```

### Build pour production
```bash
# Windows
poetry run python scripts/build.py --platform windows

# Linux
poetry run python scripts/build.py --platform linux
```

### Packaging
Les builds sont générés dans le dossier `build/` :
```
build/
├── windows/
│   └── CalculatorApp.exe
└── linux/
    └── CalculatorApp
```

---

## 🤖 CI/CD

Le pipeline CI/CD (GitHub Actions) effectue automatiquement :

1. **Linting** (flake8, black, isort)
2. **Tests** (pytest avec couverture)
3. **Build** (Windows/Linux)
4. **Création de release** (pour les tags)

### Workflow
- Push sur `main` : exécute lint + tests
- Push sur `release/*` : exécute lint + tests + build
- Tag `v*` : crée une release avec les artefacts

---

## 📝 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Architecture détaillée de l'application |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Guide de développement et contribution |
| [USER_GUIDE.md](docs/USER_GUIDE.md) | Guide utilisateur complet |

---

## 🎨 Design UI

### Thème Custom (CSS Qt)
L'application utilise un thème sombre personnalisé :
- Fond sombre avec accents colorés
- Boutons avec effets hover/pressed
- Affichage clair et lisible

### Aperçu
```
┌─────────────────────────────────┐
│  CalculatorApp                   │
│ ┌─────────────────────────────┐ │
│ │         0.0                 │ │
│ │ ┌───┐ ┌───┐ ┌───┐ ┌───┐     │ │
│ │ │ 7 │ │ 8 │ │ 9 │ │ / │     │ │
│ │ ├───┤ ├───┤ ├───┤ ├───┤     │ │
│ │ │ 4 │ │ 5 │ │ 6 │ │ * │     │ │
│ │ ├───┤ ├───┤ ├───┤ ├───┤     │ │
│ │ │ 1 │ │ 2 │ │ 3 │ │ - │     │ │
│ │ ├───┤ ├───┤ ├───┤ ├───┤     │ │
│ │ │ 0 │ │ . │ │ = │ │ + │     │ │
│ │ └───┘ └───┘ └───┘ └───┘     │ │
│ │                                 │ │
│ │     [C] [CE] [⌫]              │ │
│ └─────────────────────────────┘ │
└─────────────────────────────────┘
```

---

## 📜 License

Ce projet est sous license **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voir [DEVELOPMENT.md](docs/DEVELOPMENT.md) pour les instructions.

---

## 📞 Support

Pour toute question ou problème, ouvrir une issue sur le dépôt GitHub.
