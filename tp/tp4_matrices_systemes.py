"""TP4 - Matrices et resolution de systemes."""


def transposee(A):
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def produit(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Les dimensions ne correspondent pas.")
    resultat = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                resultat[i][j] += A[i][k] * B[k][j]
    return resultat


def produit_vecteur(A, x):
    resultat = []
    for ligne in A:
        total = 0
        for j in range(len(x)):
            total += ligne[j] * x[j]
        resultat.append(total)
    return resultat


def resoudre(A, b, tolerance=1e-14):
    n = len(A)
    M = [list(map(float, A[i])) + [float(b[i])] for i in range(n)]

    for k in range(n):
        # On choisit le plus grand pivot de la colonne.
        pivot = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[pivot][k]) < tolerance:
            raise ValueError("Le systeme n'a pas de solution unique.")
        M[k], M[pivot] = M[pivot], M[k]

        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k, n + 1):
                M[i][j] -= facteur * M[k][j]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        total = M[i][n]
        for j in range(i + 1, n):
            total -= M[i][j] * x[j]
        x[i] = total / M[i][i]
    return x


def norme_residu(A, b, x):
    obtenu = produit_vecteur(A, x)
    return max(abs(obtenu[i] - b[i]) for i in range(len(b)))


def rotation(angle):
    import math
    import numpy as np

    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, -s], [s, c]])


def matrice_hilbert(n):
    import numpy as np
    return np.array([[1 / (i + j + 1) for j in range(n)] for i in range(n)])


def determinant(A):
    # On reprend l'elimination de Gauss et on multiplie les pivots.
    M = [list(map(float, ligne)) for ligne in A]
    n = len(M)
    det = 1
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(M[i][k]))
        if abs(M[pivot][k]) < 1e-14:
            return 0
        if pivot != k:
            M[k], M[pivot] = M[pivot], M[k]
            det *= -1
        det *= M[k][k]
        for i in range(k + 1, n):
            facteur = M[i][k] / M[k][k]
            for j in range(k + 1, n):
                M[i][j] -= facteur * M[k][j]
    return det


if __name__ == "__main__":
    A = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
    b = [2, -1, 8]
    x = resoudre(A, b)
    print("Transposee :", transposee([[1, 2, 3], [4, 5, 6]]))
    print("A x identite :", produit(A, [[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == A)
    print("Solution :", x)
    print("Verification :", produit_vecteur(A, x))
    print("Erreur :", norme_residu(A, b, x))
