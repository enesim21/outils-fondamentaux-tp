import csv
from pathlib import Path
from time import perf_counter

from projet.attaque import attaque_force_brute, attaque_frequences, rang_cle
from projet.chiffrement import chiffrer

TEXTE = """
Quand on apprend la programmation, on commence souvent par chercher une solution qui fonctionne.
Ensuite, on peut comparer plusieurs methodes et mesurer leurs differences. Un resultat rapide n'est
pas toujours le plus fiable, et un programme qui echoue peut tout de meme nous apprendre quelque
chose. Dans cette experience, nous utilisons un chiffrement affine pour observer comment la longueur
d'un message influence une attaque. Le chiffrement remplace chaque lettre par une autre selon deux
parametres. Le premier parametre doit etre premier avec vingt-six pour que le message puisse etre
retrouve. Une attaque par force brute teste toutes les cles possibles. Une attaque par frequences
fait une hypothese sur la lettre la plus commune, ce qui reduit le nombre de cles a essayer, mais
cette hypothese n'est pas toujours juste. Les mesures permettent de voir la difference entre les deux.
""".upper().replace("\n", " ")

CLES = [(5, 8), (7, 3), (11, 17)]
LONGUEURS = [30, 80, 150, 280]


def lancer_experiences():
    lignes = []
    texte_nettoye = "".join(c for c in TEXTE if c.isalpha() or c.isspace())

    for longueur in LONGUEURS:
        clair = texte_nettoye[:longueur]
        for a, b in CLES:
            secret = chiffrer(clair, a, b)

            debut = perf_counter()
            brute = attaque_force_brute(secret)
            temps_brute = perf_counter() - debut

            debut = perf_counter()
            frequence = attaque_frequences(secret)
            temps_frequence = perf_counter() - debut

            lignes.append({
                "longueur": longueur,
                "cle_a": a,
                "cle_b": b,
                "cles_force_brute": 312,
                "rang_force_brute": rang_cle(brute, a, b) or "non classe",
                "temps_force_brute_s": f"{temps_brute:.6f}",
                "cles_frequences": len(frequence),
                "rang_frequences": rang_cle(frequence, a, b) or "non trouvee",
                "temps_frequences_s": f"{temps_frequence:.6f}",
            })

    return lignes


def enregistrer(lignes, chemin=None):
    if chemin is None:
        chemin = Path(__file__).resolve().parent / "resultats" / "experiences.csv"
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0].keys()))
        writer.writeheader()
        writer.writerows(lignes)
    return chemin
