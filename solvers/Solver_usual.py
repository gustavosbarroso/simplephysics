# ===========================
# RK4 (GENÉRICO)
# ===========================
def RK4(f, a, b, N, r0, params):
    h = (b - a) / N
    tp = np.linspace(a, b, N + 1)
    r = np.array(r0, float)

    x_list, v_list = [r[0]], [r[1]]

    for i in range(N):
        t = tp[i]

        k1 = h * f(r, t, params)
        k2 = h * f(r + 0.5*k1, t + 0.5*h, params)
        k3 = h * f(r + 0.5*k2, t + 0.5*h, params)
        k4 = h * f(r + k3, t + h, params)

        r = r + (k1 + 2*k2 + 2*k3 + k4)/6

        x_list.append(r[0])
        v_list.append(r[1])

    return tp, np.array(x_list), np.array(v_list)

# ===========================
# SOLVER CENTRAL
# ===========================
def solve(params):
    tp, x, v = RK4(
        f,
        0, 10, 500,
        [params["x0"], params["v0"]],
        params
    )

    return tp, x, v

# ===========================
# ESCALA DO SISTEMA
# ===========================
def update_axis():
    ax_sys.set_xlim(-2, 2)
    ax_sys.set_ylim(-2, 2)

# ===========================
# INICIALIZAÇÃO
# ===========================
tp, x, v = solve(params)

# ===========================
# FIGURA
# ===========================
fig, (ax_sys, ax_plot) = plt.subplots(1, 2, figsize=(12,5))
plt.subplots_adjust(left=0.25, bottom=0.35)

update_axis()

ax_sys.set_title("Sistema físico")

point, = ax_sys.plot([], [], 'o')

# ---------------------------
# GRÁFICO
# ---------------------------
ax_plot.set_xlim(0, tp[-1])
ax_plot.set_title("Evolução temporal")

line_x, = ax_plot.plot([], [], label="x(t)")
line_v, = ax_plot.plot([], [], label="v(t)")
ax_plot.legend()
