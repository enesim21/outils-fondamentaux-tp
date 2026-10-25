from pathlib import Path

from projet.experiences import comparer, enregistrer_csv
from projet.graphique import tracer


def main():
    resultats = comparer()

    print(f"{'Fonction':20} {'Methode':12} {'OK':4} {'Iter.':6} {'Erreur':12}")
    print("-" * 61)

    for r in resultats:
        racine = r["racine"]
        erreur = r["erreur"]
        racine_txt = "-" if racine is None else f"{racine:.8f}"
        erreur_txt = "-" if erreur is None else f"{erreur:.2e}"
        statut = "oui" if r["succes"] else "non"

        print(f"{r['fonction']:20} {r['methode']:12} {statut:4} "
              f"{r['iterations']:<6} {erreur_txt:12}")
        if not r["succes"]:
            print("  ", r["raison"])

    dossier = Path(__file__).resolve().parent / "resultats"
    chemin = enregistrer_csv(resultats, dossier)
    print(f"\nFichier CSV : {chemin}")
    tracer(resultats, dossier / "iterations.png")


if __name__ == "__main__":
    main()
