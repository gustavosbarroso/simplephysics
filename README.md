# 🔬 simplephysics

This repository contains numerical simulations of physical systems using the 4th-order Runge-Kutta (RK4) method and other numerical integrators, combined with interactive visualization.

The project explores a wide range of topics in physics through computational approaches, emphasizing both numerical accuracy and physical interpretation.

---

## ⚙️ Features

* Numerical integration of ordinary differential equations (ODEs)
* RK4 implementation for general dynamical systems
* Simulation of nonlinear and coupled systems
* Real-time animation using matplotlib
* Interactive parameter control via sliders
* Visualization of system dynamics and trajectories

---

## 📦 Implemented Systems

### 1. Damped Pendulum

Nonlinear pendulum with damping:

θ'' + bθ' + (g/L) sin(θ) = 0

Run:

```bash
python scripts/pendulo_amortecido.py
```

---

### 2. Double Pendulum (Chaotic System)

The double pendulum is a classical nonlinear system exhibiting chaotic behavior.

The equations of motion are:

θ₁'' = [ -g(2m₁ + m₂)sin(θ₁) - m₂g sin(θ₁ - 2θ₂) - 2 sin(θ₁ - θ₂)m₂(θ₂'²L₂ + θ₁'²L₁cos(θ₁ - θ₂)) ]/ [ L₁(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

θ₂'' = [ 2 sin(θ₁ - θ₂)(θ₁'²L₁(m₁ + m₂) + g(m₁ + m₂)cos(θ₁)+ θ₂'²L₂m₂cos(θ₁ - θ₂)) ]/ [ L₂(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

Run:

```bash
python scripts/Pendulo_duplo.py
```

---

### 3. Coupled Mass-Spring Chain

1D system of coupled oscillators:

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

Two bodies interacting via Newtonian gravity:

r₁'' = G m₂ (r₂ − r₁) / |r₂ − r₁|³
r₂'' = G m₁ (r₁ − r₂) / |r₁ − r₂|³

This system conserves total energy and angular momentum.

Run:

```bash
python scripts/dois_corpos.py
```

---

### 6. RLC Circuit Simulation

Electrical analog of a damped oscillator:

Lq'' + Rq' + (1/C)q = 0

Run:

```bash
python scripts/circuito_rlc.py
```

---

### 7. Spring-Mass Oscillator (with Gravity)

Mass-spring system under gravity:

m y'' + k y = mg

Run:

```bash
python scripts/Massa-mola-gravidade.py
```

---

### 8. RC Circuit

First-order system analogous to an overdamped oscillator:

q' + (1/RC) q = 0

Run:

```bash
python scripts/circuito_rc.py
```

---

### 9. Kapitiza's Pendulum

Fundamental to nonlinear dynamics, this simulation describes the dynamics of a pendulum whose pivot oscillates vertically according to y(t)=Acos(vt)

Lθ''=-gsin(θ) + Av²cos(vt)sin(θ)

Run:

```bash
python scripts/Kapitiza_pendulo.py
```
---
---

### 10. Driven Pendulum on Oscillating Cart

Pendulum attached to a cart with prescribed motion:

x(t) = A cos(ωt)

θ'' = −(g/L) sin(θ) + (A/L) cos(θ) cos(ωt)

Run:

```bash
python scripts/Driven_cart_pendulum.py
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

All simulations include sliders for real-time adjustment of physical parameters and initial conditions.

---

## 🧠 Approach

* Systems modeled as ODEs
* Conversion to first-order systems
* Numerical integration via RK4
* Dynamic visualization

---

## 🔗 Physical Connections

* Mechanical oscillators
* Electrical circuits
* Nonlinear dynamics
* Chaotic systems

---

## 🚀 Future Improvements

* Phase space visualization
* Energy tracking
* Chaos diagnostics (Poincaré sections, Lyapunov exponents)

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
