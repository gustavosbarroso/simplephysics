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

Simulation of a double pendulum using RK4.

This system is a classical example of nonlinear dynamics and chaos.

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

Simulation of two bodies interacting under Newtonian gravity.

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

### 7. Spring-mass oscillator
Electrical analog of a damped oscillator:

my'' + (k/m)y' + g = 0

Run:

```bash
python scripts/Massa-mola-gravidade.py
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/gustavosbarroso/simplephysics.git
cd simplephysics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run any simulation

```bash
python scripts/<script_name>.py
```

---

## 🎛️ Interactive Controls

All simulations include sliders for real-time adjustment of physical parameters and initial conditions.

---

## 🧠 Approach

* Physical systems are modeled as ODEs
* Higher-order equations are rewritten as first-order systems
* Numerical integration is performed using RK4 or adaptive methods
* Results are visualized dynamically

---

## 🔗 Physical Connections

Many systems share the same mathematical structure:

* Mechanical oscillators (pendulum)
* Electrical circuits (RLC)
* Coupled systems (mass chains)

---

## 🚀 Future Improvements

* Phase space visualization
* Energy analysis

---

## 🛠️ Development

Developed in Python using:

* NumPy
* Matplotlib
* SciPy

---

## 👨‍🔬 Author

Gustavo Sobreira Barroso
Physics Engineering student
