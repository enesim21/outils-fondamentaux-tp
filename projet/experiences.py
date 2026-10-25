import csv
from pathlib import Path

from scipy.optimize import brentq

from projet.fonctions import CAS
from projet.methodes import dichotomie, newton, hybride


COLONNES = [
    "fonction", "methode", "racine", "iterations", "evaluations_f",
    "evaluations_df", "erreur", "succes", "raison", "pas_newton",
    "pas_dichotomie",
]


def compter(f):
    compteur = {"nombre": 0}

    def fonction(x):
        compteur["nombre"] += 1
        return f(x)

    return fonction, compteur


def comparer():
    resultats = []

    for nom, cas in CAS.items():
        methodes = [
            ("Dichotomie", lambda f, df, c=cas: dichotomie(f, c["a"], c["b"])),
            ("Newton", lambda f, df, c=cas: newton(f, df, c["x0"])),
            ("Hybride", lambda f, df, c=cas: hybride(
                f, df, c["a"], c["b"], c["x0"]
            )),
        ]

        for nom_methode, lancer in methodes:
            f, compteur_f = compter(cas["f"])
            df, compteur_df = compter(cas["df"])
            try:
                ligne = lancer(f, df)
                ligne["evaluations_f"] = compteur_f["nombre"]
                ligne["evaluations_df"] = compteur_df["nombre"]
            except (ValueError, ZeroDivisionError, OverflowError) as erreur:
                ligne = {
                    "methode": nom_methode,
                    "racine": None,
                    "iterations": 0,
                    "evaluations_f": compteur_f["nombre"],
                    "evaluations_df": compteur_df["nombre"],
                    "erreur": None,
                    "succes": False,
                    "raison": str(erreur),
                    "pas_newton": 0,
                    "pas_dichotomie": 0,
                }
            ligne["fonction"] = nom
            resultats.append(ligne)

        f, compteur_f = compter(cas["f"])
        try:
            racine, infos = brentq(
                f, cas["a"], cas["b"], xtol=1e-10,
                maxiter=1000, full_output=True
            )
            erreur_finale = abs(f(racine))
            ligne = {
                "methode": "Brent (SciPy)",
                "racine": racine,
                "iterations": infos.iterations,
                "evaluations_f": compteur_f["nombre"],
                "evaluations_df": 0,
                "erreur": erreur_finale,
                "succes": infos.converged,
                "raison": "Reference SciPy.",
                "pas_newton": 0,
                "pas_dichotomie": 0,
            }
        except (ValueError, ZeroDivisionError, OverflowError) as erreur:
            ligne = {
                "methode": "Brent (SciPy)",
                "racine": None,
                "iterations": 0,
                "evaluations_f": compteur_f["nombre"],
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
