import unittest

from projet.fonctions import (
    f_racine, df_racine, f_cycle, df_cycle,
    f_cosinus, df_cosinus, f_racine_double, df_racine_double,
)
from projet.methodes import dichotomie, newton, hybride


class TestMethodes(unittest.TestCase):
    def test_dichotomie(self):
        r = dichotomie(f_racine, 1, 2)
        self.assertTrue(r["succes"])
        self.assertLess(abs(r["racine"] ** 2 - 2), 1e-8)

    def test_newton(self):
        r = newton(f_racine, df_racine, 1.5)
        self.assertTrue(r["succes"])
        self.assertLess(abs(r["racine"] ** 2 - 2), 1e-8)

    def test_newton_cycle(self):
        r = newton(f_cycle, df_cycle, 0)
        self.assertFalse(r["succes"])
        self.assertIn("Cycle", r["raison"])

    def test_hybride_recupere_cycle(self):
        r = hybride(f_cycle, df_cycle, -2, 0, 0)
        self.assertTrue(r["succes"], r["raison"])
        self.assertLess(abs(f_cycle(r["racine"])), 1e-8)
        self.assertGreater(r["pas_dichotomie"], 0)

    def test_cosinus(self):
        r = hybride(f_cosinus, df_cosinus, 0, 1, 0.5)
        self.assertTrue(r["succes"])
        self.assertLess(abs(f_cosinus(r["racine"])), 1e-8)

    def test_racine_double_et_limite_dichotomie(self):
        r = newton(f_racine_double, df_racine_double, 1.5)
        self.assertTrue(r["succes"])
        self.assertAlmostEqual(r["racine"], 1, places=4)
        with self.assertRaises(ValueError):
            dichotomie(f_racine_double, 0, 2)


if __name__ == "__main__":
    unittest.main()
