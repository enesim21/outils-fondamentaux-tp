import csv
import random
from pathlib import Path

from projet.attaque import (
    K_AUTORISES,
    attaque_force_brute,
    attaque_frequences,
    rang_cle,
)
from projet.chiffrement import ALPHABET, chiffrer, cles_valides, nettoyer

# Cinq paragraphes français assez longs pour tirer des fenêtres de 280 lettres.
TEXTES_FRANCAIS = (
    ("apprentissage", """Quand on apprend la programmation, on avance en faisant des essais, en lisant les erreurs et en corrigeant peu à peu son raisonnement. Un programme utile ne se limite pas à produire une réponse : il doit aussi permettre de comprendre comment cette réponse a été obtenue. En informatique, on compare parfois plusieurs méthodes sur les mêmes données, puis on note précisément les conditions de l'expérience. Cette démarche évite de confondre une impression avec un résultat mesuré. Elle aide également à repérer les limites d'un algorithme, notamment lorsque les données sont courtes, incomplètes ou peu représentatives. La clarté du code compte autant que le résultat final, car une autre personne doit pouvoir le relire, le tester et proposer des améliorations."""),
    ("ville", """Dans une ville, les rues changent de rythme au fil de la journée. Le matin, les bus se remplissent, les commerces ouvrent et les étudiants rejoignent leurs salles de cours. Plus tard, les places deviennent des lieux de rencontre, tandis que les bibliothèques offrent un espace calme pour lire ou travailler. Les habitants partagent des habitudes, mais ils n'utilisent pas tous les mêmes itinéraires ni les mêmes services. Pour comprendre la vie urbaine, il faut donc observer plusieurs quartiers et tenir compte des différences entre les horaires, les saisons et les besoins. Un exemple isolé peut être intéressant, sans suffire à décrire toute une ville."""),
    ("nature", """Au début du printemps, les journées s'allongent et les changements deviennent visibles dans les jardins et les forêts. Les premières feuilles apparaissent, les oiseaux reprennent leurs chants et la pluie transforme parfois les chemins en terrain boueux. La météo varie d'une semaine à l'autre, si bien qu'une observation unique ne permet pas de décrire toute une saison. Les naturalistes prennent des notes régulières, comparent les lieux et indiquent les conditions dans lesquelles ils ont effectué leurs mesures. Cette méthode rend les observations plus faciles à vérifier. Elle rappelle qu'un résultat dépend à la fois du phénomène étudié, de la qualité des données et de la manière dont celles-ci ont été recueillies."""),
    ("lecture", """Lire un livre demande du temps et de l'attention, mais cette activité peut aussi devenir une source de plaisir. Certains lecteurs préfèrent les récits d'aventure, d'autres recherchent des explications scientifiques ou des histoires proches de leur quotidien. Une bibliothèque rassemble des ouvrages très différents et permet de découvrir des auteurs que l'on ne connaissait pas. Prendre quelques notes après la lecture aide à retenir les idées principales, à comparer les personnages et à repérer les questions que le texte soulève. La compréhension dépend aussi du vocabulaire, de l'expérience du lecteur et du contexte dans lequel le livre a été écrit. Discuter d'un ouvrage avec d'autres personnes permet parfois de voir un détail qui nous avait échappé."""),
    ("voyage", """Préparer un voyage consiste à choisir une destination, organiser les déplacements et prévoir un budget raisonnable. Pourtant, il reste toujours une part d'imprévu : un train peut être en retard, la météo peut changer ou un musée peut fermer exceptionnellement. Il est utile de vérifier les horaires avant le départ, de conserver les informations importantes et de garder du temps libre pour se promener. Découvrir une région ne se résume pas à visiter les lieux les plus connus. On peut aussi observer l'architecture, goûter les spécialités locales ou discuter avec les personnes qui y vivent. Un carnet de voyage aide à garder une trace des étapes et des impressions, mais il ne remplace pas l'expérience vécue sur place."""),
)

LONGUEURS_LETTRES = (20, 30, 50, 80, 150, 280)
ESSAIS_PAR_LONGUEUR = 300
GRAINE_DEFAUT = 20261025


def _fenetre_aleatoire(texte, longueur, generateur):
    texte = nettoyer(texte)
    positions = [index for index, caractere in enumerate(texte) if caractere in ALPHABET]
    if len(positions) < longueur:
        raise ValueError("Le texte est trop court pour cette longueur.")
    debut = generateur.randrange(len(positions) - longueur + 1)
    position_debut = positions[debut]
    position_fin = positions[debut + longueur - 1] + 1
    # La fenêtre contient exactement 'longueur' lettres ; espaces et ponctuation restent.
    return texte[position_debut:position_fin]


def lancer_experiences(nombre_essais=ESSAIS_PAR_LONGUEUR, graine=GRAINE_DEFAUT, longueurs=None):
    if type(nombre_essais) is not int or nombre_essais < 1:
        raise ValueError("nombre_essais doit etre un entier positif.")
    if longueurs is None:
        longueurs = LONGUEURS_LETTRES
    if not longueurs or any(type(n) is not int or n < 1 for n in longueurs):
        raise ValueError("longueurs doit contenir des entiers positifs.")

    generateur = random.Random(graine)
    valeurs_a = cles_valides()
    lignes = []

    for longueur in longueurs:
        for numero_essai in range(1, nombre_essais + 1):
            nom_texte, texte_source = generateur.choice(TEXTES_FRANCAIS)
            clair = _fenetre_aleatoire(texte_source, longueur, generateur)
            # Tirage uniforme : 12 valeurs possibles pour a et 26 pour b, soit 312 clés.
            a = generateur.choice(valeurs_a)
            b = generateur.randrange(26)
            secret = chiffrer(clair, a, b)

            brute = attaque_force_brute(secret)
            rang_brute = rang_cle(brute, a, b)
            ligne = {
                "longueur_lettres": longueur,
                "essai": numero_essai,
                "texte_source": nom_texte,
                "cle_a": a,
                "cle_b": b,
                "brute_nb_cles": len(brute),
                "brute_cle_presente": rang_brute is not None,
                "brute_rang_chi2": rang_brute if rang_brute is not None else "",
                "brute_rang1": rang_brute == 1,
            }
            for k in K_AUTORISES:
                candidats = attaque_frequences(secret, k)
                rang = rang_cle(candidats, a, b)
                ligne[f"k{k}_nb_cles"] = len(candidats)
                ligne[f"k{k}_cle_presente"] = rang is not None
                ligne[f"k{k}_rang_chi2"] = rang if rang is not None else ""
                ligne[f"k{k}_rang1"] = rang == 1
            lignes.append(ligne)
    return lignes


def enregistrer(lignes, chemin=None):
    if not lignes:
        raise ValueError("Aucun resultat a enregistrer.")
    if chemin is None:
        chemin = Path(__file__).resolve().parent / "resultats" / "experiences.csv"
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=list(lignes[0].keys()))
        writer.writeheader()
        writer.writerows(lignes)
    return chemin
