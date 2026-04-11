import numpy as np

def mass_chain_system(r, t, N, k, m):
    x = r[:N]
    v = r[N:]

    a = np.zeros(N)

    for i in range(N):
        if i == 0:
            a[i] = (k/m)*(x[i+1] - x[i])
        elif i == N-1:
            a[i] = (k/m)*(x[i-1] - x[i])
        else:
            a[i] = (k/m)*(x[i+1] + x[i-1] - 2*x[i])

    return np.concatenate([v, a])
