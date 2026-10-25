"""Quelques tests rapides pour les fonctions des TP."""

import math
from tp import tp1
from tp import tp2
from tp import tp3
from tp import tp4
from tp import tp5
from tp import tp6

# TP1
assert tp1.division_euclidienne(2026, 7) == (289, 3)
assert abs(tp1.heron(2) - math.sqrt(2)) < 1e-12
assert tp1.vers_binaire(37) == "100101"
assert abs(tp1.racines_stables(1, -1e8, 1)[0] - 1e-8) < 1e-12

# TP2
assert tp2.diviseurs(28) == [1, 2, 4, 7, 14, 28]
assert tp2.pgcd(1071, 462) == 21
assert tp2.facteurs(756) == [2, 2, 3, 3, 3, 7]
assert len(tp2.crible(100000)) == 9592
assert tp2.puissance_modulaire(5, 117, 19) == pow(5, 117, 19)

# TP3
P = [2, 3, 0, 5]
assert tp3.evaluer_naif(P, 2) == 48
assert tp3.evaluer(P, 2) == 48
assert tp3.deriver(P) == [3, 0, 15]
assert abs(tp3.dichotomie(lambda x: x*x - 2, 0, 2) - math.sqrt(2)) < 1e-10

# TP4
A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
b = [2, -1, 8]
x = tp4.resoudre(A, b)
assert max(abs(a - b) for a, b in zip(x, [3, -1, 0.5])) < 1e-10
assert tp4.transposee([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]

# TP5
message = tp5.nettoyer("Été, à Paris !")
secret = tp5.chiffrer(message, 5, 8)
assert message == "ETEAPARIS"
assert tp5.dechiffrer(secret, 5, 8) == message
assert len(tp5.toutes_les_cles(secret)) == 312
assert len(tp5.casser_par_frequences(secret)) == 12

# TP6
assert tp6.orientation((0, 0), (1, 0), (1, 1)) == 1
assert abs(tp6.aire([(0, 0), (1, 0), (1, 1), (0, 1)]) - 1) < 1e-12
assert tp6.dedans((1, 1), [(0, 0), (2, 0), (2, 2), (0, 2)])
assert tp6.intersection((0, 0), (2, 2), (0, 2), (2, 0)) == (1.0, 1.0)

print("Tous les tests sont OK.")
