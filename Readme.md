# Projet de Fusion et Génération de Molécules

Ce projet est un programme de simulation de fusion moléculaire, permettant de combiner des éléments de base pour générer de nouvelles molécules. Utilisant des API LLM (Large Language Model) comme Mistral pour la génération de nouvelles combinaisons d'éléments, le programme identifie et crée des molécules réalistes en fonction des éléments sélectionnés. L'objectif est de fournir une interface intuitive pour créer des molécules complexes à partir d'éléments de base.

## Fonctionnalités Actuelles

- **Affichage des éléments disponibles** : Le programme affiche la liste des éléments de base et permet de choisir les éléments à fusionner pour créer une nouvelle molécule.
- **Fusion de molécules** : En sélectionnant deux éléments dans la liste, le programme génère une nouvelle molécule si la fusion est possible, avec une validation pour éviter les doublons.
- **Stockage des molécules créées** : Les molécules générées sont enregistrées localement dans un fichier JSON pour un usage ultérieur.
- **Retour d’erreurs et de messages clairs** : En cas d’erreur ou d’impossibilité de réaction, le programme affiche des messages d’erreur explicites pour guider l’utilisateur.

## Technologies Utilisées

- **Python** : Langage principal du projet.
- **LLM (Large Language Model)** : Utilisé pour déterminer les réactions possibles et les molécules générées en fonction des éléments choisis.
- **JSON** : Format utilisé pour stocker les éléments de base et les molécules créées.

## Structure du Projet

- `src/` : Contient le code source principal
    - `display_loop.py` : Gère les interactions utilisateur et affiche les éléments disponibles.
    - `mistral_integration.py` : Interface avec le modèle LLM pour générer de nouvelles molécules.
    - `load_elements.py` : Charge les éléments de base à partir d’un fichier JSON.
- `data/` : Contient les fichiers JSON pour les éléments et les molécules créées.
- `README.md` : Documentation du projet.

## Prérequis

- Python 3.8+
- Les dépendances listées dans `requirements.txt`
- Une clé API pour l’API LLM (ex. : Mistral ou autre modèle de génération)

## Utilisation

1. Cloner le dépôt.
2. Installer les dépendances : `pip install -r requirements.txt`
3. Exécuter le programme : `python src/main.py`
4. Suivre les instructions dans le terminal pour créer et fusionner des éléments.

## Futures Implémentations

1. **Ajout d’une Interface Web (création d'API)** :
   - Développement d'une API permettant de gérer et d'automatiser les interactions utilisateur et la fusion de molécules via une interface web.

2. **Multiples Fusions de Molécules (7 max)** :
   - Ajout d'une fonctionnalité permettant de fusionner jusqu'à sept molécules ou éléments en une seule fois, augmentant ainsi la complexité des molécules générées.

3. **Intégration d’un Autre LLM avec Explication d’Éléments** :
   - Inclusion d'un autre LLM pour générer des explications détaillées sur les molécules créées. Grâce à une fonction de type `call function`, le modèle sera en mesure de fournir des informations et des propriétés des molécules nouvellement créées.