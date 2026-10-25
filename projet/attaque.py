from collections import Counter
import math

from projet.chiffrement import ALPHABET, TAILLE, cles_valides, dechiffrer

FREQUENCES_FR = {
    "A": 0.076, "B": 0.009, "C": 0.032, "D": 0.037,
    "E": 0.147, "F": 0.011, "G": 0.010, "H": 0.007,
    "I": 0.075, "J": 0.006, "K": 0.001, "L": 0.055,
    "M": 0.030, "N": 0.071, "O": 0.053, "P": 0.030,
    "Q": 0.014, "R": 0.066, "S": 0.079, "T": 0.072,
    "U": 0.063, "V": 0.018, "W": 0.001, "X": 0.004,
    "Y": 0.003, "Z": 0.003,
}


def lettres(texte):
    return [c for c in texte if c in ALPHABET]


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


def attaque_force_brute(secret):
    candidats = []
    for a in cles_valides():
        for b in range(TAILLE):
            texte = dechiffrer(secret, a, b)
            candidats.append({
                "a": a,
                "b": b,
                "texte": texte,
                "score": score_frequences(texte),
            })
    return sorted(candidats, key=lambda c: c["score"])


def attaque_frequences(secret):
    texte = lettres(secret)
    if not texte:
        return []
    lettre_plus_frequente = Counter(texte).most_common(1)[0][0]
    y = ALPHABET.index(lettre_plus_frequente)
    e = ALPHABET.index("E")
    candidats = []
    # On suppose que la lettre la plus frequente correspond a E.
    for a in cles_valides():
        b = (y - a * e) % TAILLE
        clair = dechiffrer(secret, a, b)
        candidats.append({
            "a": a,
            "b": b,
            "texte": clair,
            "score": score_frequences(clair),
        })
    return sorted(candidats, key=lambda c: c["score"])


def rang_cle(candidats, a, b):
    for rang, candidat in enumerate(candidats, start=1):
        if candidat["a"] == a and candidat["b"] == b:
            return rang
    return None
