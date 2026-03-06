import json
from typing import List

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
    def __init__(self, name, radius_km, color, glow_color, mass_kg, description, type, distance_au):
        super().__init__(name, radius_km, color, glow_color, mass_kg, description, type)
        self.distance_au = distance_au
        self.parent = None

class SolarSystem:
    def __init__(self, planets_path, moons_path):
        self.planets = []
        self.moons = []
        self.small_bodies = []

        self._load_planets(planets_path)
        self._load_moons_and_small_bodies(moons_path)
        self._link_moons()

    def _load_planets(self, planets_path):
        with open(planets_path) as file:
            data = json.load(file)

        for entry in data:
            planet = Planet(entry)
            self.planets.append(planet)

    def _load_moons_and_small_bodies(self, moons_path):
        with open(moons_path) as file:
            data = json.load(file)

        for entry in data:
            if entry["type"] == "moon":
                moon = Moon(entry)
                self.moons.append(moon)
            else:
                small_body = SmallBody(entry)
                self.small_bodies.append(small_body)

    def _link_moons(self):
        for planet in self.planets:
            for moon in self.moons:
                if self.small_bodies["parent"] == planet["name"]:
                    planet.add_moon(moon)

    def get_all_bodies(self) -> List[CelestialBody]:
        return [self.planets] + [self.small_bodies] + [self.moons]
    
    def get_by_type(self, type_string):
        bodies = self.get_all_bodies()
        body_filter = []
        for body in bodies:
            if type_string == body.type:
                body_filter.append(body)
        return body_filter
    
    def get_by_name(self, name_string):
        bodies = self.get_all_bodies()
        body_filter = []
        for body in bodies:
            if name_string == body.name:
                body_filter.append(body)
        return body_filter
    
    def iterate_planets(self):
        for planet in self.planets:
            yield planet
            for moon in self.moons:
                yield moon

    def iterate_small_bodies(self):
        for body in self.small_bodies:
            yield body