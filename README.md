# Outils fondamentaux

- `tp/` : solutions des TP1 à TP6.
- `projet/` : chiffrement affine, attaques statistiques et expériences reproductibles.

Depuis la racine du dépôt :

```bash
python -m tp.test_solutions
python -m unittest projet.test_projet -v
python -m pip install -r requirements.txt
python -m projet.main
```

Le dernier lancement génère le CSV et les graphiques dans `projet/resultats/`.
