# Outils fondamentaux

- `tp/` : solutions des TP1 à TP6.
- `projet/` : comparaison de trois méthodes pour trouver les racines d'une fonction.

Lancer : `python -m projet.main`  
Installer : `python -m pip install -r requirements.txt`  
Tests : `python -m unittest projet.test_methodes -v`

On observe les itérations, l'erreur et les échecs. Newton est rapide sur certains cas, mais peut cycler ; l'hybride arrive à récupérer cet exemple. Les méthodes à intervalle ne trouvent pas la racine double si l'intervalle ne change pas de signe.

Une IA a aidé à écrire et organiser une partie du code. Les tests automatiques ont été exécutés ; l'analyse des résultats reste à compléter.
