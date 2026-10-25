import unicodedata

from tp.tp5 import pgcd, inverse_modulaire as _inverse_modulaire_tp5
from tp.tp5 import cles_valides

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TAILLE = len(ALPHABET)


def nettoyer(texte):
    """Retire les accents et met en majuscules sans effacer les espaces."""
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte.upper()


def inverse_modulaire(a, modulo=TAILLE):
    # Réutilise l'algorithme du TP5, avec le modulo 26 par défaut.
    return _inverse_modulaire_tp5(a, modulo)


def _verifier_cle(a, b):
    # Si a=2, A (x=0) et N (x=13) donnent le meme resultat, car 2*13=26.
    # Il faut donc pgcd(a, 26)=1 pour que chaque lettre ait un inverse unique.
    if type(a) is not int or pgcd(a, TAILLE) != 1:
        raise ValueError("a doit etre un entier premier avec 26.")
    if type(b) is not int or not 0 <= b < TAILLE:
        raise ValueError("b doit etre un entier compris entre 0 et 25.")


def chiffrer(texte, a, b):
    _verifier_cle(a, b)
    resultat = []
    for caractere in nettoyer(texte):
        if caractere in ALPHABET:
            x = ALPHABET.index(caractere)
            resultat.append(ALPHABET[(a * x + b) % TAILLE])
        else:
            resultat.append(caractere)
    return "".join(resultat)


def dechiffrer(texte, a, b):
    _verifier_cle(a, b)
    inverse = inverse_modulaire(a)
    resultat = []
    for caractere in nettoyer(texte):
        if caractere in ALPHABET:
            y = ALPHABET.index(caractere)
            resultat.append(ALPHABET[(inverse * (y - b)) % TAILLE])
        else:
            resultat.append(caractere)
    return "".join(resultat)
