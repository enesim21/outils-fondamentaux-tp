# Casser un code affine

**Enes Avsar — travail individuel**

## Le but du projet

J'ai choisi le chiffrement affine parce qu'il utilise le PGCD et le modulo vus en TP. Chaque lettre est remplacée par un nombre entre 0 et 25. Pour chiffrer une lettre, le programme calcule :

`y = (a * x + b) modulo 26`

Pour que le message puisse être déchiffré, `a` doit être premier avec 26. Il y a 12 valeurs possibles pour `a` et 26 pour `b), donc **312 clés** au total.

J'ai comparé deux façons de retrouver la clé :
- **Force brute** : le programme essaie toutes les clés puis classe les textes avec un score du khi-deux.
- **Fréquences** : il suppose que l'une des lettres chiffrées les plus fréquentes correspond à E. Je teste cette idée avec `k = 1, 2, 3, 5`.

Le score du khi-deux compare les fréquences des lettres d'un texte avec celles qu'on trouve habituellement en français. Un petit score est considéré comme meilleur, mais ça ne garantit pas que le texte proposé soit le bon.

## Ce que j'ai repris du TP5

Le TP5 contient déjà le PGCD, l'inverse modulaire, les clés valides et une première attaque par fréquences. Je réutilise ces fonctions au lieu de tout réécrire.

Pour les expériences, je ne me sers pas directement de `toutes_les_cles`, car elle reconstruit le texte pour chaque clé. Ici, je compte d'abord les lettres, puis je réutilise ces comptes pour calculer plus vite le score. J'ai aussi ajouté plusieurs valeurs de `k` et la comparaison des résultats sur des textes de longueurs différentes.

## Lancer le projet

Depuis le dossier principal du dépôt, je lance :

```bash
python -m pip install -r requirements.txt
python -m unittest projet.test_projet -v
python -m tp.test_solutions
python -m projet.main
```

Le programme fait 300 essais pour chacune de ces longueurs : **20, 30, 50, 80, 150 et 280 lettres**, soit 1 800 essais. Il choisit une fenêtre de texte au hasard et une clé au hasard. J'utilise cinq textes en français sur différents sujets (programmation, ville, nature, lecture et voyage). La graine `20261025` permet de retrouver la même série d'essais. Certaines fenêtres peuvent se chevaucher, donc ce n'est pas un échantillon de tout le français.

Les résultats détaillés sont enregistrés dans `projet/resultats/experiences.csv`. Le programme produit aussi trois graphiques, chacun en PNG et en SVG :
- `taux_reussite` : à quelle fréquence la bonne clé arrive en première position ;
- `presence_cle` : à quelle fréquence la bonne clé est dans la liste ;
- `nombre_cles` : combien de clés sont examinées en moyenne.

## Graphiques

![Taux de réussite](resultats/taux_reussite.svg)

![Présence de la clé dans les candidats](resultats/presence_cle.svg)

Les graphiques sont produits par `projet/graphique.py` avec Matplotlib. Le programme lit les résultats des expériences, dessine les courbes et les barres, puis sauvegarde les fichiers. Le SVG est un format vectoriel : il reste net quand on zoome, contrairement au PNG qui est fait de pixels.

## Résultats

Les tableaux ci-dessous viennent de la série de 1 800 essais avec la graine indiquée plus haut. Je sépare deux questions : est-ce que la bonne clé est dans les candidats, et est-ce que le score du khi-deux la met en première position ?

### La bonne clé est classée première

| Nombre de lettres | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 91,3 % | 61,0 % | 72,3 % | 77,0 % | 83,0 % |
| 30  | 98,7 % | 74,0 % | 87,0 % | 91,3 % | 96,3 % |
| 50  | 100,0 % | 94,0 % | 97,0 % | 99,0 % | 100,0 % |
| 80  | 100,0 % | 98,3 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### La bonne clé est dans les candidats

| Nombre de lettres | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 100,0 % | 63,7 % | 77,7 % | 82,7 % | 90,3 % |
| 30  | 100,0 % | 74,7 % | 87,7 % | 92,3 % | 97,3 % |
| 50  | 100,0 % | 94,0 % | 97,0 % | 99,0 % | 100,0 % |
| 80  | 100,0 % | 98,3 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### Nombre moyen de clés examinées

| Méthode | Nombre de clés |
|---|---:|
| Force brute | 312 |
| Fréquences k = 1 | 12 |
| Fréquences k = 2 | 24 |
| Fréquences k = 3 | 36 |
| Fréquences k = 5 | 60 |

Sur les 1 800 essais, la force brute a toujours inclus la bonne clé. Par contre, le khi-deux l'a mise en première position dans 1 770 essais, soit **98,3 %**. Cela montre que tester toutes les clés permet de retrouver la bonne parmi les propositions, mais que le classement statistique peut encore se tromper.

J'ai aussi remarqué que, dans ces essais, pour `k=1`, les taux de présence et de classement sont les mêmes à partir de 50 lettres. Ça veut dire que lorsque la bonne clé est trouvée par cette méthode, elle est également arrivée première dans cette série. Ça ne veut pas dire que ce sera toujours le cas avec d'autres textes.

Chaque taux par longueur est calculé sur 300 essais. Vers 50 %, l'incertitude liée à la taille de l'échantillon est d'environ **± 5,6 points** à 95 %. Pour 300 réussites sur 300, le taux observé est de 100 %, mais ça ne prouve pas que la méthode réussira sur tous les textes. Les paragraphes utilisés sont peu nombreux et les fenêtres se chevauchent parfois.

## Un exemple où k = 1 échoue

J'ai utilisé cette phrase comme exemple : « Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. »

Après avoir retiré les accents et les espaces, la lettre S apparaît 16 fois et E 15 fois. S est donc plus fréquente qu'E d'une occurrence. Avec `k=1`, le programme suppose que la lettre chiffrée la plus fréquente correspond à E : il fait une mauvaise hypothèse et ne propose pas la bonne clé.

Avec `k=3`, il teste les trois lettres chiffrées les plus fréquentes comme correspondantes possibles de E. Dans cet exemple, cela permet de retrouver la bonne clé et le score la classe première. C'est un exemple construit pour montrer le problème ; il ne représente pas tous les textes français.

## Limites

- J'ai utilisé cinq paragraphes français, pas un grand corpus de textes variés.
- Les fréquences utilisées sont celles du français et ne conviendraient pas directement à une autre langue.
- Le score regarde les fréquences des lettres, mais pas l'ordre des lettres ni les mots.
- Les espaces et la ponctuation sont conservés par le chiffrement. On voit donc encore la longueur des mots.
- La graine permet de refaire les mêmes essais, mais les résultats dépendent des textes et des clés tirés.
- Je ne compare pas les temps : les différences seraient trop faibles pour conclure quelque chose de solide.
- Le chiffrement affine est simple à casser ; il ne faut pas l'utiliser pour protéger de vraies données.

## Aide et vérifications

J'ai utilisé une aide IA pour mettre en place une première version des attaques, des expériences et des tests. Les tests automatisés vérifient notamment que le chiffrement peut être inversé, que les clés invalides sont refusées et que l'attaque `k=1` peut échouer quand E n'est pas la lettre la plus fréquente. Une première version utilisait seulement des extraits d'un même texte, ce qui ne permettait pas de bien comparer les longueurs. J'ai ensuite remplacé cette partie par des fenêtres prises dans cinq textes différents et j'ai séparé le fait de trouver la clé du fait de la classer première.
