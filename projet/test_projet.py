import unittest

from projet.chiffrement import chiffrer, dechiffrer, cles_valides, inverse_modulaire
from projet.attaque import attaque_force_brute, attaque_frequences, rang_cle
from projet.experiences import lancer_experiences


class TestChiffrement(unittest.TestCase):
    def test_nombre_de_cles(self):
        self.assertEqual(len(cles_valides()) * 26, 312)

    def test_chiffrer_dechiffrer(self):
        texte = "Bonjour, le message est secret !"
        secret = chiffrer(texte, 5, 8)
        self.assertEqual(dechiffrer(secret, 5, 8), texte.upper())

    def test_accents(self):
        self.assertEqual(chiffrer("Été à Noël", 5, 8), chiffrer("Ete a Noel", 5, 8))

    def test_cle_invalide(self):
        with self.assertRaises(ValueError):
            chiffrer("SALUT", 2, 4)

    def test_inverse_modulaire(self):
        for a in cles_valides():
            self.assertEqual((a * inverse_modulaire(a)) % 26, 1)

    def test_force_brute_trouve_la_cle(self):
        secret = chiffrer("LE MESSAGE SECRET EST CACHE DANS LE TEXTE", 5, 8)
        candidats = attaque_force_brute(secret)
        self.assertEqual(len(candidats), 312)
        self.assertIsNotNone(rang_cle(candidats, 5, 8))

    def test_frequences_sur_un_texte_plus_long(self):
        resultats = lancer_experiences()
        longs = [r for r in resultats
                 if r["longueur"] == 150 and r["rang_frequences"] == 1]
        self.assertEqual(len(longs), 3)

    def test_frequences_reduit_les_candidats(self):
        secret = chiffrer("CE MESSAGE FRANCAIS EST ASSEZ LONG POUR UNE ANALYSE DE FREQUENCES", 5, 8)
        candidats = attaque_frequences(secret)
        self.assertEqual(len(candidats), 12)


if __name__ == "__main__":
    unittest.main()
