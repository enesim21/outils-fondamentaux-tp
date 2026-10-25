import math
import sys
from fractions import Fraction


def division_euclidienne(n, d):
    if d == 0:
        raise ValueError("Le diviseur ne peut pas etre nul.")
    return n // d, n % d


def dernier_chiffre(n):
    return abs(n) % 10


def sans_dernier_chiffre(n):
    return n // 10


def nombre_de_chiffres(n):
    n = abs(n)
    compte = 1
    while n >= 10:
        n //= 10
        compte += 1
    return compte


def table_de_sept():
    return [f"7 x {i} = {7 * i}" for i in range(1, 11)]


def somme_1_a_n(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def heron(a, tolerance=1e-12):
    if a < 0:
        raise ValueError("a doit etre positif.")
    if a == 0:
        return 0.0

    x = float(a)
    while True:
        suivant = (x + a / x) / 2
        if abs(suivant - x) < tolerance * abs(suivant):
            return suivant
        x = suivant


def vers_binaire(n):
    if n < 0:
        raise ValueError("Le nombre doit etre positif.")
    if n == 0:
        return "0"

    resultat = ""
    while n > 0:
        resultat = str(n % 2) + resultat
        n //= 2
    return resultat


def epsilon_machine():
    epsilon = 1.0
    while 1 + epsilon / 2 != 1:
        epsilon /= 2
    return epsilon


def racines_naives(a, b, c):
    delta = b * b - 4 * a * c
    if a == 0 or delta < 0:
        raise ValueError("Cette equation n'a pas deux racines reelles.")
    racine = math.sqrt(delta)
    return (-b - racine) / (2 * a), (-b + racine) / (2 * a)


def racines_stables(a, b, c):
    # Formule plus stable.
    if a == 0:
        raise ValueError("a ne doit pas etre nul.")
    delta = b * b - 4 * a * c
    if delta < 0:
        raise ValueError("Pas de racines reelles.")
    if delta == 0:
        racine = -b / (2 * a)
        return racine, racine

    racine_delta = math.sqrt(delta)
    q = -0.5 * (b + math.copysign(racine_delta, b))
    if q == 0:
        racine = -b / (2 * a)
        return racine, racine
    r1 = q / a
    r2 = c / q
    return min(r1, r2), max(r1, r2)


def somme_dixiemes_exacte(nombre_termes=1000):
    total = Fraction(0)
    for _ in range(nombre_termes):
        total += Fraction(1, 10)
    return total


def diagnostic_flottants():
    return {
        "0.1 + 0.2 == 0.3": 0.1 + 0.2 == 0.3,
        "epsilon calcule": epsilon_machine(),
        "epsilon Python": sys.float_info.epsilon,
        "0.1 exact": Fraction(0.1),
        "1000 dixiemes": somme_dixiemes_exacte(),
    }


if __name__ == "__main__":
    n, d = 2026, 7
    q, r = division_euclidienne(n, d)
    print("Quotient et reste :", q, r)
    print("Verification :", q * d + r == n)
    print("Nombre de chiffres de 10**60 :", nombre_de_chiffres(10**60))
    print("Racine de 2 :", heron(2), math.sqrt(2))
    print("37 en binaire :", vers_binaire(37))
    print("Flottants :", diagnostic_flottants())
    print("Racines classiques :", racines_naives(1, -1e8, 1))
    print("Racines stables :", racines_stables(1, -1e8, 1))
