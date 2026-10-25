# Casser un code affine

**Auteur : Enes Avsar**  
**Travail individuel**

## 1. Objectif

Ce projet étudie le chiffrement affine. Chaque lettre est convertie en nombre de 0 à 25, puis chiffrée avec la formule :

`y = (a × x + b) modulo 26`

La valeur `a` doit être première avec 26 pour que le chiffrement soit réversible. Il existe 12 valeurs valides de `a` et 26 valeurs possibles de `b`, soit **312 clés**.

Le projet compare deux méthodes pour essayer de retrouver la clé :
- **Force brute** : teste les 312 clés et trie les textes déchiffrés avec le score du khi-deux.
- **Attaque par fréquences** : suppose que l'une des `k` lettres chiffrées les plus fréquentes correspond à E, pour `k = 1, 2, 3, 5`. Elle examine donc en général 12, 24, 36 ou 60 clés.

Le score du khi-deux compare les fréquences observées dans un texte déchiffré aux fréquences attendues en français. Un score plus faible signifie que les deux distributions sont plus proches ; cela ne prouve pas à lui seul que le texte est le bon.

## 2. Lien avec le TP5

Le TP5 fournit déjà le PGCD, l'inverse modulaire, les clés valides, le nettoyage des lettres et une première attaque par fréquences. Le projet réutilise ces fonctions mathématiques et le nettoyage du TP5.

Je ne réutilise pas directement `toutes_les_cles` dans les expériences de masse : elle reconstruit chaque texte candidat. Ici, je compte les lettres chiffrées une seule fois et permute ces comptes pour calculer le score de chaque clé plus efficacement. L'attaque par fréquences généralise `casser_par_frequences` en testant plusieurs valeurs de `k`. Le projet ajoute ainsi le score statistique, des variantes de l'attaque et un protocole d'expérience reproductible.

Le chiffrement conserve les espaces et la ponctuation pour rendre le message lisible. Pour calculer les fréquences, les fonctions d'attaque ne gardent que les lettres A à Z.

## 3. Lancer le projet

Depuis la racine du dépôt :

```bash
python -m pip install -r requirements.txt
python -m unittest projet.test_projet -v
python -m tp.test_solutions
python -m projet.main
```

La commande `python -m projet.main` lance **300 essais pour chacune des longueurs 20, 30, 50, 80, 150 et 280 lettres**, soit 1 800 essais. Trois paragraphes français sont utilisés. Pour chaque essai, le programme choisit une fenêtre qui contient exactement le nombre demandé de lettres, puis tire une clé valide au hasard. La graine `20261025` permet de reproduire la même série.

Le programme écrit les mesures dans `projet/resultats/experiences.csv` et génère trois graphiques en PNG et SVG :
- `taux_reussite.png` et `taux_reussite.svg` : taux où le score du khi-deux classe la vraie clé première, pour la force brute et les variantes `k=1` et `k=3).
- `presence_cle.png` et `presence_cle.svg` : taux où la vraie clé est présente dans la liste des candidats.
- `nombre_cles.png` et `nombre_cles.svg` : nombre moyen de clés examinées.

### Comment les graphiques SVG sont faits

Le fichier `projet/graphique.py` utilise **Matplotlib**. Le code crée une figure, ajoute les courbes ou les barres, les axes, le titre et la légende, puis sauvegarde le graphique deux fois :

```python
plt.savefig(dossier / "taux_reussite.png", dpi=160)
plt.savefig(dossier / "taux_reussite.svg")
```

Le PNG est une image matricielle, tandis que le SVG est un dessin vectoriel décrit par du texte (axes, lignes, textes et formes). Les deux fichiers sont produits par le programme à partir des données du CSV : le SVG n'est pas dessiné à la main et ne contient pas de résultats inventés.

## 4. Résultats observés

Les tableaux suivants proviennent d'une exécution du protocole avec la graine `20261025`, 300 essais par longueur, soit 1 800 essais au total. Les taux sont arrondis à un chiffre après la virgule. La colonne `k` précise combien de lettres chiffrées les plus fréquentes sont testées comme correspondantes à E.

### La vraie clé est-elle classée première ?

| Lettres du message | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 96,7 % | 58,7 % | 76,3 % | 82,7 % | 90,0 % |
| 30  | 98,3 % | 75,0 % | 87,3 % | 91,3 % | 96,7 % |
| 50  | 100,0 % | 89,3 % | 95,7 % | 98,0 % | 99,3 % |
| 80  | 100,0 % | 97,0 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### La vraie clé est-elle présente parmi les candidats ?

| Lettres du message | Force brute | k = 1 | k = 2 | k = 3 | k = 5 |
|---:|---:|---:|---:|---:|---:|
| 20  | 100,0 % | 60,0 % | 78,3 % | 85,7 % | 93,3 % |
| 30  | 100,0 % | 76,0 % | 89,0 % | 93,0 % | 98,3 % |
| 50  | 100,0 % | 89,3 % | 95,7 % | 98,0 % | 99,3 % |
| 80  | 100,0 % | 97,0 % | 99,0 % | 99,3 % | 100,0 % |
| 150 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |
| 280 | 100,0 % | 100,0 % | 100,0 % | 100,0 % | 100,0 % |

### Nombre moyen de clés examinées

| Méthode | Clés examinées en moyenne |
|---|---:|
| Force brute | 312 |
| Fréquences k = 1 | 12 |
| Fréquences k = 2 | 24 |
| Fréquences k = 3 | 36 |
| Fréquences k = 5 | 60 |

Sur l'ensemble des 1 800 essais, la force brute a inclus la vraie clé **1 800 fois sur 1 800 (100 %)**. Le score du khi-deux l'a classée première **1 785 fois sur 1 800 (99,2 %)** : énumérer toutes les clés garantit que la bonne est dans la liste, mais le classement statistique peut tout de même la placer derrière un autre texte.

Pour l'attaque par fréquences, augmenter `k` améliore le taux de présence de la clé dans cette série d'expériences, mais augmente le nombre de candidats. Cela ne démontre pas que `k=5` sera toujours meilleur pour tous les textes : les résultats dépendent du contenu des messages et des fréquences observées.

## 5. Exemple d'échec de k = 1

La phrase suivante sert de cas d'essai : « Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. »

Après normalisation en A-Z, la lettre S apparaît **16 fois** et E **15 fois** : S dépasse donc E d'une occurrence. L'attaque `k=1` suppose que la lettre chiffrée la plus fréquente correspond à E ; dans ce cas, elle suppose à tort que l'image chiffrée de S correspond à E, et la vraie clé n'est pas dans ses candidats.

Avec `k=3`, les trois lettres chiffrées les plus fréquentes sont testées comme pouvant correspondre à E. La lettre chiffrée correspondant réellement à E est alors prise en compte ; pour ce cas construit exprès, la vraie clé est présente et le score du khi-deux la classe première. Ce test explique un mécanisme possible d'échec, mais une seule phrase n'est pas représentative de tous les textes français.

## 6. Limites

- Les expériences utilisent trois paragraphes français ; elles ne représentent pas tous les sujets, styles ou langues.
- Les fréquences théoriques sont des fréquences françaises arrondies puis normalisées. Elles ne conviennent pas automatiquement à une autre langue.
- Le khi-deux compare seulement les fréquences individuelles : il ne tient pas compte de l'ordre des lettres, des syllabes ni des mots.
- Les espaces et la ponctuation sont conservés dans le message chiffré. Cela révèle la longueur des mots et la structure des phrases.
- Une graine fixe facilite la reproduction des mesures, mais les 1 800 essais restent un échantillon de situations possibles.
- Les temps de calcul ne sont pas comparés : pour 26 lettres et des messages courts, les petites différences de temps ne permettraient pas de tirer une conclusion solide.
- Le chiffrement affine est un outil pédagogique, pas une méthode destinée à protéger des données réelles.

## 7. Utilisation des outils et vérification

Un assistant IA a aidé à structurer une partie des fonctions d'attaque, du protocole d'expérience et des tests. Une première version avait une faiblesse méthodologique : elle traitait plusieurs essais issus du même extrait comme s'ils étaient indépendants et tirait une conclusion trop forte sur l'effet de la longueur. La version actuelle utilise des fenêtres de texte aléatoires, trois paragraphes, des clés tirées au hasard et une graine fixe. Les 12 tests automatisés de cette version ont été exécutés et réussis ; la série de 1 800 essais utilisée pour les tableaux a également été exécutée avec la graine indiquée.
