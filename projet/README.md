# Solveur d'equations

Nom : à compléter  
Groupe : à compléter

Le programme compare la dichotomie, Newton et une methode hybride, avec `brentq` de SciPy comme reference. Les tests portent sur quatre fonctions, dont un cas ou Newton cycle et une racine double sans changement de signe.

## Lancer

Depuis la racine du depot :

```bash
python -m pip install -r requirements.txt
python -m projet.main
python -m unittest projet.test_methodes -v
```

Le programme produit un tableau dans le terminal, un fichier CSV et deux graphiques dans `projet/resultats/`. Le graphique des iterations est aussi disponible ici : [voir le graphique](resultats/iterations.svg).

## Premiers resultats

Avec une tolerance de `1e-10` :

| Fonction | Dichotomie | Newton | Hybride | Brent (SciPy) |
|---|---:|---:|---:|---:|
| x² - 2 | 29 it. | 3 it. | 3 it. | 7 it. |
| cos(x) - x | 30 it. | 4 it. | 4 it. | 7 it. |
| x³ - 2x + 2 | 34 it. | cycle | 23 it. | 9 it. |
| (x - 1)² | echec | 16 it. | echec | echec |

Sur les trois intervalles avec changement de signe, Newton est rapide pour les deux premiers cas. Sur x³ - 2x + 2, il revient a son point de depart et le cycle est detecte. L'hybride trouve une racine, mais prend plus d'iterations que Brent sur cet exemple. La racine double est un contre-exemple utile : les methodes basees sur un changement de signe ne peuvent pas l'encadrer avec l'intervalle choisi.

Les appels de fonction et l'erreur finale sont aussi sauvegardes dans le CSV. Le nombre d'iterations ne suffit pas a lui seul pour comparer toutes les methodes : Newton demande aussi des evaluations de derivee et les points de depart ne sont pas identiques.

## Limites

La methode hybride utilise un intervalle qui doit deja encadrer une racine. Elle ne trouve donc pas toutes les racines possibles. Les quatre fonctions choisies donnent des exemples utiles, mais elles ne suffisent pas a prouver que l'hybride est toujours meilleur. Les resultats dependent de la fonction, du point de depart, de l'intervalle et de la tolerance.

Utilisation de l'IA : une aide a servi a ecrire et organiser une partie du code et des tests. Les tests et les resultats numeriques doivent etre verifies et interpretes avant le rendu.
