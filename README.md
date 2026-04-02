### 🌌 Solar System Visualizer

A vibecoded interactive, high-performance 2D orrery and astronomical data visualizer built with Python and Pygame-CE.
This project simulates planetary motion using real-world orbital elements (J2000 Epoch) and provides an immersive way to explore celestial mechanics.






### 🚀 Features

Real-Time Orbital Simulation

Accurate planetary positions calculated using mean longitude and orbital periods.

Atomic Time Engine

A custom Timeline class maps simulation frames to real calendar dates starting from the J2000 epoch (Jan 1, 2000).

Dynamic UI & Interactivity

Orrery Mode – Watch planets orbit in real time.

Size Comparison Mode – Compare the true radii of celestial bodies.

Deep Space Aesthetic

Procedurally generated starfields with brightness variance and subtle parallax.

Educational Overlay

Displays the Atomic Date and information panels for planets and moons.

### 🎮 Controls
Key	Action
1	Size Comparison Mode
2	Orrery (Orbit) Mode
SPACE	Play / Pause simulation
= / -	Increase / Decrease time speed
L	Toggle labels
R	Reset camera & time
Mouse Drag	Pan camera
Scroll Wheel	Zoom

### 🛠 Installation
1. Prerequisites

Install Python 3.10 or higher

2. Clone the Repository
git clone https://github.com/ceraton/Solar-System-Visualizer.git
cd Solar-System-Visualizer
3. Install Dependencies
pip install pygame-ce

### 🧪 The Math Behind the Orbits

The simulation uses simplified Keplerian elements.

The position of a body at time t is calculated using Mean Longitude:

theta(t) = L0 + (360 / P * delta_t)

Where:

L0 — Mean Longitude at the J2000 reference epoch

P — Orbital period in Earth days

delta_t — Days elapsed since January 1, 2000

### 📂 Project Structure
Solar-System-Visualizer
│
├── main.py              # Entry point and event loop
│
├── data/
│   ├── planets.json     # NASA-derived orbital data
│   └── moons.json       # Lunar orbital data
│
├── src/
│   └── bodies.py        # CelestialBody class hierarchy
│
└── visuals/
    ├── orrery.py        # Orbital math and rendering
    ├── timeline.py      # Atomic clock & date logic
    └── renderer.py      # Starfield and UI helpers
