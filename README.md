# 🔬 simplephysics

This repository contains numerical simulations of physical systems using the 4th-order Runge-Kutta (RK4) method and other numerical integrators, combined with interactive visualization.

The project explores a wide range of topics in physics through computational approaches, emphasizing both **numerical accuracy** and **physical interpretation**.

---

## ⚙️ Features

* Numerical integration of ordinary differential equations (ODEs)
* RK4 implementation for general dynamical systems
* Use of modern solvers (`solve_ivp`, SciPy)
* Simulation of nonlinear and coupled systems
* Real-time animation using matplotlib
* Interactive parameter control via sliders
* Visualization of system dynamics and trajectories

---

## 📦 Implemented Systems

### 1. Damped Pendulum and Simple Pendulum

Nonlinear pendulum with damping:

θ'' + (b/m)θ' + (g/L) sin(θ) = 0

Run:

```bash
python scripts/pendulo_amortecido.py
```

Simple pendulum (b = 0):

θ'' + (g/L) sin(θ) = 0

Run:

```bash
python scripts/Pendulo_simples.py
```

---

### 2. Double Pendulum (Chaotic System)

θ₁'' = [ -g(2m₁ + m₂)sin(θ₁) - m₂g sin(θ₁ - 2θ₂) - 2 sin(θ₁ - θ₂)m₂(θ₂'²L₂ + θ₁'²L₁cos(θ₁ - θ₂)) ] / [ L₁(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

θ₂'' = [ 2 sin(θ₁ - θ₂)(θ₁'²L₁(m₁ + m₂) + g(m₁ + m₂)cos(θ₁) + θ₂'²L₂m₂cos(θ₁ - θ₂)) ] / [ L₂(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

Run:

```bash
python scripts/Pendulo_duplo.py
```

---

### 3. Coupled Mass-Spring Chain

m xᵢ'' = k(xᵢ₊₁ + xᵢ₋₁ − 2xᵢ)

Run:

```bash
python scripts/cadeia_massas.py
```

---

### 4. Wave Interference in Mass-Spring Chain

Simulation of wave interference using Gaussian initial perturbations.

Run:

```bash
python scripts/cadeia_interferencia.py
```

---

### 5. Gravitational Two-Body Problem

r₁'' = G m₂ (r₂ − r₁) / |r₂ − r₁|³

r₂'' = G m₁ (r₁ − r₂) / |r₁ − r₂|³

This system conserves total energy and angular momentum.

Run:

```bash
python scripts/dois_corpos.py
```

---

### 6. RLC Circuit Simulation

V(t) = V₀ cos(ωt)

q'(t) = i

i'(t) = (V₀/L) cos(ωt) − (R/L)i − (1/(LC))q

Run:

```bash
python scripts/circuito_rlc.py
```

---

### 7. Spring-Mass Oscillator (with Gravity)

m y'' + k y = mg

Run:

```bash
python scripts/Massa-mola-gravidade.py
```

---

### 8. RC Circuit

q' + (1/RC) q = 0

Run:

```bash
python scripts/circuito_rc.py
```

---

### 9. Kapitza's Pendulum

y(t) = A cos(ωt)

Lθ'' = -g sin(θ) + Aω² cos(ωt) sin(θ)

Run:

```bash
python scripts/Kapitiza_pendulo.py
```

---

### 10. Driven Pendulum on Oscillating Cart

x(t) = A cos(ωt)

θ'' = −(g/L) sin(θ) + (A/L) cos(θ) cos(ωt)

Run:

```bash
python scripts/Driven_cart_pendulum.py
```

---

### 11. Projectile Motion with Air Resistance

x'(t) = vₓ

y'(t) = vᵧ

vₓ'(t) = -(k/m) · v · vₓ

vᵧ'(t) = -g -(k/m) · v · vᵧ

v = √(vₓ² + vᵧ²)

Run:

```bash
python scripts/Launch.py
```

---

## ▶️ How to Run

```bash
git clone https://github.com/gustavosbarroso/simplephysics.git
cd simplephysics
pip install -r requirements.txt
python scripts/<script_name>.py
```

---

## 🎛️ Interactive Controls

All simulations include:

* Sliders for real-time parameter adjustment
* Dynamic updates of trajectories and states
* Visualization of system evolution

---

## 🧠 Approach

* Systems modeled as ODEs
* Conversion to first-order systems
* Numerical integration via RK4 and SciPy solvers
* Dynamic visualization and analysis

---

## 🔗 Physical Connections

* Mechanical oscillators
* Electrical circuits
* Nonlinear dynamics
* Chaotic systems

---

## 🚧 Project Evolution

* Initial version: independent simulations using global variables
* Current stage: refactoring to a parameter-based architecture
* Next step: integration into a unified interface (Flask + Plotly)

---

## 🛠️ Development

Python, using:

* NumPy
* Matplotlib
* SciPy

---

## 👨‍🔬 Author

Gustavo Sobreira Barroso
Physics Engineering student

---

## 📄 License

MIT License
