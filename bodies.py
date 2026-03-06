import json


class CelestialBody:
    def __init__(self, name, radius_km, color, glow_color, mass_kg, description, type):
        self.name = name
        self.radius_km = radius_km
        self.color = color
        self.glow_color = glow_color
        self.mass_kg = mass_kg
        self.description = description
        self.type = type

    def __repr__(self):
        return "{self.type}: {self.name} (radius= {self.radius_km} km)"
    
class Planet(CelestialBody):
    def __init__(self, name, radius_km, color, glow_color, mass_kg, description, type, distance_au):
        super().__init__(name, radius_km, color, glow_color, mass_kg, description, type)
        self.distance_au = distance_au
        self.moons = []

    def add_moon(self, moon):
        self.moons.append(moon)

    def get_moon_count(self):
        return len(self.moons)

class Moon(CelestialBody):
    def __init__(self, name, radius_km, color, glow_color, mass_kg, description, type, parent, orbital_radius_km):
        super().__init__(name, radius_km, color, glow_color, mass_kg, description, type)
        self.parent_name = parent
        self.orbital_radius_km = orbital_radius_km
        self.parent = None

class SmallBody(CelestialBody):
    def __init__(self, name, radius_km, color, glow_color, mass_kg, description, type, parent, distance_au):
        super().__init__(name, radius_km, color, glow_color, mass_kg, description, type)
        self.distance_au = distance_au
        self.parent = None

class SolarSystem:
    def __init__(self, planets_path, moons_path):
        self.planets = []
        self.moon = []
        self.small_bodies = []

        self._load_planets(planets_path)
        self._load_moons_and_small_bodies(moons_path)
        self._link_moons()

        
