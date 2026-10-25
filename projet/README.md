# Casser un code affine

J'ai choisi le chiffrement affine parce qu'il utilise le PGCD et les calculs modulo vus en TP. Le programme chiffre un message, le dechiffre, puis essaie de retrouver la cle sans la connaitre.

## Lancer

Depuis le dossier principal du depot :

    python -m pip install -r requirements.txt
    python -m projet.main
    python -m unittest projet.test_projet -v

Le programme cree un CSV et deux graphiques dans `projet/resultats/`.

## Ce que je compare

La force brute teste les 312 cles possibles. L'attaque par frequences fait une hypothese sur la lettre la plus courante et ne garde que 12 cles. Cette hypothese peut se tromper, surtout sur un message court.

Les experiences testent plusieurs longueurs de message et plusieurs cles. Le CSV contient les rangs de la vraie cle et le temps mesure. Les temps dependent de l'ordinateur, donc ils peuvent varier d'une execution a l'autre.

Le chiffrement affine est simple a casser et ne doit pas servir a proteger de vraies donnees. Les frequences des lettres changent aussi selon le texte. Une aide IA a servi a organiser une partie du code ; je dois relire les fonctions et expliquer les resultats.
