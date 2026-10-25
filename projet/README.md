# Casser un code affine

Enes Avsar — travail individuel

## Le projet

J'ai choisi le chiffrement affine car il utilise le PGCD et le modulo vus en TP. Chaque lettre est remplacée par un nombre de 0 à 25, puis le programme calcule :

`y = (a * x + b) modulo 26`

Pour pouvoir déchiffrer le message, `a` doit être premier avec 26. Il y a 12 valeurs possibles pour `a` et 26 pour `b), donc 312 clés.

J'ai comparé deux méthodes. La force brute essaie les 312 clés et classe les résultats avec un score du khi-deux. L'attaque par fréquences part de l'idée que la lettre chiffrée la plus fréquente correspond à E. J'ai testé cette idée avec `k = 1, 2, 3, 5`, c'est-à-dire en prenant les 1, 2, 3 ou 5 lettres les plus fréquentes.

Le TP5 contient déjà les fonctions pour le PGCD, l'inverse modulaire, les clés valides et une première attaque par fréquences. Je les réutilise. Pour les expériences, je compte les lettres une seule fois puis je réutilise ces comptes pour calculer les scores plus vite. Le projet ajoute surtout la comparaison des attaques et les tests sur plusieurs longueurs.

## Lancer le programme

Depuis le dossier principal du dépôt, il faut installer Matplotlib, lancer les tests puis exécuter le projet :

```bash
python -m pip install -r requirements.txt
python -m unittest projet.test_projet -v
python -m tp.test_solutions
python -m projet.main
```

Le programme fait 300 essais pour chacune des longueurs 20, 30, 50, 80, 150 et 280 lettres, soit 1 800 essais. Il choisit une fenêtre au hasard dans cinq textes en français (programmation, ville, nature, lecture et voyage) et tire une clé au hasard. La graine `20261025` permet de refaire la même série. Les fenêtres peuvent se chevaucher : ces textes ne représentent donc pas tout le français.

Les mesures sont enregistrées dans `projet/resultats/experiences.csv`. Le programme génère aussi trois graphiques en PNG et SVG : le taux de classement en première position, la présence de la vraie clé parmi les candidats et le nombre moyen de clés examinées.

### Graphiques

![Taux de réussite](resultats/taux_reussite.svg)

![Présence de la clé dans les candidats](resultats/presence_cle.svg)

Les graphiques sont générés avec Matplotlib dans `projet/graphique.py`. Le programme lit les résultats des expériences, trace les courbes et les barres, puis enregistre les fichiers. Le SVG est vectoriel et reste net quand on zoome ; le PNG est composé de pixels.

## Résultats

Les tableaux viennent de la série de 1 800 essais avec la graine indiquée plus haut. Je distingue deux choses : est-ce que la bonne clé figure dans la liste, et est-ce que le score du khi-deux la classe première.

### La bonne clé est classée première

| Lettres du message | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 91,3 % | 61,0 % | 72,3 % | 77,0 % | 83,0 % |
| 30  | 98,7 % | 74,0 % | 87,0 % | 91,3 % | 96,3 % |
| 50  | 100,0 % | 94,0 % | 97,0 % | 99,0 % | 100,0 % |
| 80  | 100,0 % | 98,3 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### La bonne clé est présente dans les candidats

| Lettres du message | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 100,0 % | 63,7 % | 77,7 % | 82,7 % | 90,3 % |
| 30  | 100,0 % | 74,7 % | 87,7 % | 92,3 % | 97,3 % |
| 50  | 100,0 % | 94,0 % | 97,0 % | 99,0 % | 100,0 % |
| 80  | 100,0 % | 98,3 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### Nombre de clés examinées en moyenne

| Méthode | Nombre de clés |
|---|---:|
| Force brute | 312 |
| Fréquences k = 1 | 12 |
| Fréquences k = 2 | 24 |
| Fréquences k = 3 | 36 |
| Fréquences k = 5 | 60 |

Sur les 1 800 essais, la force brute a toujours inclus la bonne clé. Par contre, le score du khi-deux l'a classée première dans 1 770 cas, soit 98,3 %. Donc tester toutes les clés permet bien de mettre la vraie clé dans la liste, mais le classement statistique peut parfois se tromper.

J'ai aussi remarqué que, pour `k=1`, les taux de présence et de classement sont identiques à partir de 50 lettres dans cette série. Quand la méthode trouve la bonne clé, le khi-deux la place donc aussi première dans ces essais. Ça ne garantit pas le même résultat avec d'autres textes.

Chaque taux par longueur est calculé sur 300 essais. Autour de 50 % de réussite, la marge d'incertitude à 95 % est d'environ 5,6 points. Même avec 300 succès sur 300, le résultat ne prouve pas que la méthode marchera à tous les coups : les textes utilisés sont peu nombreux et les fenêtres peuvent se chevaucher.

## Exemple d'échec de k = 1

J'ai utilisé la phrase : « Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. »

Après avoir retiré les accents et les espaces, S apparaît 16 fois et E 15 fois. S est donc plus fréquente qu'E d'une occurrence. Avec `k=1`, le programme suppose que la lettre chiffrée la plus fréquente correspond à E. Ici, cette hypothèse est fausse et la bonne clé n'est pas dans les candidats.

Avec `k=3`, le programme essaie trois lettres chiffrées comme correspondantes possibles de E. Dans cet exemple, il retrouve la bonne clé et le score la classe première. C'est un exemple choisi pour montrer pourquoi `k=1` peut échouer, pas une preuve sur tous les textes français.

## Limites

J'ai utilisé cinq textes assez courts, donc les résultats ne représentent pas tous les textes français. Les fréquences sont prévues pour le français et le programme ne regarde que les lettres : il ne tient pas compte de l'ordre des lettres ni des mots. Les espaces restent visibles dans le message chiffré, ce qui donne déjà un indice sur la longueur des mots. Je n'ai pas comparé les temps de calcul, car les différences sont trop petites pour être vraiment utiles ici.

Le chiffrement affine reste facile à casser ; il ne faut pas l'utiliser pour protéger de vraies données.

J'ai utilisé ChatGPT pour m'aider sur une partie du code et des tests. Les tests vérifient le chiffrement et le déchiffrement, le refus des clés invalides et un exemple où l'attaque `k=1` se trompe. Au début, les expériences utilisaient des extraits du même texte. Les résultats dépendaient donc trop de ce texte, alors le programme a été changé pour faire les essais sur cinq textes différents et comparer séparément la présence de la clé et son classement.
