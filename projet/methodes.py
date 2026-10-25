import math


def _resultat(nom, x, iterations, nb_f, nb_df, fonction, succes, raison,
              pas_newton=0, pas_dicho=0):
    try:
        erreur = abs(fonction(x)) if x is not None else math.inf
        nb_f += 1 if x is not None else 0
    except (ValueError, OverflowError, ZeroDivisionError):
        erreur = math.inf

    return {
        "methode": nom,
        "racine": x,
        "iterations": iterations,
        "evaluations_f": nb_f,
        "evaluations_df": nb_df,
        "erreur": erreur,
        "succes": succes,
        "raison": raison,
        "pas_newton": pas_newton,
        "pas_dichotomie": pas_dicho,
    }


def dichotomie(f, a, b, tolerance=1e-10, max_iter=1000):
    if tolerance <= 0 or max_iter < 1 or a >= b:
        raise ValueError("Parametres invalides.")

    fa = f(a)
    fb = f(b)
    nb_f = 2

    if fa == 0:
        return _resultat("Dichotomie", a, 0, nb_f, 0, f, True, "Racine a gauche.")
    if fb == 0:
        return _resultat("Dichotomie", b, 0, nb_f, 0, f, True, "Racine a droite.")
    if (fa > 0) == (fb > 0):
        raise ValueError("L'intervalle doit contenir un changement de signe.")

    for i in range(1, max_iter + 1):
        milieu = (a + b) / 2
        fm = f(milieu)
        nb_f += 1

        if not math.isfinite(fm):
            return _resultat("Dichotomie", milieu, i, nb_f, 0, f, False,
                             "Valeur non finie.", pas_dicho=i)
        if abs(fm) <= tolerance:
            return _resultat("Dichotomie", milieu, i, nb_f, 0, f, True,
                             "Precision atteinte.", pas_dicho=i)

        if (fa > 0) != (fm > 0):
            b, fb = milieu, fm
        else:
            a, fa = milieu, fm

        if b - a <= tolerance:
            racine = (a + b) / 2
            return _resultat("Dichotomie", racine, i, nb_f, 0, f, True,
                             "Intervalle assez petit.", pas_dicho=i)

    racine = (a + b) / 2
    return _resultat("Dichotomie", racine, max_iter, nb_f, 0, f, False,
                     "Limite d'iterations atteinte.", pas_dicho=max_iter)


def newton(f, df, x0, tolerance=1e-10, max_iter=100):
    if tolerance <= 0 or max_iter < 1:
        raise ValueError("Parametres invalides.")

    x = float(x0)
    historique = [x]
    fx = f(x)
    nb_f = 1
    nb_df = 0

    if not math.isfinite(fx):
        return _resultat("Newton", x, 0, nb_f, nb_df, f, False, "Valeur non finie.")
    if abs(fx) <= tolerance:
        return _resultat("Newton", x, 0, nb_f, nb_df, f, True, "Precision atteinte.")

    for i in range(1, max_iter + 1):
        pente = df(x)
        nb_df += 1

        if not math.isfinite(pente) or abs(pente) < 1e-14:
            return _resultat("Newton", x, i - 1, nb_f, nb_df, f, False,
                             "Derivee trop proche de zero.", pas_newton=i - 1)

        suivant = x - fx / pente
        if not math.isfinite(suivant):
            return _resultat("Newton", x, i, nb_f, nb_df, f, False,
                             "Valeur non finie.", pas_newton=i)

        limite = tolerance * max(1.0, abs(suivant))
        if any(abs(suivant - ancien) <= limite for ancien in historique):
            return _resultat("Newton", suivant, i, nb_f, nb_df, f, False,
                             "Cycle detecte.", pas_newton=i)

        x = suivant
        historique.append(x)
        fx = f(x)
        nb_f += 1

        if not math.isfinite(fx):
            return _resultat("Newton", x, i, nb_f, nb_df, f, False,
                             "Valeur non finie.", pas_newton=i)
        if abs(fx) <= tolerance:
            return _resultat("Newton", x, i, nb_f, nb_df, f, True,
                             "Precision atteinte.", pas_newton=i)

    return _resultat("Newton", x, max_iter, nb_f, nb_df, f, False,
                     "Limite d'iterations atteinte.", pas_newton=max_iter)


def hybride(f, df, a, b, x0=None, tolerance=1e-10, max_iter=1000):
    if tolerance <= 0 or max_iter < 1 or a >= b:
        raise ValueError("Parametres invalides.")

    fa = f(a)
    fb = f(b)
    nb_f = 2
    nb_df = 0
    pas_newton = 0
    pas_dicho = 0

    if fa == 0:
        return _resultat("Hybride", a, 0, nb_f, nb_df, f, True, "Racine a gauche.")
    if fb == 0:
        return _resultat("Hybride", b, 0, nb_f, nb_df, f, True, "Racine a droite.")
    if (fa > 0) == (fb > 0):
        raise ValueError("L'intervalle doit contenir un changement de signe.")

    if x0 is None or not a < x0 < b:
        x = (a + b) / 2
    else:
        x = float(x0)

    fx = f(x)
    nb_f += 1

    for i in range(1, max_iter + 1):
        if not math.isfinite(fx):
            return _resultat("Hybride", x, i - 1, nb_f, nb_df, f, False,
                             "Valeur non finie.", pas_newton, pas_dicho)
        if abs(fx) <= tolerance:
            return _resultat("Hybride", x, i - 1, nb_f, nb_df, f, True,
                             "Precision atteinte.", pas_newton, pas_dicho)

        if (fa > 0) != (fx > 0):
            b, fb = x, fx
        else:
            a, fa = x, fx

        if b - a <= tolerance:
            racine = (a + b) / 2
            return _resultat("Hybride", racine, i - 1, nb_f, nb_df, f, True,
                             "Intervalle assez petit.", pas_newton, pas_dicho)

        pente = df(x)
        nb_df += 1
        suivant = None

        if math.isfinite(pente) and abs(pente) >= 1e-14:
            candidat = x - fx / pente
            if a < candidat < b and abs(candidat - x) > tolerance * max(1, abs(x)):
                suivant = candidat

        if suivant is None:
            suivant = (a + b) / 2
            pas_dicho += 1
        else:
            pas_newton += 1

        x = suivant
        fx = f(x)
        nb_f += 1

    return _resultat("Hybride", x, max_iter, nb_f, nb_df, f, False,
                     "Limite d'iterations atteinte.", pas_newton, pas_dicho)
