"""TP6 - Quelques calculs de geometrie dans le plan."""

import math
import random


def vecteur(A, B):
    return B[0] - A[0], B[1] - A[1]


def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]


def norme(u):
    return math.sqrt(produit_scalaire(u, u))


def angle(u, v):
    denominateur = norme(u) * norme(v)
    if denominateur == 0:
        raise ValueError("Un vecteur nul n'a pas d'angle.")
    cosinus = produit_scalaire(u, v) / denominateur
    # On corrige un petit depassement possible a cause des arrondis.
    cosinus = max(-1, min(1, cosinus))
    return math.degrees(math.acos(cosinus))


def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def distance_point_droite(P, A, B):
    AB = vecteur(A, B)
    AP = vecteur(A, P)
    longueur = norme(AB)
    if longueur == 0:
        raise ValueError("A et B doivent etre differents.")
    return abs(determinant(AB, AP)) / longueur


def orientation(A, B, C, tolerance=1e-12):
    valeur = determinant(vecteur(A, B), vecteur(A, C))
    if abs(valeur) < tolerance:
        return 0
    if valeur > 0:
        return 1
    return -1


def aire(polygone):
    if len(polygone) < 3:
        return 0
    total = 0
    for i in range(len(polygone)):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % len(polygone)]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def se_coupent(A, B, C, D):
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)
    return o1 * o2 < 0 and o3 * o4 < 0


def intersection(A, B, C, D, tolerance=1e-12):
    AB = vecteur(A, B)
    CD = vecteur(C, D)
    AC = vecteur(A, C)
    denominateur = determinant(AB, CD)
    if abs(denominateur) < tolerance:
        return None

    t = determinant(AC, CD) / denominateur
    u = determinant(AC, AB) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return A[0] + t * AB[0], A[1] + t * AB[1]
    return None


def dedans(P, polygone):
    x, y = P
    interieur = False
    n = len(polygone)
    for i in range(n):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < croisement:
                interieur = not interieur
    return interieur


def zone_de(P, zones):
    for i in range(len(zones)):
        if dedans(P, zones[i]):
            return i
    return None


def aire_monte_carlo(polygone, tirages=200000, graine=0):
    if len(polygone) == 0:
        return 0
    xs = [p[0] for p in polygone]
    ys = [p[1] for p in polygone]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    aire_rectangle = (xmax - xmin) * (ymax - ymin)
    if aire_rectangle == 0:
        return 0

    hasard = random.Random(graine)
    dedans_compte = 0
    for _ in range(tirages):
        P = (hasard.uniform(xmin, xmax), hasard.uniform(ymin, ymax))
        if dedans(P, polygone):
            dedans_compte += 1
    return aire_rectangle * dedans_compte / tirages


def tracer_polygone(polygone, points=()):
    import matplotlib.pyplot as plt

    xs = [p[0] for p in polygone] + [polygone[0][0]]
    ys = [p[1] for p in polygone] + [polygone[0][1]]
    plt.plot(xs, ys)
    for x, y in points:
        plt.scatter(x, y)
    plt.axis("equal")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
    print("Vecteur AB :", vecteur((1, 2), (4, 6)))
    print("Angle :", angle((1, 0), (1, 1)))
    print("Distance :", distance_point_droite((0, 0), (0, 1), (1, 0)))
    print("Aire de la maison :", aire(maison))
    print("A l'interieur ?", dedans((1, 1), maison))
    print("Aire estimee :", aire_monte_carlo(maison, 20000))
