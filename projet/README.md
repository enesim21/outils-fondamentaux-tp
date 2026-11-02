# Casser un chiffrement affine

Enes Avsar, groupe A1, travail individuel.

Le chiffrement affine code chaque lettre avec `y = (a*x + b) mod 26`. Comme `a` doit être premier avec 26, il y a 312 clés possibles.

Je compare trois attaques :
- la force brute : on teste les 312 clés et on garde le texte dont les fréquences de lettres ressemblent le plus au français (score du khi-deux) ;
- l'attaque par fréquences : on suppose qu'une des `k` lettres les plus fréquentes du message est un E, ce qui ne laisse que 12 clés par lettre testée ;
- l'attaque à clair connu : on connaît quelques lettres du message en clair, et on résout un système d'équations modulo 26.

Ma question : à partir de combien de lettres on retrouve la clé, et quelle attaque est la plus fiable ?

Je réutilise les fonctions du TP5 (PGCD, inverse modulaire, nettoyage du texte).

## Lancer

```bash
python -m unittest projet.test_projet -v
python -m projet.main
```

`projet.main` fait 300 essais par longueur (20 à 280 lettres) sur des morceaux de cinq paragraphes, avec des clés tirées au hasard (graine 20261025), puis l'expérience à clair connu. Les résultats sont dans `resultats/`.

## Force brute et fréquences

![Taux de réussite](resultats/taux_reussite.svg)

Pourcentage d'essais où la bonne clé est classée première :

| Lettres | Force brute | k = 1 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|
| 20 | 91,3 % | 61,0 % | 77,0 % | 83,0 % |
| 30 | 98,7 % | 74,0 % | 91,3 % | 96,3 % |
| 50 | 100 % | 94,0 % | 99,0 % | 100 % |
| 80 | 100 % | 98,3 % | 99,3 % | 100 % |
| 150 et 280 | 100 % | 100 % | 100 % | 100 % |

Ce que j'en retiens :
- La force brute a toujours la bonne clé dans sa liste, mais le khi-deux la classe mal 30 fois sur 1 800, toujours sur des messages courts.
- Avec k = 1, quand ça rate, c'est presque toujours parce que E n'était pas la lettre la plus fréquente. À partir de 50 lettres, si la clé est parmi les 12 candidats, elle est toujours classée première.
- k = 3 est un bon compromis : 36 clés testées au lieu de 312, et 99 % de réussite dès 50 lettres.
- Le texte compte : sur les messages de 20 et 30 lettres, k = 1 réussit 59 % du temps sur le paragraphe « apprentissage » et 73 % sur « nature ».

Exemple d'échec : la phrase « Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. » a 16 S pour 15 E, donc k = 1 se trompe. k = 3 trouve la bonne clé (c'est vérifié dans les tests).

## Attaque à clair connu

Si on connaît deux lettres en clair (x1, x2) et leur version chiffrée (y1, y2), on a le système :

```
a*x1 + b = y1  (mod 26)
a*x2 + b = y2  (mod 26)
```

C'est un système 2×2 comme au TP4, de déterminant `x1 - x2`. En le soustrayant, on obtient `a*(x1 - x2) = y1 - y2`. D'après le TP4, il faudrait que le déterminant soit inversible, donc premier avec 26, ce qui n'arrive que dans environ la moitié des cas.

En testant, j'ai trouvé beaucoup mieux. Comme `a` doit être impair, la clé reste unique même quand le déterminant est pair. Sur les 650 couples de lettres différentes, seuls les 26 couples écartés de 13 (AN, ER, ...) laissent plusieurs clés : dans ce cas, les 12 valeurs de `a` marchent toutes.

| Lettres connues | Clé unique | Déterminant inversible | Clés possibles en moyenne |
|---:|---:|---:|---:|
| 1 | 0 % | — | 12 |
| 2 | 87,9 % | 49,3 % | 2,33 |
| 3 | 98,4 % | — | 1,18 |
| 4 et plus | 100 % | — | 1 |

Avec deux lettres connues, les 121 échecs sur 1 000 viennent de deux lettres identiques (50 cas, comme « SS ») ou de deux lettres écartées de 13 (71 cas, souvent E et R). Il suffit donc de connaître quatre lettres du message, contre une vingtaine de lettres chiffrées pour les attaques statistiques.

## Limites

Je n'ai utilisé que cinq paragraphes, donc les 100 % sur les longs messages valent surtout pour ces textes. Avec 300 essais, les taux ont une marge d'environ ±5 points. Le khi-deux ne regarde pas l'ordre des lettres, et j'ai laissé les espaces dans le message chiffré, ce qui donne la longueur des mots. L'attaque à clair connu suppose qu'on sait où se trouvent les lettres connues dans le message.

## Aide utilisée

Je me suis aidé d'un assistant IA pour structurer le code et les tests. Ma première version des expériences réutilisait toujours le même début de texte, je l'ai refaite avec des extraits tirés au hasard. J'ai lancé moi-même les tests et les expériences.
