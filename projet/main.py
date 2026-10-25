from pathlib import Path

from projet.experiences import comparer, enregistrer_csv
from projet.graphique import tracer


def main():
    resultats = comparer()

    print(f"{'Fonction':20} {'Methode':14} {'OK':4} {'Iter.':6} "
          f"{'f(x)':12} {'Appels f':9} {'Appels f\u2032':10}")
    print("-" * 84)

    for r in resultats:
        erreur = r["erreur"]
        erreur_txt = "-" if erreur is None else f"{erreur:.2e}"
        statut = "oui" if r["succes"] else "non"

        print(f"{r['fonction']:20} {r['methode']:14} {statut:4} "
              f"{r['iterations']:<6} {erreur_txt:12} "
              f"{r['evaluations_f']:<9} {r['evaluations_df']:<10}")
        if not r["succes"]:
            print("  ", r["raison"])

    dossier = Path(__file__).resolve().parent / "resultats"
    chemin = enregistrer_csv(resultats, dossier)
    tracer(resultats, dossier)
    print(f"\nCSV : {chemin}")
    print(f"Graphiques : {dossier}")


if __name__ == "__main__":
    main()
