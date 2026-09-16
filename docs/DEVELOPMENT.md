# 🛠️ Guide de Développement - CalculatorApp

Ce document fournit toutes les informations nécessaires pour **développer, tester, contribuer et déployer** CalculatorApp.

---

## 📥 Prérequis

### Environnement
- **Python** : 3.10 ou supérieur (recommandé : 3.11)
- **Système d'exploitation** : Windows, Linux ou macOS
- **Gestionnaire de paquets** : Poetry (recommandé) ou pip

### Dépendances obligatoires
- PySide6 (>= 6.6.0) - Framework Qt pour Python

### Dépendances de développement
- pytest (>= 8.0.0) - Framework de tests
- pytest-qt (>= 4.4.0) - Plugin pytest pour les tests Qt
- pytest-cov (>= 4.1.0) - Plugin pytest pour la couverture de code
- flake8 (>= 6.1.0) - Linter
- black (>= 24.0.0) - Formateur de code
- isort (>= 5.13.0) - Trieur d'imports
- pyinstaller (>= 6.0.0) - Outil de build

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
# Cloner le dépôt GitHub
git clone https://github.com/alnews2/EvaluationDeMistralCODE2.git
cd EvaluationDeMistralCODE2/CalculatorApp

# Créer une branche de développement (optionnel)
git checkout -b develop
```

### 2. Installer avec Poetry (recommandé)

```bash
# Installer Poetry si ce n'est pas déjà fait
curl -sSL https://install.python-poetry.org | python3 -

# Installer les dépendances
poetry install

# Activer l'environnement virtuel
poetry shell

# Exécuter l'application
poetry run python -m src.main
```

### 3. Installer avec pip

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Exécuter l'application
python -m src.main
```

---

## 🏗️ Structure du Projet

```
CalculatorApp/
├── src/                          # Code source principal
│   ├── app/                     # Logique métier
│   │   ├── calculator.py        # Modèle de la calculatrice
│   │   ├── persistence/         # Persistance des données
│   │   │   ├── json_repository.py
│   │   │   └── sqlite_repository.py
│   │   └── viewmodel/          # ViewModels
│   │       └── calculator_viewmodel.py
│   └── ui/                      # Interface utilisateur
│       ├── main_window.py      # Fenêtre principale
│       ├── components/         # Composants personnalisés
│       │   ├── button.py        # Boutons
│       │   └── display.py       # Affichage
│       └── styles/             # Styles CSS
│           └── dark_theme.py    # Thème sombre
├── tests/                        # Tests
│   ├── conftest.py             # Fixtures pytest
│   ├── test_calculator.py      # Tests du modèle
│   ├── test_persistence.py     # Tests de la persistance
│   └── test_ui.py              # Tests de l'UI
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md          # Architecture
│   ├── DEVELOPMENT.md           # Ce document
│   └── USER_GUIDE.md            # Guide utilisateur
├── scripts/                      # Scripts utilitaires
│   ├── build.py                 # Script de build
│   └── package.py               # Script de packaging
├── .github/                      # Configuration GitHub
│   └── workflows/
│       └── ci-cd.yml            # Pipeline CI/CD
├── pyproject.toml              # Configuration Poetry
├── pytest.ini                  # Configuration pytest
├── .coveragerc                 # Configuration coverage
├── requirements.txt            # Dépendances pip
├── README.md                   # Documentation principale
└── LICENSE                      # License MIT
```

---

## 📝 Conventions de Codage

### Style de code

Ce projet suit les conventions suivantes :

1. **Formatage** : Black (line-length = 100)
2. **Tri des imports** : isort
3. **Linting** : flake8
4. **Nommage** :
   - Classes : `PascalCase` (ex: `CalculatorViewModel`)
   - Variables et fonctions : `snake_case` (ex: `display_value`, `on_digit_clicked`)
   - Constantes : `UPPER_SNAKE_CASE` (ex: `MAX_DISPLAY_LENGTH`)
   - Méthodes privées : `_prefix` (ex: `_setup_ui`)

### Exemple de code

```python
# Bon exemple
from typing import Optional

class Calculator:
    """Modèle de la calculatrice."""
    
    MAX_DISPLAY_LENGTH = 15
    
    def __init__(self):
        self._reset_state()
    
    def _reset_state(self):
        """Réinitialise l'état."""
        self.current_value = "0"
        self.previous_value = None
    
    def append_digit(self, digit: str):
        """Ajoute un chiffre.
        
        Args:
            digit: Le chiffre à ajouter (0-9)
        """
        if self.current_value == "0":
            self.current_value = digit
        else:
            self.current_value += digit

# Mauvais exemple (à éviter)
class calculator:
    maxLength = 15
    
    def __init__(self):
        self.current_value = "0"
    
    def appendDigit(d, val):
        if self.current_value == "0":
            self.current_value = val
        else:
            self.current_value += val
```

---

## ⚙️ Configuration de l'Environnement

### Variables d'environnement

| Variable | Description | Valeurs possibles | Défaut |
|----------|-------------|------------------|--------|
| `CALCULATOR_STORAGE` | Type de stockage à utiliser | `json`, `sqlite` | `json` |

**Exemple d'utilisation** :

```bash
# Utiliser SQLite pour la persistance
export CALCULATOR_STORAGE=sqlite

# Exécuter l'application
poetry run python -m src.main
```

### Configuration dans le code

```python
# Dans le ViewModel
viewmodel = CalculatorViewModel(storage_type="sqlite")
```

---

## 🧪 Tests

### Exécuter les tests

```bash
# Exécuter tous les tests
poetry run pytest

# Exécuter avec couverture de code
poetry run pytest --cov=src --cov-report=html

# Exécuter un fichier de test spécifique
poetry run pytest tests/test_calculator.py

# Exécuter un test spécifique
poetry run pytest tests/test_calculator.py::TestCalculatorOperations::test_addition

# Exécuter les tests avec affichage détaillé
poetry run pytest -v

# Exécuter les tests avec capture des prints
poetry run pytest -s
```

### Types de tests

1. **Tests unitaires** (`test_calculator.py`)
   - Testent le modèle Calculator
   - Testent CalculationHistory
   - Pas de dépendance à Qt

2. **Tests de persistance** (`test_persistence.py`)
   - Testent JsonRepository
   - Testent SQLiteRepository
   - Testent l'intégration avec le modèle

3. **Tests UI** (`test_ui.py`)
   - Testent les composants UI
   - Utilisent pytest-qt
   - Nécessitent un environnement Qt

### Écrire de nouveaux tests

**Exemple : Test unitaire pour le modèle**

```python
def test_new_feature(calculator):
    """Test une nouvelle fonctionnalité."""
    # Setup
    calculator.append_digit("5")
    
    # Action
    calculator.new_method()
    
    # Assert
    assert calculator.current_value == "expected"
```

**Exemple : Test UI avec pytest-qt**

```python
def test_button_click(qtbot):
    """Test le clic sur un bouton."""
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
```

---

## 🏗️ Développement de Nouvelles Fonctionnalités

### Ajouter une nouvelle opération

1. **Mettre à jour OperationType**
   ```python
   # Dans src/app/calculator.py
   class OperationType(Enum):
       ADDITION = auto()
       SUBTRACTION = auto()
       MULTIPLICATION = auto()
       DIVISION = auto()
       POWER = auto()  # Nouvelle opération
   ```

2. **Mettre à jour le calcul**
   ```python
   # Dans Calculator._calculate_result()
   elif self.current_operation == OperationType.POWER:
       result = prev ** curr
   ```

3. **Mettre à jour le ViewModel**
   ```python
   # Dans CalculatorViewModel.on_operation_clicked()
   op_map = {
       "+": OperationType.ADDITION,
       "-": OperationType.SUBTRACTION,
       "*": OperationType.MULTIPLICATION,
       "/": OperationType.DIVISION,
       "^": OperationType.POWER,  # Nouveau
   }
   ```

4. **Mettre à jour l'UI**
   ```python
   # Dans MainWindow._setup_buttons_section()
   self._create_button(buttons_layout, "^", 1, 4, "OperationButton", "^")
   ```

5. **Ajouter des tests**
   ```python
   # Dans tests/test_calculator.py
   def test_power(self, calculator):
       calculator.append_digit("2")
       calculator.set_operation(OperationType.POWER)
       calculator.append_digit("3")
       calculator.set_operation(OperationType.EQUALS)
       assert calculator.current_value == "8"
   ```

### Ajouter un nouveau type de stockage

1. **Créer une nouvelle classe Repository**
   ```python
   # Dans src/app/persistence/mongodb_repository.py
   class MongoDBRepository:
       def save_state(self, state):
           # Implémentation
       
       def load_state(self):
           # Implémentation
       
       # ... autres méthodes
   ```

2. **Mettre à jour le ViewModel**
   ```python
   # Dans CalculatorViewModel._create_repository()
   if storage == StorageType.MONGODB:
       return MongoDBRepository()
   ```

3. **Ajouter des tests**
   ```python
   # Dans tests/test_persistence.py
   class TestMongoDBRepository:
       def test_save_and_load(self, temp_mongodb_repository):
           # Test de la nouvelle implémentation
   ```

---

## 📦 Build et Packaging

### Build pour développement

```bash
# Utiliser le script de build
poetry run python scripts/build.py

# Ou utiliser pyinstaller directement
poetry run pyinstaller --onefile --windowed src/main.py
```

### Build pour production

```bash
# Build pour Linux
poetry run python scripts/build.py --platform linux

# Build pour Windows (depuis Windows)
poetry run python scripts/build.py --platform windows

# Build pour toutes les plateformes
poetry run python scripts/build.py --platform all
```

### Options de build

| Option | Description |
|--------|-------------|
| `--platform` | Plateforme cible (`windows`, `linux`, `all`) |
| `--clean` | Nettoyer avant de construire |

### Artefacts de build

Les exécutables sont générés dans le dossier `build/` :

```
build/
├── linux/
│   └── CalculatorApp
└── windows/
    └── CalculatorApp.exe
```

---

## 🚀 Déploiement

### Déploiement local

1. **Build l'application**
   ```bash
   poetry run python scripts/build.py --platform linux --clean
   ```

2. **Exécuter l'application**
   ```bash
   ./build/linux/CalculatorApp
   ```

### Déploiement avec Docker (optionnel)

Créer un Dockerfile :

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "src.main"]
```

Build et exécuter :

```bash
docker build -t calculatorapp .
docker run -it --rm calculatorapp
```

### Création d'une release GitHub

1. **Créer un tag**
   ```bash
   git tag -a v1.0.0 -m "Version 1.0.0"
   git push origin v1.0.0
   ```

2. **Le pipeline CI/CD** s'exécutera automatiquement et créera une release avec les artefacts

---

## 🔄 Workflow de Contribution

### 1. Forker le dépôt

1. Forker le dépôt sur GitHub
2. Cloner votre fork localement

### 2. Créer une branche

```bash
# Se positionner sur main
git checkout main

# Mettre à jour main
git pull origin main

# Créer une nouvelle branche
git checkout -b feature/nom-de-la-fonctionnalite
```

### 3. Développer

- Suivre les conventions de codage
- Ajouter des tests pour les nouvelles fonctionnalités
- Vérifier que tous les tests passent

### 4. Commiter

```bash
# Ajouter les fichiers modifiés
git add .

# Commiter avec un message clair
git commit -m "feat: ajouter nouvelle opération puissance"

# Pousser vers votre fork
git push origin feature/nom-de-la-fonctionnalite
```

### 5. Créer une Pull Request

1. Aller sur GitHub
2. Créer une Pull Request depuis votre branche vers `main`
3. Remplir la description de la PR
4. Attendre la review et les tests CI

### Conventions de commit

Suivre la convention [Conventional Commits](https://www.conventionalcommits.org/) :

| Type | Utilisation |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Modification de la documentation |
| `style` | Modification de style (formatage, etc.) |
| `refactor` | Refactorisation du code |
| `test` | Ajout ou modification de tests |
| `chore` | Tâches de maintenance |

**Exemples** :
```bash
git commit -m "feat: ajouter support SQLite"
git commit -m "fix: corriger division par zéro"
git commit -m "docs: mettre à jour README"
git commit -m "refactor: extraire CalculatorViewModel"
git commit -m "test: ajouter tests pour la persistance"
```

---

## 📊 Intégration Continue / Déploiement Continu (CI/CD)

### Pipeline GitHub Actions

Le pipeline CI/CD (`/.github/workflows/ci-cd.yml`) effectue :

1. **Linting** (flake8, black, isort)
2. **Tests** (pytest avec couverture)
3. **Build** (Windows et Linux)
4. **Release** (pour les tags)

### Déclencheurs

| Événement | Actions exécutées |
|-----------|-------------------|
| Push sur `main` | Lint + Tests |
| Push sur `release/*` | Lint + Tests + Build |
| Tag `v*` | Lint + Tests + Build + Release |
| Pull Request | Lint + Tests |

### Badges

Ajouter ces badges à votre README :

```markdown
[![CI/CD Pipeline](https://github.com/alnews2/EvaluationDeMistralCODE2/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/alnews2/EvaluationDeMistralCODE2/actions)
[![Coverage Status](https://coveralls.io/repos/github/alnews2/EvaluationDeMistralCODE2/badge.svg)](https://coveralls.io/github/alnews2/EvaluationDeMistralCODE2)
```

---

## 🐛 Débogage

### Débogage Python

```bash
# Exécuter avec pdb
python -m pdb -m src.main

# Ou utiliser des breakpoints dans le code
import pdb; pdb.set_trace()
```

### Débogage Qt

```bash
# Activer le logging Qt
export QT_DEBUG_PLUGINS=1

# Exécuter avec logging
poetry run python -m src.main
```

### Journalisation

L'application utilise le logging Python :

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.debug("Message de débogage")
```

---

## 📚 Documentation

### Générer la documentation

La documentation est écrite en Markdown et peut être visualisée directement sur GitHub.

Pour une documentation plus avancée, vous pouvez utiliser MkDocs :

1. Installer MkDocs
   ```bash
   poetry add mkdocs mkdocs-material
   ```

2. Créer un fichier `mkdocs.yml`
   ```yaml
   site_name: CalculatorApp
   theme:
     name: material
   nav:
     - Accueil: README.md
     - Architecture: docs/ARCHITECTURE.md
     - Développement: docs/DEVELOPMENT.md
     - Guide Utilisateur: docs/USER_GUIDE.md
   ```

3. Générer et servir la documentation
   ```bash
   poetry run mkdocs serve
   ```

---

## 🤝 Code Review

### Checklist avant de soumettre une PR

- [ ] Le code suit les conventions de style
- [ ] Tous les tests passent
- [ ] La couverture de code est maintenue ou améliorée
- [ ] La documentation est mise à jour
- [ ] Les messages de commit sont clairs et descriptifs
- [ ] La PR a une description complète
- [ ] Les screenshots sont fournis pour les changements UI

### Critères de qualité

1. **Code propre**
   - Pas de code dupliqué
   - Fonctions courtes et ciblées
   - Noms descriptifs

2. **Tests complets**
   - Tests unitaires pour la logique
   - Tests d'intégration pour les interactions
   - Tests UI pour l'interface

3. **Documentation**
   - Docstrings pour toutes les classes et méthodes publiques
   - Mises à jour des fichiers de documentation
   - Commentaires pour le code complexe

4. **Performance**
   - Pas de fuites mémoire
   - Temps de réponse acceptable
   - Optimisation des opérations coûteuses

---

## 🔒 Sécurité

### Bonnes pratiques de sécurité

1. **Ne jamais commiter de secrets**
   - Clés API
   - Mots de passe
   - Tokens d'accès

2. **Utiliser .gitignore**
   - Fichiers temporaires
   - Fichiers de configuration locaux
   - Environnements virtuels

3. **Vérifier les dépendances**
   ```bash
   # Vérifier les vulnérabilités
   poetry audit
   ```

### Gestion des secrets

Utiliser les variables d'environnement ou les secrets GitHub :

```bash
# Dans le code
import os
api_key = os.environ.get("API_KEY")

# Dans GitHub Actions
# Utiliser ${{ secrets.MON_SECRET }}
```

---

## 📞 Support et Communication

### Ouvrir une Issue

1. Vérifier que l'issue n'existe pas déjà
2. Fournir une description claire
3. Inclure les étapes pour reproduire le problème
4. Ajouter des logs ou screenshots si pertinent

### Types d'Issues

| Type | Label | Description |
|------|-------|-------------|
| Bug | `bug` | Problème ou comportement inattendu |
| Fonctionnalité | `enhancement` | Nouvelle fonctionnalité |
| Documentation | `documentation` | Amélioration de la docs |
| Question | `question` | Question sur l'utilisation |

### Template d'Issue

```markdown
## Description

[Description claire du problème ou de la demande]

## Étapes pour reproduire (pour les bugs)

1. Aller à...
2. Cliquer sur...
3. Observer que...

## Comportement attendu

[Ce qui devrait se passer]

## Comportement actuel

[Ce qui se passe réellement]

## Informations supplémentaires

- Version de Python :
- Système d'exploitation :
- Screenshots :
```

---

## 🎯 Roadmap

### Version 1.0 (Actuelle)
- ✅ Calculatrice 4 opérations
- ✅ Architecture MVVM
- ✅ Double persistance (JSON + SQLite)
- ✅ Tests automatiques
- ✅ CI/CD avec GitHub Actions
- ✅ Documentation complète

### Version 1.1 (Future)
- [ ] Opérations avancées (puissance, racine, etc.)
- [ ] Mémoire (M+, M-, MR, MC)
- [ ] Mode scientifique
- [ ] Thèmes personnalisables
- [ ] Internationalisation (i18n)

### Version 2.0 (Long terme)
- [ ] Interface graphique améliorée
- [ ] Historique avancé avec recherche
- [ ] Synchronisation cloud
- [ ] Application mobile (via Qt for Mobile)

---

## 📄 License

Ce projet est sous license **MIT**. Voir le fichier [LICENSE](../LICENSE) pour plus de détails.

---

## 🙏 Remerciements

Merci à tous les contributeurs et à la communauté open source !

---

## 📚 Ressources Utiles

- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Qt Documentation](https://doc.qt.io/)
- [Python Documentation](https://docs.python.org/3/)
- [pytest Documentation](https://docs.pytest.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
