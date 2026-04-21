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
# MÉTODO DAS SECANTES
# ---------------------------
def secantes(f, x0, x1, tol=1e-6, max_iter=50):
    xs = [x0, x1]  # histórico

    for i in range(max_iter):
        if abs(f(x1) - f(x0)) < 1e-12:
            print("Divisão por zero!")
            return None, xs

        x_new = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))
        xs.append(x_new)

        if abs(x_new - x1) < tol:
            print(f"Convergiu em {i+1} iterações")
            return x_new, xs

        # atualização correta
        x0, x1 = x1, x_new

    print("Não convergiu dentro do número máximo de iterações")
    return x1, xs
raiz, xs = secantes(f, -10, -3)
print("Raiz aproximada:", raiz)
