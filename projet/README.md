# Casser un code affine

Nom : [À COMPLÉTER PAR MOI]  
Groupe : [À COMPLÉTER PAR MOI]

## Objectif

Le projet étudie le chiffrement affine : une lettre numérotée `x` devient `(a*x + b) modulo 26`. La valeur `a` doit être première avec 26 pour que le chiffrement soit réversible. Il y a 12 valeurs possibles pour `a` et 26 pour `b`, soit 312 clés.

Le TP5 implémente déjà le chiffrement affine, le PGCD, les inverses modulaires, l'énumération de clés et l'hypothèse « la lettre la plus fréquente correspond à E ». Le projet réutilise le PGCD, les inverses, les clés valides et le nettoyage des lettres du TP5. Je n'appelle pas directement `toutes_les_cles` dans la boucle expérimentale : cette fonction reconstruit le texte pour chaque clé, alors qu'ici je peux compter les lettres une seule fois et calculer le score de chaque clé à partir de ces comptes. L'attaque par fréquences généralise le principe de `casser_par_frequences` à `k = 1, 2, 3, 5`, et le projet ajoute le score du khi-deux et des expériences reproductibles avec des fenêtres aléatoires.

Le projet conserve les espaces et la ponctuation lors du chiffrement pour afficher les messages de façon lisible. Les fonctions d'attaque du TP5, elles, retirent ces caractères avant d'analyser les fréquences : cela convient au score statistique, qui ne compte que les lettres.

## Lancer

Depuis le dossier principal du dépôt :

```bash
python -m pip install -r requirements.txt
python -m projet.main
python -m unittest projet.test_projet -v
python -m tp.test_solutions
```

`projet.main` lance 300 essais pour chacune des longueurs 20, 30, 50, 80, 150 et 280 lettres. Il utilise trois paragraphes français, choisit aléatoirement une fenêtre contenant exactement le nombre demandé de lettres, tire une clé parmi les 312 possibilités et utilise une graine fixée pour pouvoir reproduire l'expérience. Les temps d'exécution ne sont pas comparés : les mesures sur de petits textes et si peu de calculs seraient trop sensibles à l'ordinateur et aux autres processus.

Les résultats détaillés sont écrits dans `projet/resultats/experiences.csv`. Le programme génère également `taux_reussite.png/.svg`, `presence_cle.png/.svg` et `nombre_cles.png/.svg` dans ce dossier.

## Comment lire les résultats

Deux mesures différentes sont enregistrées pour chaque attaque :

1. **Clé présente** : la bonne clé se trouve-t-elle dans la liste des candidats ?
2. **Clé classée première** : parmi les candidats produits, le score du khi-deux place-t-il la bonne clé en première position ?

La force brute énumère les 312 clés : elle doit donc inclure la bonne clé, mais cela ne garantit pas que son score soit classé premier. Pour l'attaque par fréquences, chaque lettre chiffrée parmi les `k` plus fréquentes est supposée correspondre à E ; le nombre de candidats est mesuré dans le CSV, plutôt que supposé constant si le texte ne contient pas assez de lettres distinctes.

## Ce que j'ai observé

Après avoir exécuté le programme, compléter cette section à partir de `experiences.csv` et du bilan imprimé dans le terminal. Ne pas recopier les valeurs d'un ancien lancement.

- Taux où la bonne clé est présente pour la force brute : **[À COMPLÉTER PAR MOI]**.
- Taux où la force brute classe la bonne clé première : **[À COMPLÉTER PAR MOI]**.
- Taux « clé présente » pour les attaques `k = 1` et `k = 3`, selon la longueur : **[À COMPLÉTER PAR MOI]**.
- Taux « rang 1 » pour `k = 1` et `k = 3`, selon la longueur : **[À COMPLÉTER PAR MOI]**.
- Nombre moyen de candidats examinés pour `k = 1, 2, 3, 5` : **[À COMPLÉTER PAR MOI]**.
- Exemple d'échec observé et interprétation personnelle : **[À COMPLÉTER PAR MOI]**.

Le test d'échec utilise cette phrase française : « Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. » Après normalisation en A-Z, S apparaît 16 fois et E 15 : S dépasse donc E d'une occurrence. Avec `k = 1`, le programme suppose que l'image chiffrée de S correspond à E et la bonne clé n'est pas dans les candidats ; avec `k = 3`, l'image chiffrée de E est aussi testée, et dans ce cas la bonne clé arrive première au score du khi-deux.

## Limites

- L'expérience utilise trois textes français et ne permet pas de généraliser à toutes les langues, à tous les styles ou à tous les sujets.
- Le programme utilise l'alphabet A-Z ; les fréquences attendues sont celles du français et ne conviennent pas automatiquement à une autre langue.
- Les espaces et la ponctuation sont conservés dans le texte chiffré, ce qui révèle la longueur des mots et la structure des phrases.
- Les fréquences de lettres ignorent l'ordre des lettres, les syllabes et les mots. Le khi-deux peut donc mal classer un texte court ou atypique.
- La graine fixe rend l'expérience reproductible, mais les fenêtres et clés testées restent un échantillon des situations possibles.
- Le chiffrement affine est un exercice pédagogique, pas une méthode pour protéger de vraies données.

## Utilisation de l'IA et vérifications

L'assistant IA a aidé à proposer la structure de l'attaque avec plusieurs valeurs de `k`, le protocole d'expériences reproductibles, les tests et une première version de cette documentation. J'ai relu le code et exécuté les commandes suivantes : **[À COMPLÉTER PAR MOI : indiquer les commandes réellement exécutées et les résultats vérifiés]**. Je dois aussi pouvoir expliquer oralement le calcul de la clé, le score du khi-deux et les deux critères de réussite.

Un point où l'assistant s'était trompé dans une version antérieure : il avait interprété 12 résultats obtenus à partir du début d'un même texte comme s'il s'agissait de 12 situations indépendantes, puis en avait tiré une conclusion trop forte sur l'effet de la longueur. Cette version corrige le protocole en tirant des fenêtres aléatoires dans trois paragraphes et des clés aléatoires, avec une graine fixe.
