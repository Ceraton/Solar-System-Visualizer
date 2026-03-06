from pathlib import Path
from src.bodies import *


planets_json = Path('data/planets.json')
moons_json = Path('data/moons.json')

solar_system = SolarSystem(planets_json, moons_json)

if __name__ == "__main__":
    pass