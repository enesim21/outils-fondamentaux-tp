from projet.chiffrement import chiffrer, dechiffrer
from projet.attaque import K_AUTORISES, attaque_force_brute, attaque_frequences, rang_cle
from projet.experiences import (
    ESSAIS_PAR_LONGUEUR,
    LONGUEURS_LETTRES,
    GRAINE_DEFAUT,
    lancer_experiences,
    enregistrer,
)
from projet.graphique import creer_graphiques
from projet.clair_connu import experience_clair_connu, enregistrer_clair_connu


def _taux(lignes, colonne):
    return 100 * sum(bool(ligne[colonne]) for ligne in lignes) / len(lignes)


def afficher_bilan(lignes):
    print("\nTaux de classement en première position par le khi-deux")
    entete = "Lettres | Force brute | " + " | ".join(f"k={k}" for k in K_AUTORISES)
    print(entete)
    for longueur in LONGUEURS_LETTRES:
        groupe = [ligne for ligne in lignes if ligne["longueur_lettres"] == longueur]
        valeurs = [_taux(groupe, "brute_rang1")]
        valeurs += [_taux(groupe, f"k{k}_rang1") for k in K_AUTORISES]
        print(f"{longueur:>7} | " + " | ".join(f"{v:>8.1f}%" for v in valeurs))

    print("\nPrésence de la vraie clé dans les candidats")
    print(entete)
    for longueur in LONGUEURS_LETTRES:
        groupe = [ligne for ligne in lignes if ligne["longueur_lettres"] == longueur]
        valeurs = [_taux(groupe, "brute_cle_presente")]
        valeurs += [_taux(groupe, f"k{k}_cle_presente") for k in K_AUTORISES]
        print(f"{longueur:>7} | " + " | ".join(f"{v:>8.1f}%" for v in valeurs))

    print("\nNombre moyen de clés examinées")
    for k in K_AUTORISES:
        moyenne = sum(ligne[f"k{k}_nb_cles"] for ligne in lignes) / len(lignes)
        print(f"Fréquences k={k} : {moyenne:.1f} clés en moyenne")


def main():
    message = "LE CODE SECRET EST CACHE DANS CE MESSAGE"
    a, b = 5, 8
    secret = chiffrer(message, a, b)

    print("Message :", message)
    print("Message chiffre :", secret)
    print("Message dechiffre :", dechiffrer(secret, a, b))

    brute = attaque_force_brute(secret)
    frequence = attaque_frequences(secret, k=1)
    print("\nNombre de clés valides :", len(brute))
    print("Candidats fréquences k=1 :", len(frequence))
    print("Rang de la clé en force brute :", rang_cle(brute, a, b))
    print("Rang de la clé par fréquences k=1 :", rang_cle(frequence, a, b))

    print(
        f"\nLancement des expériences : {ESSAIS_PAR_LONGUEUR} essais par longueur, "
        f"graine {GRAINE_DEFAUT}."
    )
    lignes = lancer_experiences()
    chemin = enregistrer(lignes)
    creer_graphiques(lignes)
    afficher_bilan(lignes)
    print("\nAttaque à clair connu : clés possibles selon le nombre de lettres connues")
    print("Lettres connues | Clé unique | Déterminant inversible | Candidats moyens")
    lignes_clair = experience_clair_connu()
    for ligne in lignes_clair:
        print(
            f"{ligne['lettres_connues']:>15} | {ligne['cle_unique_pourcent']:>9.1f}% | "
            f"{ligne['determinant_inversible_pourcent']:>21.1f}% | {ligne['candidats_moyens']:>16.2f}"
        )
    enregistrer_clair_connu(lignes_clair)

    print("\nCSV enregistré dans :", chemin)
    print("Graphiques PNG/SVG enregistrés dans projet/resultats/.")


if __name__ == "__main__":
    main()
