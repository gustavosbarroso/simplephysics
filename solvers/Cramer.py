#exemplo de sistema mecânico qualquer
def f(r, t):
    theta, omega, x, v = r

    F = A * np.cos(w * t)

    # matriz do sistema
    A_mat = np.array([
        [l, -np.cos(theta)],
        [-m*l*np.cos(theta), (M + m)]
    ])

    # vetor independente
    b_vec = np.array([
        -g * np.sin(theta) - (b/(m*l)) * omega,
        F - m*l*(omega**2)*np.sin(theta)
    ])

    # resolve sistema linear
    a_theta, a_x = np.linalg.solve(A_mat, b_vec)

    return np.array([omega, a_theta, v, a_x], float)
