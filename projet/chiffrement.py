import unicodedata

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TAILLE = len(ALPHABET)


def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return texte.upper()


def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def cles_valides():
    return [a for a in range(1, TAILLE) if pgcd(a, TAILLE) == 1]


def inverse_modulaire(a, modulo=TAILLE):
    for x in range(modulo):
        if (a * x) % modulo == 1:
            return x
    raise ValueError("Cette cle ne possede pas d'inverse modulo 26.")


def chiffrer(texte, a, b):
    if a not in cles_valides():
        raise ValueError("a doit etre premier avec 26.")
    resultat = []
    for caractere in nettoyer(texte):
        if caractere in ALPHABET:
            x = ALPHABET.index(caractere)
            resultat.append(ALPHABET[(a * x + b) % TAILLE])
        else:
            resultat.append(caractere)
    return "".join(resultat)


def dechiffrer(texte, a, b):
    if a not in cles_valides():
        raise ValueError("a doit etre premier avec 26.")
    inverse = inverse_modulaire(a)
    resultat = []
    for caractere in nettoyer(texte):
        if caractere in ALPHABET:
            y = ALPHABET.index(caractere)
            resultat.append(ALPHABET[(inverse * (y - b)) % TAILLE])
        else:
            resultat.append(caractere)
    return "".join(resultat)
