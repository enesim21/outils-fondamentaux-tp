import csv
from pathlib import Path

from projet.fonctions import CAS
from projet.methodes import dichotomie, newton, hybride


COLONNES = [
    "fonction", "methode", "racine", "iterations", "evaluations_f",
    "evaluations_df", "erreur", "succes", "raison", "pas_newton",
    "pas_dichotomie",
]


def comparer():
    resultats = []

    for nom, cas in CAS.items():
        methodes = [
            ("Dichotomie", lambda c=cas: dichotomie(c["f"], c["a"], c["b"])),
            ("Newton", lambda c=cas: newton(c["f"], c["df"], c["x0"])),
            ("Hybride", lambda c=cas: hybride(
                c["f"], c["df"], c["a"], c["b"], c["x0"]
            )),
        ]

        for nom_methode, lancer in methodes:
            try:
                ligne = lancer()
            except (ValueError, ZeroDivisionError, OverflowError) as erreur:
                ligne = {
                    "methode": nom_methode,
                    "racine": None,
                    "iterations": 0,
                    "evaluations_f": 0,
                    "evaluations_df": 0,
                    "erreur": None,
                    "succes": False,
                    "raison": str(erreur),
                    "pas_newton": 0,
                    "pas_dichotomie": 0,
                }
            ligne["fonction"] = nom
            resultats.append(ligne)

    return resultats


def enregistrer_csv(resultats, dossier=None):
    if dossier is None:
        dossier = Path(__file__).resolve().parent / "resultats"
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / "comparaison.csv"

    with chemin.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=COLONNES)
        writer.writeheader()
        writer.writerows(resultats)

    return chemin
