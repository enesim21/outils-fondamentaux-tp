from pathlib import Path

import matplotlib.pyplot as plt


def tracer_iterations(resultats, chemin):
    lignes = [r for r in resultats if r["succes"]]
    if not lignes:
        print("Aucun resultat a afficher.")
        return

    etiquettes = [f"{r['fonction']}\n{r['methode']}" for r in lignes]
    iterations = [r["iterations"] for r in lignes]

    plt.figure(figsize=(12, 5))
    plt.bar(etiquettes, iterations)
    plt.ylabel("Nombre d'iterations")
    plt.title("Nombre d'iterations selon la methode")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(chemin, dpi=150)
    plt.close()


def tracer_erreurs(resultats, chemin):
    lignes = [r for r in resultats if r["succes"] and r["erreur"] is not None]
    if not lignes:
        return

    etiquettes = [f"{r['fonction']}\n{r['methode']}" for r in lignes]
    erreurs = [max(r["erreur"], 1e-16) for r in lignes]

    plt.figure(figsize=(12, 5))
    plt.bar(etiquettes, erreurs)
    plt.yscale("log")
    plt.ylabel("Valeur absolue de f(racine)")
    plt.title("Erreur finale (0 affiche a 1e-16)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(chemin, dpi=150)
    plt.close()


def tracer(resultats, dossier=None):
    if dossier is None:
        dossier = Path(__file__).resolve().parent / "resultats"
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    tracer_iterations(resultats, dossier / "iterations.png")
    tracer_erreurs(resultats, dossier / "erreurs.png")
