import math


def evaluer_naif(P, x):
    total = 0
    for i in range(len(P)):
        total += P[i] * x**i
    return total


def evaluer(P, x):
    # Methode de Horner.
    total = 0
    for coefficient in reversed(P):
        total = total * x + coefficient
    return total


def deriver(P):
    resultat = []
    for i in range(1, len(P)):
        resultat.append(i * P[i])
    return resultat


def dichotomie(f, a, b, tolerance=1e-12):
    fa = f(a)
    fb = f(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError("Il faut un changement de signe entre a et b.")

    while b - a > tolerance:
        milieu = (a + b) / 2
        fm = f(milieu)
        if fm == 0:
            return milieu
        if fa * fm < 0:
            b, fb = milieu, fm
        else:
            a, fa = milieu, fm
    return (a + b) / 2


def newton(P, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(P)
    x = float(depart)
    for tour in range(tours_max):
        valeur = evaluer(P, x)
        pente = evaluer(derivee, x)
        if abs(valeur) < tolerance:
            return x, tour
        if abs(pente) < 1e-15:
            raise ZeroDivisionError("La derivee est trop proche de zero.")
        suivant = x - valeur / pente
        if abs(suivant - x) < tolerance * max(1, abs(suivant)):
            return suivant, tour + 1
        x = suivant
    raise RuntimeError("Newton n'a pas converge.")


def somme(P, Q):
    taille = max(len(P), len(Q))
    resultat = []
    for i in range(taille):
        a = P[i] if i < len(P) else 0
        b = Q[i] if i < len(Q) else 0
        resultat.append(a + b)
    return resultat


def produit_poly(P, Q):
    if not P or not Q:
        return []
    resultat = [0] * (len(P) + len(Q) - 1)
    for i in range(len(P)):
        for j in range(len(Q)):
            resultat[i + j] += P[i] * Q[j]
    return resultat


def rectangles(f, a, b, n):
    pas = (b - a) / n
    total = 0
    for i in range(n):
        total += f(a + i * pas)
    return total * pas


def trapezes(f, a, b, n):
    pas = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total += f(a + i * pas)
    return total * pas


def simpson(f, a, b, n):
    # n doit etre pair.
    if n % 2 != 0:
        n += 1
    pas = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        total += (4 if i % 2 else 2) * f(a + i * pas)
    return total * pas / 3


def integrer_trapezes(f, a, b, n):
    return trapezes(f, a, b, n)


def derivee_numerique(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)


def tracer_fonction(f, a, b, nombre=200):
    import matplotlib.pyplot as plt

    xs = [a + (b - a) * i / (nombre - 1) for i in range(nombre)]
    ys = [f(x) for x in xs]
    plt.plot(xs, ys)
    plt.axhline(0, linewidth=0.8)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    P = [2, 3, 0, 5]
    print("P(2), methode naive :", evaluer_naif(P, 2))
    print("P(2), Horner :", evaluer(P, 2))
    print("Derivee :", deriver(P))
    print("Racine de x^2 - 2 :", dichotomie(lambda x: x * x - 2, 0, 2))
    print("Newton :", newton([-5, -2, 0, 1], 2))
    print("(1 + x)^2 :", produit_poly([1, 1], [1, 1]))
    print("Integrale de x^2 :", simpson(lambda x: x * x, 0, 1, 100))
