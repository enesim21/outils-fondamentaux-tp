import csv
import random
from pathlib import Path

from tp.tp5 import pgcd
from projet.chiffrement import ALPHABET, TAILLE, chiffrer, cles_valides, inverse_modulaire
from projet.attaque import lettres
from projet.experiences import TEXTES_FRANCAIS, GRAINE_DEFAUT

LETTRES_CONNUES = (1, 2, 3, 4, 6, 8)
ESSAIS_CLAIR_CONNU = 1000


def _numeros(texte):
    return [ALPHABET.index(c) for c in lettres(texte)]


def resoudre_deux_paires(x1, y1, x2, y2):
    """Résout le système  a*x1 + b = y1  et  a*x2 + b = y2  (mod 26).

    Sous forme matricielle : [[x1, 1], [x2, 1]] * [a, b] = [y1, y2].
    Le déterminant vaut x1 - x2. Comme au TP4, la solution est unique si le
    déterminant est inversible, mais ici « inversible » veut dire premier
    avec 26 (et pas seulement non nul).
    Renvoie (a, b), ou None si le déterminant n'est pas inversible modulo 26.
    """
    determinant = (x1 - x2) % TAILLE
    if pgcd(determinant, TAILLE) != 1:
        return None
    # En soustrayant les deux équations : a * (x1 - x2) = y1 - y2 (mod 26).
    a = (y1 - y2) * inverse_modulaire(determinant) % TAILLE
    b = (y1 - a * x1) % TAILLE
    return a, b


def cles_compatibles(clair, secret):
    """Toutes les clés valides (a, b) qui envoient chaque lettre de clair sur secret."""
    xs = _numeros(clair)
    ys = _numeros(secret)
    if len(xs) != len(ys):
        raise ValueError("clair et secret doivent avoir le meme nombre de lettres.")
    if not xs:
        raise ValueError("Il faut au moins une lettre connue.")
    resultat = []
    for a in cles_valides():
        # La première paire fixe b pour chaque a ; on vérifie les autres.
        b = (ys[0] - a * xs[0]) % TAILLE
        if all((a * x + b) % TAILLE == y for x, y in zip(xs, ys)):
            resultat.append((a, b))
    return resultat


def couples_ambigus():
    """Couples de deux lettres différentes qui laissent plusieurs clés possibles.

    Le résultat ne dépend pas de la clé utilisée : on prend (5, 8).
    """
    ambigus = []
    for x1 in range(TAILLE):
        for x2 in range(TAILLE):
            if x1 == x2:
                continue
            clair = ALPHABET[x1] + ALPHABET[x2]
            if len(cles_compatibles(clair, chiffrer(clair, 5, 8))) > 1:
                ambigus.append(clair)
    return ambigus


def experience_clair_connu(nombre_essais=ESSAIS_CLAIR_CONNU, graine=GRAINE_DEFAUT,
                           lettres_connues=LETTRES_CONNUES):
    """Combien de lettres du message faut-il connaître pour trouver la clé ?

    À chaque essai : une clé au hasard, un morceau d'un des trois paragraphes,
    et on suppose connues ses m premières lettres. On compare la méthode du
    déterminant (deux premières lettres) avec la liste des clés compatibles.
    """
    if type(nombre_essais) is not int or nombre_essais < 1:
        raise ValueError("nombre_essais doit etre un entier positif.")
    generateur = random.Random(graine)
    textes = [lettres(texte) for _, texte in TEXTES_FRANCAIS]
    lignes = []
    for m in lettres_connues:
        uniques = determinant_ok = total_candidats = meme_lettre = ecart_13 = 0
        for _ in range(nombre_essais):
            texte = generateur.choice(textes)
            debut = generateur.randrange(len(texte) - m + 1)
            clair = texte[debut:debut + m]
            a = generateur.choice(cles_valides())
            b = generateur.randrange(TAILLE)
            secret = chiffrer(clair, a, b)
            candidats = cles_compatibles(clair, secret)
            # La vraie clé est toujours compatible : seul le nombre compte.
            total_candidats += len(candidats)
            uniques += len(candidats) == 1
            if m >= 2:
                x1, x2 = _numeros(clair[:2])
                y1, y2 = _numeros(secret[:2])
                determinant_ok += resoudre_deux_paires(x1, y1, x2, y2) is not None
                if len(candidats) > 1:
                    meme_lettre += x1 == x2
                    ecart_13 += (x1 - x2) % TAILLE == 13
        lignes.append({
            "lettres_connues": m,
            "cle_unique_pourcent": round(100 * uniques / nombre_essais, 1),
            "determinant_inversible_pourcent": round(100 * determinant_ok / nombre_essais, 1),
            "candidats_moyens": round(total_candidats / nombre_essais, 2),
            "echecs_meme_lettre": meme_lettre,
            "echecs_ecart_13": ecart_13,
        })
    return lignes


def enregistrer_clair_connu(lignes, chemin=None):
    if chemin is None:
        chemin = Path(__file__).resolve().parent / "resultats" / "clair_connu.csv"
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0].keys()))
        writer.writeheader()
        writer.writerows(lignes)
    return chemin
