import unittest
from collections import Counter

from projet.chiffrement import chiffrer, dechiffrer, cles_valides, inverse_modulaire
from projet.attaque import (
    FREQUENCES_FR_NORMALISEES, attaque_force_brute, attaque_frequences, rang_cle, lettres
)
from projet.experiences import lancer_experiences


class TestChiffrement(unittest.TestCase):
    def test_nombre_de_cles(self):
        self.assertEqual(len(cles_valides()) * 26, 312)


    def test_frequences_fr_normalisees(self):
        self.assertAlmostEqual(sum(FREQUENCES_FR_NORMALISEES.values()), 1.0)

    def test_chiffrer_dechiffrer_conserve_espaces(self):
        texte = "Bonjour, le message est secret !"
        secret = chiffrer(texte, 5, 8)
        self.assertEqual(dechiffrer(secret, 5, 8), texte.upper())
        self.assertEqual(len(secret), len(texte))

    def test_accents(self):
        self.assertEqual(chiffrer("Été à Noël", 5, 8), chiffrer("Ete a Noel", 5, 8))

    def test_a_invalide(self):
        for a in (2, 13, 0, 26, 5.0, True):
            with self.subTest(a=a):
                with self.assertRaises(ValueError):
                    chiffrer("SALUT", a, 4)
                with self.assertRaises(ValueError):
                    dechiffrer("SALUT", a, 4)

    def test_b_invalide(self):
        for b in (-1, 26, 2.5, "4"):
            with self.subTest(b=b):
                with self.assertRaises(ValueError):
                    chiffrer("SALUT", 5, b)
                with self.assertRaises(ValueError):
                    dechiffrer("SALUT", 5, b)

    def test_inverse_modulaire(self):
        for a in cles_valides():
            self.assertEqual((a * inverse_modulaire(a)) % 26, 1)
        with self.assertRaises(ValueError):
            inverse_modulaire(2)

    def test_force_brute_classe_la_cle_en_premier(self):
        texte = (
            "Quand on apprend la programmation, on avance en faisant des essais, "
            "en lisant les erreurs et en corrigeant peu a peu son raisonnement. "
            "Un programme utile doit expliquer comment la reponse a ete obtenue. "
        ) * 8
        secret = chiffrer(texte, 5, 8)
        candidats = attaque_force_brute(secret)
        self.assertEqual(len(candidats), 312)
        self.assertEqual(rang_cle(candidats, 5, 8), 1)

    def test_nombre_de_candidats_selon_k(self):
        secret = chiffrer("ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2, 5, 8)
        for k, attendu in ((1, 12), (2, 24), (3, 36), (5, 60)):
            with self.subTest(k=k):
                self.assertEqual(len(attaque_frequences(secret, k=k)), attendu)

    def test_frequences_k1_echoue_et_k3_classe_la_cle_premiere(self):
        clair = (
            "Les habitants partagent des habitudes, mais ils n'utilisent pas tous "
            "les mêmes itinéraires ni les mêmes services."
        )
        comptes = Counter(lettres(clair))
        # Dans cette phrase, S apparaît 16 fois et E 15 fois.
        self.assertEqual(comptes["S"], 16)
        self.assertEqual(comptes["E"], 15)
        secret = chiffrer(clair, 5, 8)
        candidats_k1 = attaque_frequences(secret, k=1)
        candidats_k3 = attaque_frequences(secret, k=3)
        self.assertIsNone(rang_cle(candidats_k1, 5, 8))
        self.assertEqual(rang_cle(candidats_k3, 5, 8), 1)

    def test_parametre_k_invalide(self):
        for k in (0, 4, 6, 1.0, "3"):
            with self.subTest(k=k):
                with self.assertRaises(ValueError):
                    attaque_frequences("MESSAGE", k=k)

    def test_experience_courte_sans_lancer_toute_la_serie(self):
        lignes = lancer_experiences(nombre_essais=1, graine=12, longueurs=[20])
        self.assertEqual(len(lignes), 1)
        self.assertEqual(lignes[0]["longueur_lettres"], 20)
        self.assertEqual(lignes[0]["brute_nb_cles"], 312)
        self.assertEqual(lignes[0]["k1_nb_cles"], 12)
        self.assertEqual(lignes[0]["k3_nb_cles"], 36)
        self.assertIn("brute_rang1", lignes[0])
        self.assertIn("k3_cle_presente", lignes[0])


if __name__ == "__main__":
    unittest.main()
