# 🌌 Solar System Visualizer

An interactive, high-performance 2D orrery and astronomical data visualizer built with **Python** and **Pygame-CE**. This project simulates planetary motion based on real-world orbital elements (J2000 Epoch) and provides an immersive way to explore celestial mechanics.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Pygame](https://img.shields.io/badge/pygame--ce-latest-green.svg)

---

## 🚀 Features

* **Real-Time Orbital Simulation**: Accurate planetary positions calculated using mean longitude and orbital periods.
* **Atomic Time Engine**: A custom `Timeline` class that maps simulation frames to real calendar dates starting from the **J2000 epoch** (Jan 1, 2000).
* **Dynamic UI & Interactivity**:
    * **Orrery Mode**: Watch the planets dance in real-time with adjustable time-scales.
    * **Size Comparison Mode**: A sense of scale comparing the true radii of celestial bodies.
* **Deep Space Aesthetic**: Procedurally generated starfields with brightness variance and subtle parallax.
* **Educational Overlay**: Displays "Atomic Date" and detailed information panels for selected planets and moons.

---

## 🎮 Controls

| Key | Action |
| :--- | :--- |
| **1** | Switch to **Size Comparison** Mode |
| **2** | Switch to **Orrery (Orbit)** Mode |
| **SPACE** | Play / Pause Simulation |
| **= / -** | Increase / Decrease Time Speed (Atomic multiplier) |
| **L** | Toggle Labels |
| **R** | Reset Camera & Time |
| **Mouse Drag** | Pan around the system |
| **Scroll Wheel** | Zoom In / Out |

---

## 🛠️ Installation

### 1. Prerequisites
Ensure you have Python 3.10 or higher installed.

### 2. Clone the Repository
```bash
git clone