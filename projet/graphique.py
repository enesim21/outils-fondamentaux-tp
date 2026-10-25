from pathlib import Path

import matplotlib.pyplot as plt


def _taux(groupe, nom_colonne):
    return 100 * sum(bool(ligne[nom_colonne]) for ligne in groupe) / len(groupe)


def creer_graphiques(lignes, dossier=None):
    if not lignes:
        raise ValueError("Aucun resultat pour creer les graphiques.")
    if dossier is None:
        dossier = Path(__file__).resolve().parent / "resultats"
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    longueurs = sorted({int(ligne["longueur_lettres"]) for ligne in lignes})
    groupes = {
        longueur: [ligne for ligne in lignes if int(ligne["longueur_lettres"]) == longueur]
        for longueur in longueurs
    }

    # Le taux de réussite signifie ici « vraie clé classée première par le khi-deux ».
    plt.figure(figsize=(8, 4.8))
    for colonne, etiquette in (
        ("brute_rang1", "Force brute + khi-deux"),
        ("k1_rang1", "Fréquences k=1 + khi-deux"),
        ("k3_rang1", "Fréquences k=3 + khi-deux"),
    ):
        valeurs = [_taux(groupes[longueur], colonne) for longueur in longueurs]
        plt.plot(longueurs, valeurs, marker="o", linewidth=2, label=etiquette)
    plt.xticks(longueurs)
    plt.ylim(50, 102)
    plt.xlabel("Longueur du message (nombre de lettres, espaces exclus)")
    plt.ylabel("Vraie clé classée première (%)")
    plt.title("Taux de classement en première position")
    plt.grid(axis="y", alpha=0.3)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(dossier / "taux_reussite.png", dpi=160)
    plt.savefig(dossier / "taux_reussite.svg")
    plt.close()

    # La présence de la clé est une mesure différente du classement par score.
    plt.figure(figsize=(8, 4.8))
    for colonne, etiquette in (
        ("brute_cle_presente", "Force brute"),
        ("k1_cle_presente", "Fréquences k=1"),
        ("k3_cle_presente", "Fréquences k=3"),
    ):
        valeurs = [_taux(groupes[longueur], colonne) for longueur in longueurs]
        plt.plot(longueurs, valeurs, marker="o", linewidth=2, label=etiquette)
    plt.xticks(longueurs)
    plt.ylim(50, 102)
    plt.xlabel("Longueur du message (nombre de lettres, espaces exclus)")
    plt.ylabel("Vraie clé présente dans les candidats (%)")
    plt.title("Présence de la clé dans les candidats")
    plt.grid(axis="y", alpha=0.3)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(dossier / "presence_cle.png", dpi=160)
    plt.savefig(dossier / "presence_cle.svg")
    plt.close()

    colonnes = (
        ("brute_nb_cles", "Force brute"),
        ("k1_nb_cles", "Fréquences k=1"),
        ("k2_nb_cles", "Fréquences k=2"),
        ("k3_nb_cles", "Fréquences k=3"),
        ("k5_nb_cles", "Fréquences k=5"),
    )
    moyennes = [sum(float(ligne[nom]) for ligne in lignes) / len(lignes) for nom, _ in colonnes]
    etiquettes = [etiquette for _, etiquette in colonnes]
    plt.figure(figsize=(8, 4.8))
    plt.bar(etiquettes, moyennes)
    plt.ylabel("Nombre moyen de clés examinées")
    plt.title("Nombre de candidats examinés par méthode")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(dossier / "nombre_cles.png", dpi=160)
    plt.savefig(dossier / "nombre_cles.svg")
    plt.close()
