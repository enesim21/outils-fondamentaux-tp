from projet.chiffrement import chiffrer, dechiffrer
from projet.attaque import attaque_force_brute, attaque_frequences, rang_cle
from projet.experiences import lancer_experiences, enregistrer
from projet.graphique import creer_graphiques


def main():
    message = "LE CODE SECRET EST CACHE DANS CE MESSAGE"
    a, b = 5, 8
    secret = chiffrer(message, a, b)

    print("Message :", message)
    print("Message chiffre :", secret)
    print("Message dechiffre :", dechiffrer(secret, a, b))
    print("\nNombre de cles valides : 312")

    brute = attaque_force_brute(secret)
    frequence = attaque_frequences(secret)
    print("Candidats par force brute :", len(brute))
    print("Candidats par frequences :", len(frequence))
    print("Rang de la cle en force brute :", rang_cle(brute, a, b))
    print("Rang de la cle par frequences :", rang_cle(frequence, a, b))

    lignes = lancer_experiences()
    chemin = enregistrer(lignes)
    creer_graphiques(lignes)
    print("\nExperiences enregistrees dans :", chemin)
    print("Graphiques enregistres dans projet/resultats/")


if __name__ == "__main__":
    main()
