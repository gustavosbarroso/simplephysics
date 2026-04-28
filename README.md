🔬 simplephysics

This repository contains computational physics simulations of classical and electromagnetic systems using:

- 4th-order Runge-Kutta (RK4)
- Numerical integration (Simpson method)
- Discrete field solvers
- Interactive visualization (Matplotlib + widgets)

The goal is to build a modular physics simulation framework, where each system follows a consistent structure:

Equations → Numerical method → Visualization → Interactivity

⚙️ Core Features

🧮 Numerical Methods
- RK4 integration for dynamical systems
- Simpson numerical integration for field problems
- ODE → first-order system reduction
- Discrete evaluation of continuous fields

📊 Visualization
- Real-time matplotlib animation
- Streamplot field visualization (E, B fields)
- Phase space / trajectory plots
- 1D + 2D coupled visual outputs

🎛️ Interactivity
- Slider-based parameter control
- Live system updates (update(val) pattern)
- HUD-style physical information display
- Instant feedback for parameter changes

🧠 Architecture Philosophy

All simulations follow a unified structure:

Physics model → Field / ODE function → Numerical method → Update loop → Visualization

Two main categories:

1. Dynamical Systems (RK4)
- Pendulums
- Oscillators
- Chaotic systems
- Circuits

2. Field Systems (Simpson / Analytical discretization)
- Electric fields
- Magnetic fields
- Charge distributions
- Finite geometry sources

📦 Implemented Systems

🧷 1. Pendulums (Linear & Nonlinear)

Nonlinear damped pendulum:
θ'' + (b/m)θ' + (g/L) sin(θ) = 0  

Run:
python scripts/pendulo_amortecido.py

Simple pendulum:

θ'' + (g/L) sin(θ) = 0  

Run:
python scripts/Pendulo_simples.py


🌀 2. Double Pendulum (Chaotic System)

Highly nonlinear coupled system exhibiting chaos.

θ₁'' = [ -g(2m₁ + m₂)sin(θ₁) - m₂g sin(θ₁ - 2θ₂) - 2 sin(θ₁ - θ₂)m₂(θ₂'²L₂ + θ₁'²L₁cos(θ₁ - θ₂)) ] / [ L₁(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

θ₂'' = [ 2 sin(θ₁ - θ₂)(θ₁'²L₁(m₁ + m₂) + g(m₁ + m₂)cos(θ₁) + θ₂'²L₂m₂cos(θ₁ - θ₂)) ] / [ L₂(2m₁ + m₂ - m₂cos(2θ₁ - 2θ₂)) ]

Run:
python scripts/Pendulo_duplo.py



🧵 3. Coupled Oscillators (Mass-Spring Chain)

m xᵢ'' = k(xᵢ₊₁ + xᵢ₋₁ − 2xᵢ)

Run:
python scripts/cadeia_massas.py


🌊 4. Wave Interference in Chains

Gaussian perturbation propagation + interference effects.

Run:
python scripts/cadeia_interferencia.py


🌍 5. Two-Body Gravitational System

r₁'' = G m₂ (r₂ − r₁) / |r₂ − r₁|³  
r₂'' = G m₁ (r₁ − r₂) / |r₁ − r₂|³  

Conserves energy and angular momentum.

Run:
python scripts/dois_corpos.py


⚡ 6. RLC Circuit

q' = i  
i' = (V₀/L) cos(ωt) − (R/L)i − (1/(LC))q  

Run:
python scripts/circuito_rlc.py


🔌 7. RC Circuit

q' + (1/RC) q = 0  

Run:
python scripts/circuito_rc.py


🧲 8. Kapitza Pendulum

Fast oscillating pivot system with effective potential.

Run:
python scripts/Kapitiza_pendulo.py


🚗 9. Driven Pendulum (Oscillating Base)

x(t) = A cos(ωt)  
θ'' = −(g/L) sin(θ) + (A/L) cos(θ) cos(ωt)

Run:
python scripts/Driven_cart_pendulum.py


🪂 10. Projectile with Air Resistance

v = √(vₓ² + vᵧ²)

vₓ' = -(k/m) v vₓ  
vᵧ' = -g - (k/m) v vᵧ  

Run:
python scripts/Launch.py


⚡ 11. Electromagnetic Field Systems (NEW STRUCTURE)

This project also includes field-based simulations, built with a different architecture:

🧲 Electric Field (charges, dipoles)
- Coulomb law discretized on grids
- Streamplot visualization
- Charge superposition

🧲 Magnetic Field (wire, solenoid)
- Biot-Savart numerical integration
- Symmetry-based simplifications
- Field line visualization

🔁 Standard Pattern:

Field function → Grid evaluation → Normalization → Streamplot → HUD


▶️ How to Run

git clone https://github.com/gustavosbarroso/simplephysics.git
cd simplephysics
pip install -r requirements.txt
python scripts/<script_name>.py



🎛️ Interactive System Design

Every simulation includes:

- Real-time sliders
- Instant recomputation of ODE/fields
- Dynamic visualization updates
- Physical parameter HUD
- Clean separation: physics / numerics / plotting


🧠 Methodology

Dynamical systems:
- Convert to first-order ODEs
- Integrate via RK4 or SciPy solvers
- Visualize trajectories + phase space

Field systems:
- Define continuous field equation
- Discretize on spatial grid
- Normalize vectors
- Plot streamlines / magnitude maps


🔗 Physical Domains Covered

- Classical mechanics
- Nonlinear dynamics
- Chaos theory
- Electrical circuits
- Electromagnetism
- Numerical physics methods


🚧 Project Evolution

Stage 1:
Independent scripts with global variables

Stage 2:
RK4-based modular simulations

Stage 3 (current):
Hybrid framework:
- ODE systems (RK4)
- Field systems (Simpson + grid solvers)
- Unified visualization style

Stage 4 (planned):
- Unified simulation engine
- GUI (Flask / Plotly / web-based)
- Plug-and-play physics modules


🛠️ Tech Stack

- Python
- NumPy
- Matplotlib
- SciPy
- IPyWidgets


👨‍🔬 Author

Gustavo Sobreira Barroso  

Physics Engineering Student


📄 License

MIT License
