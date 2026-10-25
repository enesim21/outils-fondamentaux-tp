
def diviseurs(n):
    resultat = []
    for d in range(1, n + 1):
        if n % d == 0:
            resultat.append(d)
    return resultat


def est_parfait(n):
    somme = 0
    for d in range(1, n):
        if n % d == 0:
            somme += d
    return n > 1 and somme == n


def pgcd_naif(a, b):
    a, b = abs(a), abs(b)
    meilleur = 0
    for d in range(1, min(a, b) + 1):
        if a % d == 0 and b % d == 0:
            meilleur = d
    return meilleur


def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def est_premier_naif(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def est_premier(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def crible(limite):
    if limite < 2:
        return []
    premiers = [True] * (limite + 1)
    premiers[0] = premiers[1] = False
    d = 2
    while d * d <= limite:
        if premiers[d]:
            for multiple in range(d * d, limite + 1, d):
                premiers[multiple] = False
        d += 1
    return [n for n in range(2, limite + 1) if premiers[n]]


def facteurs(n):
    if n < 1:
        raise ValueError("n doit etre positif.")
    resultat = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            resultat.append(d)
            n //= d
        d += 1
    if n > 1:
        resultat.append(n)
    return resultat


def fibonacci_recursif(n):
    if n < 0:
        raise ValueError("n doit etre positif ou nul.")
    if n < 2:
        return n
    return fibonacci_recursif(n - 1) + fibonacci_recursif(n - 2)


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def euclide_etendu(a, b):
    if b == 0:
        return abs(a), (1 if a >= 0 else -1), 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v


def puissance_modulaire(base, exposant, modulo):
    resultat = 1
    base %= modulo
    while exposant > 0:
        if exposant % 2 == 1:
            resultat = resultat * base % modulo
        base = base * base % modulo
        exposant //= 2
    return resultat % modulo


if __name__ == "__main__":
    print("Diviseurs de 28 :", diviseurs(28))
    print("PGCD :", pgcd(1071, 462), pgcd_naif(1071, 462))
    print("Premiers jusqu'a 30 :", crible(30))
    print("Facteurs de 756 :", facteurs(756))
    print("Fibonacci(10) :", fibonacci(10), fibonacci_recursif(10))
    print("Euclide etendu :", euclide_etendu(1071, 462))
    print("5 puissance 117 modulo 19 :", puissance_modulaire(5, 117, 19))
