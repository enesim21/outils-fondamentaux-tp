from collections import Counter
import math

from tp.tp5 import nettoyer as nettoyer_lettres
from projet.chiffrement import ALPHABET, TAILLE, cles_valides, inverse_modulaire

FREQUENCES_FR = {
    "A": 0.076, "B": 0.009, "C": 0.032, "D": 0.037,
    "E": 0.147, "F": 0.011, "G": 0.010, "H": 0.007,
    "I": 0.075, "J": 0.006, "K": 0.001, "L": 0.055,
    "M": 0.030, "N": 0.071, "O": 0.053, "P": 0.030,
    "Q": 0.014, "R": 0.066, "S": 0.079, "T": 0.072,
    "U": 0.063, "V": 0.018, "W": 0.001, "X": 0.004,
    "Y": 0.003, "Z": 0.003,
}

K_AUTORISES = (1, 2, 3, 5)


def lettres(texte):
    # Le TP5 sait déjà normaliser un texte en ne gardant que A-Z.
    return nettoyer_lettres(texte)


def score_frequences(texte):
    texte = lettres(texte)
    n = len(texte)
    if n == 0:
        return math.inf
    compte = Counter(texte)
    score = 0.0
    for lettre in ALPHABET:
        observe = compte.get(lettre, 0)
        attendu = n * FREQUENCES_FR[lettre]
        if attendu > 0:
            score += (observe - attendu) ** 2 / attendu
    return score


def _score_compte(compte, n):
    score = 0.0
    for numero, lettre in enumerate(ALPHABET):
        attendu = n * FREQUENCES_FR[lettre]
        if attendu > 0:
            score += (compte[numero] - attendu) ** 2 / attendu
    return score


def _candidat(texte_chiffre, compte_chiffre, a, b):
    # La formule de chiffrement permet de permuter les 26 comptes sans les recompter.
    compte_clair = [compte_chiffre[(a * x + b) % TAILLE] for x in range(TAILLE)]
    inverse = inverse_modulaire(a)
    correspondances = "".join(
        ALPHABET[(inverse * (y - b)) % TAILLE] for y in range(TAILLE)
    )
    texte_clair = texte_chiffre.translate(str.maketrans(ALPHABET, correspondances))
    return {
        "a": a,
        "b": b,
        "texte": texte_clair,
        "score": _score_compte(compte_clair, len(texte_chiffre)),
    }


def attaque_force_brute(secret):
    texte = lettres(secret)
    if not texte:
        return []

    # Le TP5 propose toutes_les_cles. Ici, pour des centaines d'expériences,
    # je précompte les lettres une fois : reconstruire chaque texte avec cette
    # fonction serait inutilement lent. Les clés valides et l'inverse viennent du TP5.
    compte = Counter(texte)
    compte_chiffre = [compte.get(lettre, 0) for lettre in ALPHABET]
    candidats = [
        _candidat(texte, compte_chiffre, a, b)
        for a in cles_valides()
        for b in range(TAILLE)
    ]
    return sorted(candidats, key=lambda candidat: candidat["score"])


def attaque_frequences(secret, k=1):
    if type(k) is not int or k not in K_AUTORISES:
        raise ValueError("k doit valoir 1, 2, 3 ou 5.")
    texte = lettres(secret)
    if not texte:
        return []

    compte = Counter(texte)
    compte_chiffre = [compte.get(lettre, 0) for lettre in ALPHABET]
    # Même principe que casser_par_frequences du TP5, généralisé aux k lettres.
    lettres_courantes = [lettre for lettre, _ in compte.most_common(k)]
    numero_e = ALPHABET.index("E")
    candidats = []
    for lettre in lettres_courantes:
        numero_chiffre = ALPHABET.index(lettre)
        for a in cles_valides():
            b = (numero_chiffre - a * numero_e) % TAILLE
            candidats.append(_candidat(texte, compte_chiffre, a, b))
    return sorted(candidats, key=lambda candidat: candidat["score"])


def rang_cle(candidats, a, b):
    for rang, candidat in enumerate(candidats, start=1):
        if candidat["a"] == a and candidat["b"] == b:
            return rang
    return None
