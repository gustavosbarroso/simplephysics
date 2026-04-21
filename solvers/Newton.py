# ---------------------------
# IMPORTS
# ---------------------------
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------
# FUNÇÃO
# ---------------------------
def f(x):
    return x**4 - 2*x + 1

# ---------------------------
# DERIVADA (diferença finita progressiva)
# ---------------------------
def df(a, b, N, x):
    h = (b - a) / N
    return (f(x + h) - f(x)) / h

# ---------------------------
# MÉTODO DE NEWTON
# ---------------------------
def Newton(f, df, x0, a, b, N, tol=1e-6, max_iter=100):
    x = x0

    for i in range(max_iter):
        dfx = df(a, b, N, x)

        if abs(dfx) < 1e-12:  # evita divisão por zero
            print("Derivada muito pequena!")
            return None

        x_new = x - f(x)/dfx

        if abs(x_new - x) < tol:
            print(f"Convergiu em {i+1} iterações")
            return x_new

        x = x_new

    print("Não convergiu")
    return x

# ---------------------------
# EXECUÇÃO
# ---------------------------
a = -2
b = 2
N = 1000  # controla o h
x0 = 0.5

raiz = Newton(f, df, x0, a, b, N)
print("Raiz aproximada:", raiz)
