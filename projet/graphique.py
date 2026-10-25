import matplotlib.pyplot as plt


def tracer(resultats, chemin=None):
    lignes = [r for r in resultats if r["succes"]]
    if not lignes:
        print("Aucun resultat a afficher.")
        return

    etiquettes = [f"{r['fonction']}\n{r['methode']}" for r in lignes]
    valeurs = [r["iterations"] for r in lignes]

    plt.figure(figsize=(10, 5))
    plt.bar(etiquettes, valeurs)
    plt.ylabel("Iterations")
    plt.title("Comparaison des methodes")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    if chemin is not None:
        plt.savefig(chemin, dpi=150)
    plt.show()
