# SimplePhysics

This repository contains computational physics simulations using analytical models, numerical methods, and interactive visualization.

The project explores a wide range of physical phenomena, including dynamical systems, electromagnetic fields, electrical circuits, and quantum mechanics, emphasizing physical interpretation and interactive exploration.

⚙️ FEATURES

- Numerical integration of ordinary differential equations (ODEs)
- RK4 implementation for general dynamical systems
- Use of modern solvers (SciPy solve_ivp)
- Simpson integration for continuous field distributions
- Analytical and algebraic physical models
- Simulation of nonlinear and coupled systems
- Discrete evaluation of electromagnetic fields on grids
- Finite-difference methods and Crank–Nicolson time evolution
- Real-time animation using matplotlib
- Interactive parameter control via sliders
- Visualization of trajectories, wavefunctions, and vector fields

📦 IMPLEMENTED SYSTEMS

I. DAMPED PENDULUM AND SIMPLE PENDULUM

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

II. DOUBLE PENDULUM (CHAOTIC SYSTEM)

θ₁'' = [ -g(2m₁ + m₂)sin(θ₁) - m₂g sin(θ₁ - 2θ₂) - 2m₂ sin(θ₁ - θ₂)(θ₂'²L₂ + θ₁'²L₁cos(θ₁ - θ₂)) ] / [ L₁(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

θ₂'' = [ 2sin(θ₁ - θ₂)(θ₁'²L₁(m₁ + m₂) + g(m₁ + m₂)cos(θ₁) + θ₂'²L₂m₂cos(θ₁ - θ₂)) ] / [ L₂(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

Run:
```bash
python scripts/Pendulo_duplo.py
```

III. COUPLED MASS-SPRING CHAIN

m xᵢ'' = k(xᵢ₊₁ + xᵢ₋₁ − 2xᵢ)

Run:
```bash
python scripts/cadeia_massas.py
```

IV. WAVE INTERFERENCE IN MASS-SPRING CHAIN

Simulation of wave propagation and interference using Gaussian perturbations.

Run:
```bash
python scripts/cadeia_interferencia.py
```

V. GRAVITATIONAL TWO-BODY PROBLEM

r₁'' = G m₂ (r₂ − r₁) / |r₂ − r₁|³

r₂'' = G m₁ (r₁ − r₂) / |r₁ − r₂|³

This system conserves total energy and angular momentum.

Run:
```bash
python scripts/dois_corpos.py
```

VI. RLC CIRCUIT SIMULATION

V(t) = V₀ cos(ωt)

q'(t) = i

i'(t) = (V₀/L) cos(ωt) − (R/L)i − (1/(LC))q

Run:
```bash
python scripts/circuito_rlc.py
```

VII. SPRING-MASS OSCILLATOR (WITH GRAVITY)

m y'' + k y = mg

Run:
```bash
python scripts/Massa-mola-gravidade.py
```

VIII. RC CIRCUIT

q' + (1/RC) q = 0

Run:
```bash
python scripts/circuito_rc.py
```

IX. KAPITZA'S PENDULUM

y(t) = A cos(ωt)

Lθ'' = −g sin(θ) + Aω² cos(ωt) sin(θ)

Run:
```bash
python scripts/Kapitiza_pendulo.py
```

X. DRIVEN PENDULUM ON OSCILLATING CART

x(t) = A cos(ωt)

θ'' = −(g/L) sin(θ) + (A/L) cos(θ) cos(ωt)

Run:
```bash
python scripts/Driven_cart_pendulum.py
```

XI. PROJECTILE MOTION WITH AIR RESISTANCE

x'(t) = vₓ

y'(t) = vᵧ

vₓ'(t) = −(k/m) v vₓ

vᵧ'(t) = −g − (k/m) v vᵧ

v = √(vₓ² + vᵧ²)

Run:
```bash
python scripts/Launch.py
```

XII. ⚡ ELECTROMAGNETIC FIELD SIMULATIONS

Electric field (Coulomb's law):

E(r) = (1/4πϵ₀) Σ [ qᵢ (r − rᵢ) / |r − rᵢ|³ ]

Examples:
```bash
python fields_scripts/Eletric_field/Point_charge.py
python fields_scripts/Eletric_field/Conducting_sphere.py
```

Magnetic field (Biot–Savart law):

dB = (μ₀/4π) (I dℓ × r̂) / r²

Examples:
```bash
python fields_scripts/Magnetic_field/Infinite_wire.py
python fields_scripts/Magnetic_field/Finite_wire.py
python fields_scripts/Magnetic_field/Infinite_cilyndrical_wire.py
python fields_scripts/Magnetic_field/Finite_solenoid.py
```

XIII. AC GENERATOR

Induced electromotive force in a rotating coil:

ε(t) = −NABω sin(ωt)

Current through a resistive load:

I(t) = ε(t) / R

The simulation includes a rotating coil, magnetic field visualization, voltage and current curves, and a lamp whose brightness responds to the induced voltage.

XIV. SNELL'S LAW AND TOTAL INTERNAL REFLECTION

Snell's law:

n₁ sin(θ₁) = n₂ sin(θ₂)

Refraction is determined from the refractive indices and the angle of incidence. The simulation also identifies critical incidence and total internal reflection.

XV. QUANTUM TUNNELING

Time-dependent Schrödinger equation:

iℏ ∂Ψ/∂t = ĤΨ

Finite-difference discretization of the Hamiltonian:

Hᵢᵢ = ℏ²/(m Δx²) + Vᵢ

Hᵢ,ᵢ₊₁ = Hᵢ,ᵢ₋₁ = −ℏ²/(2m Δx²)

Crank–Nicolson time evolution:

(I + iΔtH/(2ℏ)) Ψ(t + Δt) = (I − iΔtH/(2ℏ)) Ψ(t)

The simulation visualizes the probability density |Ψ(x,t)|² as a wave packet interacts with a potential barrier. Interactive parameters include barrier height, barrier width, initial position, packet width, and initial wave number.

XVI. PHOTOELECTRIC EFFECT

Einstein's photoelectric equation:

Kₘₐₓ = hf − φ

Threshold frequency:

f꜀ = φ / h

Maximum kinetic energy:

Kₘₐₓ = max(hf − φ, 0)

The simulation illustrates photoelectron emission as a function of the incident light frequency, work function, and light intensity. It includes an animated representation of the metal surface, emitted electrons, and the maximum kinetic energy as a function of frequency.

Interactive parameters:

- Light frequency
- Work function
- Relative light intensity

Emission occurs only when f > f꜀ and the light intensity is greater than zero. The animation illustrates the dependence of emission rate on intensity and the maximum kinetic energy on frequency.

The electron trajectories and velocities are illustrative visual representations.

🧲 FIELD SIMULATION STRUCTURE

fields_scripts/
├── Eletric_field/
└── Magnetic_field/

Pattern:

Field function → Grid → Normalization → Streamplot → Interactivity

▶️ HOW TO RUN

Clone the repository:

```bash
git clone https://github.com/gustavosbarroso/simplephysics.git
cd simplephysics
pip install -r requirements.txt
```

Run a simulation:

```bash
python scripts/<script_name>.py
```

Or run an electromagnetic field simulation:

```bash
python fields_scripts/<category>/<script_name>.py
```

🎛️ INTERACTIVE CONTROLS

- Sliders for real-time parameter adjustment
- Dynamic updates of trajectories and physical states
- Visualization of system evolution
- Real-time recomputation
- Animated representations of time-dependent phenomena

🧠 APPROACH

- Analytical and algebraic evaluation of physical models
- Conversion of second-order ODEs into first-order systems when appropriate
- Numerical integration via RK4 and SciPy solvers
- Spatial discretization for field and quantum problems
- Crank–Nicolson propagation for quantum time evolution
- Dynamic visualization and physical analysis

🔗 PHYSICAL CONNECTIONS

- Classical mechanics
- Electrical circuits
- Electromagnetism
- Electromagnetic induction
- Quantum mechanics
- Nonlinear dynamics
- Chaos theory
- Wave phenomena
- Numerical methods

🚧 PROJECT EVOLUTION

Initial version: independent simulations using global variables

Current stage: modular and parameter-based architecture

Includes: analytical models, ODE systems, electromagnetic field simulations, and quantum wavefunction evolution

Next step: unified simulation interface (Flask + Plotly)

🛠️ DEVELOPMENT

Python, using:

- NumPy
- Matplotlib
- SciPy
- IPyWidgets

👨‍🔬 AUTHOR

Gustavo Sobreira Barroso

Physics Engineering Student

📄 LICENSE

MIT License
