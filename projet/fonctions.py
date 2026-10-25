import math


def f_racine(x):
    return x * x - 2


def df_racine(x):
    return 2 * x


def f_cosinus(x):
    return math.cos(x) - x


def df_cosinus(x):
    return -math.sin(x) - 1


def f_cycle(x):
    return x**3 - 2 * x + 2


def df_cycle(x):
    return 3 * x * x - 2


def f_racine_double(x):
    return (x - 1) ** 2


def df_racine_double(x):
    return 2 * (x - 1)


CAS = {
    "racine_de_2": {
        "f": f_racine, "df": df_racine,
        "a": 1, "b": 2, "x0": 1.5,
    },
    "cosinus": {
        "f": f_cosinus, "df": df_cosinus,
        "a": 0, "b": 1, "x0": 0.5,
    },
    "cycle_de_newton": {
        "f": f_cycle, "df": df_cycle,
        "a": -2, "b": 0, "x0": 0,
    },
    "racine_double": {
        "f": f_racine_double, "df": df_racine_double,
        "a": 0, "b": 2, "x0": 1.5,
    },
}
