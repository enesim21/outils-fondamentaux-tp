import unicodedata

ALPHABET = 26


def lettre_vers_nombre(c):
    return ord(c.upper()) - ord("A")


def nombre_vers_lettre(n):
    return chr(ord("A") + n % ALPHABET)


def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return "".join(c for c in texte.upper() if "A" <= c <= "Z")


def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


def inverse_modulaire(a, n):
    # Inverse modulo n.
    for x in range(n):
        if (a * x) % n == 1:
            return x
    raise ValueError("Cette cle n'a pas d'inverse modulo n.")


def cles_valides():
    return [a for a in range(1, ALPHABET) if pgcd(a, ALPHABET) == 1]


def chiffrer(texte, a, b):
    texte = nettoyer(texte)
    resultat = ""
    for c in texte:
        x = lettre_vers_nombre(c)
        resultat += nombre_vers_lettre(a * x + b)
    return resultat


def dechiffrer(texte, a, b):
    inverse = inverse_modulaire(a, ALPHABET)
    texte = nettoyer(texte)
    resultat = ""
    for c in texte:
        y = lettre_vers_nombre(c)
        resultat += nombre_vers_lettre(inverse * (y - b))
    return resultat


def toutes_les_cles(secret):
    propositions = []
    for a in cles_valides():
        for b in range(ALPHABET):
            propositions.append((a, b, dechiffrer(secret, a, b)))
    return propositions


def frequences(texte):
    texte = nettoyer(texte)
    compte = {}
    for c in texte:
        compte[c] = compte.get(c, 0) + 1
    return compte


def casser_par_frequences(secret):
    compte = frequences(secret)
    if not compte:
        return []

    # E est supposee la plus frequente.
    lettre_courante = max(compte, key=compte.get)
    numero = lettre_vers_nombre(lettre_courante)
    numero_e = lettre_vers_nombre("E")
    resultats = []
    for a in cles_valides():
        b = (numero - a * numero_e) % ALPHABET
        resultats.append((a, b, dechiffrer(secret, a, b)))
    return resultats


def indice_coincidence(texte):
    texte = nettoyer(texte)
    n = len(texte)
    if n < 2:
        return 0
    compte = frequences(texte)
    total = 0
    for nombre in compte.values():
        total += nombre * (nombre - 1)
    return total / (n * (n - 1))


if __name__ == "__main__":
    message = "Attaque a l'aube"
    secret = chiffrer(message, 5, 8)
    print("Message :", nettoyer(message))
    print("Chiffre :", secret)
    print("Dechiffre :", dechiffrer(secret, 5, 8))
    print("Nombre de cles :", len(toutes_les_cles(secret)))
    print("Candidats par frequences :", len(casser_par_frequences(secret)))
