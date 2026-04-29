simplephysics

This repository contains numerical simulations of physical systems using the 4th-order Runge-Kutta (RK4) method, numerical integration techniques, and interactive visualization.

The project explores a wide range of topics in physics through computational approaches, emphasizing both numerical accuracy and physical interpretation, including dynamical systems and electromagnetic field simulations.

Features
Numerical integration of ordinary differential equations (ODEs)
RK4 implementation for general dynamical systems
Use of modern solvers (SciPy solve_ivp)
Simpson integration for continuous field distributions
Simulation of nonlinear and coupled systems
Discrete evaluation of electromagnetic fields on grids
Real-time animation using matplotlib
Interactive parameter control via sliders
Visualization of trajectories, phase space, and vector fields

Implemented Systems

Damped Pendulum and Simple Pendulum

Nonlinear pendulum with damping:

θ'' + (b/m)θ' + (g/L) sin(θ) = 0

Run:
python scripts/pendulo_amortecido.py

Simple pendulum (b = 0):

θ'' + (g/L) sin(θ) = 0

Run:
python scripts/Pendulo_simples.py

Double Pendulum (Chaotic System)

θ₁'' = [ -g(2m₁ + m₂)sin(θ₁) - m₂g sin(θ₁ - 2θ₂) - 2 sin(θ₁ - θ₂)m₂(θ₂'²L₂ + θ₁'²L₁cos(θ₁ - θ₂)) ]
/ [ L₁(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

θ₂'' = [ 2 sin(θ₁ - θ₂)(θ₁'²L₁(m₁ + m₂) + g(m₁ + m₂)cos(θ₁) + θ₂'²L₂m₂cos(θ₁ - θ₂)) ]
/ [ L₂(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

Run:
python scripts/Pendulo_duplo.py

Coupled Mass-Spring Chain

m xᵢ'' = k(xᵢ₊₁ + xᵢ₋₁ − 2xᵢ)

Run:
python scripts/cadeia_massas.py

Wave Interference in Mass-Spring Chain

Simulation of wave propagation and interference using Gaussian perturbations.

Run:
python scripts/cadeia_interferencia.py

Gravitational Two-Body Problem

r₁'' = G m₂ (r₂ − r₁) / |r₂ − r₁|³
r₂'' = G m₁ (r₁ − r₂) / |r₂ − r₁|³

This system conserves total energy and angular momentum.

Run:
python scripts/dois_corpos.py

RLC Circuit Simulation

V(t) = V₀ cos(ωt)

q'(t) = i
i'(t) = (V₀/L) cos(ωt) − (R/L)i − (1/(LC))q

Run:
python scripts/circuito_rlc.py

Spring-Mass Oscillator (with Gravity)

m y'' + k y = mg

Run:
python scripts/Massa-mola-gravidade.py

RC Circuit

q' + (1/RC) q = 0

Run:
python scripts/circuito_rc.py

Kapitza's Pendulum

y(t) = A cos(ωt)

Lθ'' = -g sin(θ) + Aω² cos(ωt) sin(θ)

Run:
python scripts/Kapitiza_pendulo.py

Driven Pendulum on Oscillating Cart

x(t) = A cos(ωt)

θ'' = −(g/L) sin(θ) + (A/L) cos(θ) cos(ωt)

Run:
python scripts/Driven_cart_pendulum.py

Projectile Motion with Air Resistance

x'(t) = vₓ
y'(t) = vᵧ

vₓ'(t) = -(k/m) v vₓ
vᵧ'(t) = -g -(k/m) v vᵧ

v = √(vₓ² + vᵧ²)

Run:
python scripts/Launch.py

Electromagnetic Field Simulations

Electric field (Coulomb law):

E(r) = (1/4πϵ₀) Σ [ qᵢ (r - rᵢ) / |r - rᵢ|³ ]

Examples:
python fields_scripts/Eletric_field/Point_charge.py
python fields_scripts/Eletric_field/Conducting_sphere.py

Magnetic Field (Biot–Savart law)

dB = (μ₀/4π) (I dℓ × r̂) / r²

Examples:
python fields_scripts/Magnetic_field/Infinite_wire.py
python fields_scripts/Magnetic_field/Finite_wire.py
python fields_scripts/Magnetic_field/Infinite_cilyndrical_wire.py
python fields_scripts/Magnetic_field/Finite_solenoid.py

Field Simulation Structure

fields_scripts/
├── Eletric_field/
├── Magnetic_field/

Pattern:
Field function → Grid → Normalization → Streamplot → Interactivity

How to Run

git clone https://github.com/gustavosbarroso/simplephysics.git

cd simplephysics
pip install -r requirements.txt

Run:
python scripts/<script_name>.py

or:
python fields_scripts/<category>/<script_name>.py

Interactive Controls

Sliders for real-time parameter adjustment
Dynamic updates of trajectories and states
Visualization of system evolution
Real-time recomputation

Approach

Systems modeled as ODEs or continuous fields
Conversion to first-order systems
Numerical integration via RK4 and SciPy solvers
Spatial discretization for field problems
Dynamic visualization and analysis

Physical Connections

Classical mechanics
Electrical circuits
Electromagnetism
Nonlinear dynamics
Chaos theory
Wave phenomena

Project Evolution

Initial version: independent simulations using global variables
Current stage: modular and parameter-based architecture
Includes: ODE systems and field simulations
Next step: unified simulation interface (Flask + Plotly)

Development

Python, using:

NumPy
Matplotlib
SciPy
IPyWidgets

Author

Gustavo Sobreira Barroso
Physics Engineering Student

License

MIT License
