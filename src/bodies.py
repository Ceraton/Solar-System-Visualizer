import json

# Abstract Celestial Entity
class CelestialBody:
    def __init__(self, data: dict):
        self.name = data["name"]
        self.radius_km = data["radius_km"]
        self.color = data["color"]
        self.glow_color = data["glow_color"]
        self.mass_kg = data["mass_kg"]
        self.description = data["description"]
        self.type = data["type"]

    def __repr__(self):
        return f"{self.type}: {self.name} (radius= {self.radius_km} km)"

# Planet and its Moons
class Planet(CelestialBody):
    def __init__(self, data: dict):
        super().__init__(data)
        self.distance_au = data["distance_au"]
        self.mean_longitude_deg   = data["mean_longitude_deg"]
        self.orbital_period_days  = data["orbital_period_days"]
        self.moons = []

    def add_moon(self, moon):
        self.moons.append(moon)

    def get_moon_count(self):
        return len(self.moons)

class Moon(CelestialBody):
    def __init__(self, data: dict):
        super().__init__(data)
        self.parent_name = data["parent"]
        self.orbital_radius_km = data["orbital_radius_km"]
        self.parent = None

#-- Pluto is a small body with its own moon --
class SmallBody(CelestialBody):
    def __init__(self, data: dict):
        super().__init__(data)
        self.distance_au = data["distance_au"]
        self.parent = None
        self.moons = []

    def add_moon(self, moon):
        self.moons.append(moon)

# Wrap everything together into a singular system
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
        lookup = {body.name: body for body in self.planets + self.small_bodies}
        for moon in self.moons:
            if moon.parent_name in lookup:
                moon.parent = lookup[moon.parent_name]
                moon.parent.add_moon(moon)

    def get_all_bodies(self):
        return self.planets + self.small_bodies + self.moons
    
    def get_by_type(self, type_string):
        bodies = self.get_all_bodies()
        body_filter = []
        for body in bodies:
            if type_string == body.type:
                body_filter.append(body)
        return body_filter
    
    def get_by_name(self, name_string):
        for body in self.get_all_bodies():
            if name_string == body.name:
                return body
        return None
    
    def iterate_planets(self):
        for planet in self.planets:
            yield planet
            for moon in planet.moons:
                yield moon

    def iterate_small_bodies(self):
        for body in self.small_bodies:
            yield body