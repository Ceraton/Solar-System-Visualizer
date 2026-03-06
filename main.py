from pathlib import Path
from src.bodies import *
import pygame

PLANETS_PATH = Path('data/planets.json')
MOONS_PATH = Path('data/moons.json')

solar_system = SolarSystem(PLANETS_PATH, MOONS_PATH)



pygame.init()
screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Solar System Visualizer")
clock = pygame.time.Clock()

if __name__ == "__main__":
    pass