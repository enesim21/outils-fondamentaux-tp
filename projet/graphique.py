from pathlib import Path

import matplotlib.pyplot as plt


def creer_graphiques(lignes, dossier=None):
    if dossier is None:
        dossier = Path(__file__).resolve().parent / "resultats"
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)

    longueurs = sorted({int(ligne["longueur"]) for ligne in lignes})
    brute = []
    frequence = []
    reussites = []

    for longueur in longueurs:
        groupe = [l for l in lignes if int(l["longueur"]) == longueur]
        brute.append(int(groupe[0]["cles_force_brute"]))
        frequence.append(int(groupe[0]["cles_frequences"]))
        reussites.append(sum(l["rang_frequences"] != "non trouvee" for l in groupe))

    x = range(len(longueurs))
    largeur = 0.36
    plt.figure(figsize=(8, 4.5))
    plt.bar([i - largeur / 2 for i in x], brute, largeur, label="Force brute")
    plt.bar([i + largeur / 2 for i in x], frequence, largeur, label="Frequences")
    plt.xticks(list(x), [str(n) for n in longueurs])
    plt.xlabel("Longueur du message (caracteres)")
    plt.ylabel("Nombre de cles candidates")
    plt.title("Nombre de cles examinees")
    plt.legend()
    plt.tight_layout()
    plt.savefig(dossier / "nombre_cles.png", dpi=150)
    plt.savefig(dossier / "nombre_cles.svg")
    plt.close()

    plt.figure(figsize=(8, 4.5))
    plt.plot(longueurs, reussites, marker="o")
    plt.xticks(longueurs)
    plt.xlabel("Longueur du message (caracteres)")
    plt.ylabel("Cles retrouvees parmi 3 essais")
    plt.title("Reussite de l'attaque par frequences")
    plt.ylim(0, 3.5)
    plt.tight_layout()
    plt.savefig(dossier / "reussite_frequences.png", dpi=150)
    plt.savefig(dossier / "reussite_frequences.svg")
    plt.close()
