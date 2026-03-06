import unittest
from unittest.mock import MagicMock
import sys
import os

# Allow running from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.bodies import CelestialBody, Planet, Moon, SmallBody, SolarSystem

PLANETS_PATH = "data/planets.json"
MOONS_PATH = "data/moons.json"

# ── TestCelestialBody ──────────────────────────────────────────────────────────

class TestCelestialBody(unittest.TestCase):

    def setUp(self):
        self.data = {
            "name": "TestBody",
            "radius_km": 5000,
            "color": [100, 100, 100],
            "glow_color": [80, 80, 80],
            "mass_kg": 1.0e20,
            "description": "A test body.",
            "type": "planet"
        }
        self.body = CelestialBody(self.data)

    def test_name_assigned(self):
        self.assertEqual(self.body.name, "TestBody")

    def test_radius_assigned(self):
        self.assertEqual(self.body.radius_km, 5000)

    def test_color_assigned(self):
        self.assertEqual(self.body.color, [100, 100, 100])

    def test_glow_color_assigned(self):
        self.assertEqual(self.body.glow_color, [80, 80, 80])

    def test_mass_assigned(self):
        self.assertEqual(self.body.mass_kg, 1.0e20)

    def test_description_assigned(self):
        self.assertEqual(self.body.description, "A test body.")

    def test_type_assigned(self):
        self.assertEqual(self.body.type, "planet")

    def test_repr_is_string(self):
        self.assertIsInstance(repr(self.body), str)

    def test_repr_contains_name(self):
        self.assertIn("TestBody", repr(self.body))


# ── TestPlanet ─────────────────────────────────────────────────────────────────

class TestPlanet(unittest.TestCase):

    def setUp(self):
        self.data = {
            "name": "TestPlanet",
            "radius_km": 6371,
            "color": [70, 130, 180],
            "glow_color": [30, 80, 140],
            "mass_kg": 5.972e24,
            "description": "A test planet.",
            "type": "planet",
            "distance_au": 1.0,
            "moons": 1
        }
        self.planet = Planet(self.data)

    def test_distance_au_assigned(self):
        self.assertEqual(self.planet.distance_au, 1.0)

    def test_moons_list_starts_empty(self):
        self.assertEqual(self.planet.moons, [])

    def test_add_moon(self):
        mock_moon = MagicMock()
        self.planet.add_moon(mock_moon)
        self.assertIn(mock_moon, self.planet.moons)

    def test_add_multiple_moons(self):
        moon_a = MagicMock()
        moon_b = MagicMock()
        self.planet.add_moon(moon_a)
        self.planet.add_moon(moon_b)
        self.assertEqual(len(self.planet.moons), 2)

    def test_get_moon_count_zero(self):
        self.assertEqual(self.planet.get_moon_count(), 0)

    def test_get_moon_count_after_adding(self):
        self.planet.add_moon(MagicMock())
        self.planet.add_moon(MagicMock())
        self.assertEqual(self.planet.get_moon_count(), 2)


# ── TestMoon ───────────────────────────────────────────────────────────────────

class TestMoon(unittest.TestCase):

    def setUp(self):
        self.data = {
            "name": "Moon",
            "radius_km": 1737.4,
            "color": [200, 195, 185],
            "glow_color": [160, 155, 145],
            "mass_kg": 7.342e22,
            "description": "Earth's only natural satellite.",
            "type": "moon",
            "parent": "Earth",
            "orbital_radius_km": 384400
        }
        self.moon = Moon(self.data)

    def test_parent_name_assigned(self):
        self.assertEqual(self.moon.parent_name, "Earth")

    def test_orbital_radius_assigned(self):
        self.assertEqual(self.moon.orbital_radius_km, 384400)

    def test_parent_ref_starts_as_none(self):
        self.assertIsNone(self.moon.parent)

    def test_type_assigned(self):
        self.assertEqual(self.moon.type, "moon")


# ── TestSmallBody ──────────────────────────────────────────────────────────────

class TestSmallBody(unittest.TestCase):

    def setUp(self):
        self.data = {
            "name": "Ceres",
            "radius_km": 469.7,
            "color": [160, 155, 145],
            "glow_color": [120, 115, 105],
            "mass_kg": 9.39e20,
            "description": "Largest asteroid.",
            "type": "asteroid",
            "distance_au": 2.77,
            "parent": None
        }
        self.body = SmallBody(self.data)

    def test_distance_au_assigned(self):
        self.assertEqual(self.body.distance_au, 2.77)

    def test_parent_is_none(self):
        self.assertIsNone(self.body.parent)

    def test_type_assigned(self):
        self.assertEqual(self.body.type, "asteroid")


# ── TestSolarSystem ────────────────────────────────────────────────────────────

class TestSolarSystem(unittest.TestCase):

    def setUp(self):
        self.ss = SolarSystem(PLANETS_PATH, MOONS_PATH)

    def test_planets_loaded(self):
        self.assertGreater(len(self.ss.planets), 0)

    def test_planets_are_planet_instances(self):
        for p in self.ss.planets:
            self.assertIsInstance(p, Planet)

    def test_small_bodies_loaded(self):
        self.assertGreater(len(self.ss.small_bodies), 0)

    def test_small_bodies_are_smallbody_instances(self):
        for b in self.ss.small_bodies:
            self.assertIsInstance(b, SmallBody)

    def test_moons_loaded(self):
        self.assertGreater(len(self.ss.moons), 0)

    def test_moons_are_moon_instances(self):
        for m in self.ss.moons:
            self.assertIsInstance(m, Moon)

    def test_moons_linked_to_parents(self):
        for moon in self.ss.moons:
            if moon.parent_name is not None:
                self.assertIsNotNone(moon.parent)
                self.assertIn(moon, moon.parent.moons)

    def test_get_all_bodies_count(self):
        all_bodies = self.ss.get_all_bodies()
        expected = len(self.ss.planets) + len(self.ss.small_bodies) + len(self.ss.moons)
        self.assertEqual(len(all_bodies), expected)

    def test_get_by_type_planets(self):
        result = self.ss.get_by_type("planet")
        for body in result:
            self.assertEqual(body.type, "planet")

    def test_get_by_type_asteroids(self):
        result = self.ss.get_by_type("asteroid")
        self.assertGreater(len(result), 0)
        for body in result:
            self.assertEqual(body.type, "asteroid")

    def test_get_by_type_moons(self):
        result = self.ss.get_by_type("moon")
        self.assertGreater(len(result), 0)
        for body in result:
            self.assertEqual(body.type, "moon")

    def test_get_by_type_dwarf_planets(self):
        result = self.ss.get_by_type("dwarf_planet")
        self.assertGreater(len(result), 0)
        for body in result:
            self.assertEqual(body.type, "dwarf_planet")

    def test_get_by_name_found(self):
        result = self.ss.get_by_name("Earth")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Earth")

    def test_get_by_name_not_found(self):
        result = self.ss.get_by_name("Krypton")
        self.assertIsNone(result)

    def test_get_by_name_moon(self):
        result = self.ss.get_by_name("Moon")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, "moon")

    def test_get_by_name_asteroid(self):
        result = self.ss.get_by_name("Ceres")
        self.assertIsNotNone(result)
        self.assertEqual(result.type, "asteroid")

    def test_iterate_planets_yields_planets_and_moons(self):
        results = list(self.ss.iterate_planets())
        planet_names = {p.name for p in self.ss.planets}
        moon_names = {m.name for m in self.ss.moons}
        for item in results:
            self.assertIn(item.name, planet_names | moon_names)

    def test_iterate_planets_planet_comes_before_its_moons(self):
        results = list(self.ss.iterate_planets())
        for planet in self.ss.planets:
            planet_index = next(i for i, b in enumerate(results) if b.name == planet.name)
            for moon in planet.moons:
                moon_index = next(i for i, b in enumerate(results) if b.name == moon.name)
                self.assertLess(planet_index, moon_index)

    def test_iterate_small_bodies_count(self):
        results = list(self.ss.iterate_small_bodies())
        self.assertEqual(len(results), len(self.ss.small_bodies))

    def test_earth_has_moon(self):
        earth = self.ss.get_by_name("Earth")
        self.assertIsNotNone(earth)
        self.assertGreaterEqual(earth.get_moon_count(), 1)
        moon_names = [m.name for m in earth.moons]
        self.assertIn("Moon", moon_names)

    def test_jupiter_has_four_galilean_moons(self):
        jupiter = self.ss.get_by_name("Jupiter")
        self.assertIsNotNone(jupiter)
        moon_names = [m.name for m in jupiter.moons]
        for name in ["Io", "Europa", "Ganymede", "Callisto"]:
            self.assertIn(name, moon_names)

    def test_mars_has_two_moons(self):
        mars = self.ss.get_by_name("Mars")
        self.assertIsNotNone(mars)
        moon_names = [m.name for m in mars.moons]
        self.assertIn("Phobos", moon_names)
        self.assertIn("Deimos", moon_names)

    def test_sun_has_no_moons(self):
        sun = self.ss.get_by_name("Sun")
        self.assertIsNotNone(sun)
        self.assertEqual(sun.get_moon_count(), 0)

    def test_all_planets_have_distance_au(self):
        for planet in self.ss.planets:
            self.assertIsNotNone(planet.distance_au)
            self.assertGreaterEqual(planet.distance_au, 0)

    def test_all_moons_have_orbital_radius(self):
        for moon in self.ss.moons:
            self.assertIsNotNone(moon.orbital_radius_km)
            self.assertGreater(moon.orbital_radius_km, 0)


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)