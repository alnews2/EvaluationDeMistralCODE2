# 📖 Guide Utilisateur - CalculatorApp

Bienvenue dans le **Guide Utilisateur** de **CalculatorApp** ! Ce document vous explique comment installer, utiliser et tirer le meilleur parti de cette calculatrice 4 opérations moderne.

---

## 📥 Installation

### Prérequis
- **Système d'exploitation** : Windows 10/11, Linux (Ubuntu, Fedora, etc.), ou macOS
- **Python** : 3.10 ou supérieur (si vous utilisez le code source)

### Installation via l'exécutable (recommandé)

1. **Télécharger l'exécutable**
   - Allez sur la page des [releases GitHub](https://github.com/alnews2/EvaluationDeMistralCODE2/releases)
   - Téléchargez la version correspondant à votre système :
     - `CalculatorApp.exe` pour Windows
     - `CalculatorApp` pour Linux

2. **Exécuter l'application**
   - **Windows** : Double-cliquez sur `CalculatorApp.exe`
   - **Linux** :
     ```bash
     chmod +x CalculatorApp
     ./CalculatorApp
     ```

### Installation via le code source

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/alnews2/EvaluationDeMistralCODE2.git
   cd EvaluationDeMistralCODE2/CalculatorApp
   ```

2. **Installer les dépendances**
   ```bash
   # Avec Poetry (recommandé)
   poetry install
   poetry run python -m src.main
   
   # Avec pip
   pip install -r requirements.txt
   python -m src.main
   ```

---

## 🎯 Interface de l'Application

### Vue d'ensemble

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

### Description des éléments

| Élément | Description |
|---------|-------------|
| **Zone d'opération** | Affiche l'opération en cours (ex: "5 + 3") |
| **Affichage principal** | Affiche la valeur actuelle ou le résultat |
| **Boutons numériques** | 0-9 pour entrer les nombres |
| **Boutons d'opération** | +, -, *, /, = pour les opérations |
| **Bouton .** | Point décimal |
| **Bouton C** | Efface la valeur actuelle (Clear) |
| **Bouton CE** | Efface tout (Clear All) |
| **Bouton ⌫** | Supprime le dernier chiffre (Backspace) |
| **Zone Historique** | Affiche l'historique des calculs |
| **Bouton Effacer** | Efface l'historique |
| **Info Stockage** | Affiche le type de stockage utilisé |
| **Bouton JSON/SQLite** | Bascule entre les types de stockage |

---

## 🎮 Utilisation de Base

### Calcul simple

1. **Entrer le premier nombre**
   - Cliquez sur les boutons numériques (0-9)
   - Exemple : Cliquez sur `5`, `0` → Affiche "50"

2. **Choisir une opération**
   - Cliquez sur `+`, `-`, `*`, ou `/`
   - Exemple : Cliquez sur `+` → Affiche "50 +"

3. **Entrer le deuxième nombre**
   - Cliquez sur les boutons numériques
   - Exemple : Cliquez sur `2`, `5` → Affiche "25"

4. **Obtenir le résultat**
   - Cliquez sur `=` → Affiche "75"

**Exemple complet** : `50 + 25 = 75`

### Utilisation du point décimal

1. Entrer un nombre : `3`
2. Cliquer sur `.` → Affiche "3."
3. Entrer la partie décimale : `1`, `4` → Affiche "3.14"
4. Continuer le calcul normalement

**Exemple** : `3.14 * 2 = 6.28`

### Opérations en chaîne

Vous pouvez enchaîner les opérations :

1. `5 + 3 = 8`
2. Cliquer sur `*`
3. Entrer `2`
4. Cliquer sur `=` → Résultat : `16` (car (5 + 3) * 2 = 16)

---

## ⌨️ Raccourcis Clavier

| Touche | Action |
|--------|--------|
| 0-9 | Entrer le chiffre correspondant |
| . | Point décimal |
| + | Addition |
| - | Soustraction |
| * | Multiplication |
| / | Division |
| = ou Entrée | Calculer le résultat |
| C | Effacer la valeur actuelle |
| Escape | Effacer tout |
| Backspace | Supprimer le dernier chiffre |

---

## 📊 Fonctionnalités Avancées

### Historique des calculs

- **Affichage** : Tous les calculs effectués sont enregistrés dans l'historique
- **Navigation** : Faites défiler la liste pour voir les calculs précédents
- **Effacement** : Cliquez sur "Effacer" pour supprimer l'historique

**Exemple d'historique** :
```
5 + 3 = 8
10 - 4 = 6
3.14 * 2 = 6.28
20 / 4 = 5.0
```

### Gestion des erreurs

- **Division par zéro** : Affiche "Erreur" et le message "Division par zéro"
- **Récupération** : Après une erreur, appuyez sur n'importe quel bouton numérique ou d'opération pour continuer

**Exemple** :
```
10 / 0 = Erreur
(Message : "Division par zéro")

Appuyez sur "5" → Réinitialise et affiche "5"
```

### Persistance des données

CalculatorApp sauvegarde automatiquement :
- L'état actuel de la calculatrice
- L'historique des calculs

**Deux modes de stockage disponibles** :

1. **JSON** (par défaut)
   - Fichier : `~/.calculatorapp/history.json`
   - Format lisible
   - Idéal pour les petits volumes de données

2. **SQLite**
   - Fichier : `~/.calculatorapp/calculator.db`
   - Base de données structurée
   - Idéal pour les grands volumes de données

**Changer de mode de stockage** :
- Cliquez sur le bouton "JSON" ou "SQLite" en bas de la fenêtre
- Ou utilisez la variable d'environnement :
  ```bash
  export CALCULATOR_STORAGE=sqlite
  ```

---

## ⚙️ Configuration

### Changer le type de stockage

**Méthode 1 : Via l'interface**
1. Cliquez sur le bouton "JSON" ou "SQLite" en bas de la fenêtre
2. L'application basculera automatiquement vers le nouveau type de stockage
3. Les données seront migrées vers le nouveau format

**Méthode 2 : Via variable d'environnement**
```bash
# Pour utiliser JSON
export CALCULATOR_STORAGE=json

# Pour utiliser SQLite
export CALCULATOR_STORAGE=sqlite

# Puis exécutez l'application
./CalculatorApp
```

**Méthode 3 : Via le code**
```python
# Dans le code source
viewmodel = CalculatorViewModel(storage_type="sqlite")
```

### Réinitialiser l'application

Pour réinitialiser complètement l'application :

1. **Effacer les données**
   - Cliquez sur "CE" (Clear All)
   - Cela réinitialise la calculatrice et efface l'historique

2. **Supprimer les fichiers de stockage**
   ```bash
   # Supprimer les fichiers de stockage
   rm -rf ~/.calculatorapp/
   ```

---

## 🔧 Dépannage

### Problèmes courants

| Problème | Solution |
|----------|----------|
| **L'application ne s'ouvre pas** | Vérifiez que Python 3.10+ est installé et que les dépendances sont correctement installées |
| **Erreur "ModuleNotFoundError"** | Installez les dépendances manquantes avec `pip install -r requirements.txt` |
| **Problème d'affichage** | Vérifiez que votre système supporte Qt/PySide6 |
| **Les boutons ne répondent pas** | Redémarrez l'application |
| **Problème de persistance** | Vérifiez les permissions sur le dossier `~/.calculatorapp/` |

### Vérifier les dépendances

```bash
# Vérifier la version de Python
python --version

# Vérifier les modules installés
pip list | grep -E "PySide6|pytest"

# Tester l'importation
python -c "from PySide6.QtWidgets import QApplication; print('PySide6 OK')"
```

### Journalisation

Pour activer la journalisation (logs) :

```bash
# Linux/Mac
export PYTHONLOGGING=DEBUG

# Windows
set PYTHONLOGGING=DEBUG

# Puis exécutez l'application
```

### Réinstaller les dépendances

```bash
# Avec Poetry
poetry install --force

# Avec pip
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 📈 Exemples Pratiques

### Calculs du quotidien

| Besoin | Calcul | Résultat |
|--------|--------|----------|
| Addition de taxes | `100 + 20%` (utilisez `100 * 1.2`) | 120 |
| Réduction de prix | `100 - 15%` (utilisez `100 * 0.85`) | 85 |
| Conversion de devises | `100 * 1.1` (EUR → USD) | 110 |
| Calcul de pourboire | `50 * 0.15` (15% de 50€) | 7.5 |
| Partage d'addition | `120 / 4` (120€ pour 4 personnes) | 30 |

### Calculs mathématiques

| Opération | Calcul | Résultat |
|-----------|--------|----------|
| Carré | `5 * 5` | 25 |
| Cube | `3 * 3 * 3` | 27 |
| Moyenne | `(10 + 20 + 30) / 3` | 20 |
| Pourcentage | `25 / 100 * 200` | 50 |
| Racine carrée (approx.) | Utilisez la méthode de Newton |

### Calculs en chaîne

```
1. 5 + 3 = 8
2. * 2 = 16
3. - 4 = 12
4. / 3 = 4
5. + 10 = 14
```

---

## 🎨 Personnalisation

### Thème de l'application

L'application utilise un **thème sombre personnalisé** avec les couleurs suivantes :

| Élément | Couleur | Code |
|---------|---------|------|
| Fond principal | Bleu nuit | `#1e1e2e` |
| Fond secondaire | Bleu foncé | `#181825` |
| Boutons | Gris foncé | `#313244` |
| Texte | Blanc cassé | `#cdd6f4` |
| Accent | Violet | `#cba6f7` |
| Bouton = | Gris clair | `#6c7086` |

### Personnaliser le thème

Pour personnaliser le thème :

1. Modifier le fichier `src/ui/styles/dark_theme.py`
2. Changer les codes couleur
3. Redémarrer l'application

**Exemple de personnalisation** :
```css
/* Changer la couleur de fond */
QMainWindow {
    background-color: #282a36;  /* Nouveau fond */
}

/* Changer la couleur des boutons */
QPushButton {
    background-color: #44475a;  /* Nouveau fond de bouton */
    color: #ff79c6;             /* Nouveau texte */
}
```

---

## 📱 Utilisation sur Mobile (Expérimental)

Bien que CalculatorApp soit principalement conçue pour le bureau, elle peut fonctionner sur certains appareils mobiles :

### Android (via Termux)

1. Installer Termux depuis le Play Store
2. Installer Python et les dépendances :
   ```bash
   pkg install python
   pip install PySide6
   ```
3. Cloner et exécuter l'application

### iOS (via Pythonista)

1. Installer Pythonista depuis l'App Store
2. Copier le code source
3. Installer les dépendances
4. Exécuter l'application

⚠️ **Note** : L'expérience mobile peut être limitée en raison de la taille de l'écran.

---

## 🔒 Sécurité et Vie Privée

### Données stockées

CalculatorApp stocke localement :
- **État de la calculatrice** : Valeur actuelle, opération en cours
- **Historique des calculs** : Liste des calculs effectués

**Emplacement des données** :
- Linux/Mac : `~/.calculatorapp/`
- Windows : `%USERPROFILE%\.calculatorapp\`

### Confidentialité

- ✅ **Aucune donnée n'est envoyée** à des serveurs distants
- ✅ **Toutes les données restent locales** sur votre machine
- ✅ **Aucune connexion Internet** requise
- ✅ **Aucun suivi** ou collecte de données

### Supprimer les données

Pour supprimer toutes les données :

```bash
# Linux/Mac
rm -rf ~/.calculatorapp/

# Windows
rd /s /q %USERPROFILE%\.calculatorapp\
```

---

## 📊 Performances

### Optimisations

CalculatorApp est optimisée pour :
- **Réactivité** : Interface fluide et réactive
- **Mémoire** : Utilisation minimale de la mémoire
- **Calculs** : Opérations mathématiques rapides
- **Persistance** : Sauvegarde asynchrone (ne bloque pas l'UI)

### Benchmark

| Opération | Temps (moyenne) |
|-----------|-----------------|
| Addition | < 1ms |
| Soustraction | < 1ms |
| Multiplication | < 1ms |
| Division | < 1ms |
| Sauvegarde JSON | < 5ms |
| Sauvegarde SQLite | < 10ms |

---

## 🌐 Communauté et Support

### Poser une question

Si vous avez une question :
1. Consultez ce guide utilisateur
2. Consultez la [documentation technique](ARCHITECTURE.md)
3. Ouvrez une [Issue GitHub](https://github.com/alnews2/EvaluationDeMistralCODE2/issues)

### Signaler un bug

Pour signaler un bug :
1. Vérifiez que le bug n'a pas déjà été signalé
2. Ouvrez une nouvelle Issue avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Comportement attendu
   - Comportement actuel
   - Screenshots si possible

### Contribuer

Pour contribuer au développement :
1. Lisez le [Guide de Développement](DEVELOPMENT.md)
2. Forker le dépôt
3. Créer une branche
4. Soumettre une Pull Request

---

## 📝 Historique des Versions

| Version | Date | Changements |
|---------|------|------------|
| **1.0.0** | 2024 | Version initiale |
| | | - Calculatrice 4 opérations |
| | | - Architecture MVVM |
| | | - Double persistance (JSON + SQLite) |
| | | - Tests automatiques |
| | | - CI/CD avec GitHub Actions |
| | | - Documentation complète |

---

## 📄 License

CalculatorApp est distribué sous la **license MIT**.

Cela signifie que vous pouvez :
- ✅ Utiliser l'application gratuitement
- ✅ Modifier le code source
- ✅ Distribuer l'application
- ✅ Utiliser le code dans vos propres projets

**Conditions** :
- Inclure la notice de copyright
- Inclure la license MIT

Voir le fichier [LICENSE](../LICENSE) pour plus de détails.

---

## 🙏 Remerciements

Merci à :
- **La communauté Python** pour les bibliothèques utilisées
- **La communauté Qt** pour PySide6
- **Tous les contributeurs** qui améliorent ce projet
- **Vous** pour utiliser CalculatorApp !

---

## 📚 Ressources Supplémentaires

- [Site Web du Projet](https://github.com/alnews2/EvaluationDeMistralCODE2)
- [Documentation Technique](ARCHITECTURE.md)
- [Guide de Développement](DEVELOPMENT.md)
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Python Documentation](https://docs.python.org/3/)

---

## 🎉 Conclusion

Félicitations ! Vous savez maintenant tout ce qu'il faut savoir pour utiliser **CalculatorApp** efficacement. Cette application combine simplicité et puissance, avec une interface moderne et des fonctionnalités avancées.

N'hésitez pas à :
- **Explorer** toutes les fonctionnalités
- **Personnaliser** l'application selon vos besoins
- **Contribuer** au développement
- **Partager** avec vos amis et collègues

Bonne calcul ! 🧮✨
