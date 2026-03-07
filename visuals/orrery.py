import pygame, math
from visuals.renderer import draw_planet, is_on_screen
from visuals.timeline import Timeline


def clamp(n, min_value, max_value): return max(min_value, min(n, max_value))

AU_PX               = 55    #pixels per AU at zoom 1.0
ORBIT_SCALE_POWER   = 0.55  #compress distances so orbits can fit on screen

MIN_PLANET_R        = 3     #minimum planet radius in pixels
MAX_PLANET_R        = 22    #maximum planet radius in pixels

class OrreryMode:
    def __init__(self, solar_system, screen_w, screen_h, timeline):
        self.solar_system = solar_system
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.zoom = 1.0
        self.offset_x = screen_w / 2
        self.offset_y = screen_h / 2
        self.time = 0.0
        self.timeline = timeline

    def _orbit_radius_px(self, au, zoom):
        if au == 0:
            return 0
        
        return (au ** ORBIT_SCALE_POWER) * AU_PX * zoom
    
    def _planet_radius_px(self, planet):
        ratio = math.log10(planet.radius_km / 2000 + 1) + 0.3
        r = ratio * 14 * self.zoom
        return max(MIN_PLANET_R, min(MAX_PLANET_R * self.zoom, r))
    
    def planet_screen_pos(self, planet, time=None):
        if time is None:
            time = self.time

        if planet.distance_au == 0:
            return (int(self.offset_x), int(self.offset_y))
        
        angle_deg = self.timeline.get_angle(planet)
        angle_rad = angle_deg * (math.pi / 180)
        orbit_r = self._orbit_radius_px(planet.distance_au, self.zoom)
        x = self.offset_x + orbit_r * math.cos(angle_rad)
        y = self.offset_y + orbit_r * math.sin(angle_rad)
        return (int(x), int(y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            factor = 1.1 if event.y > 0 else 0.9
        
            mx, my = pygame.mouse.get_pos()
            self.offset_x = mx - (mx - self.offset_x) * factor
            self.offset_y = my - (my - self.offset_y) * factor
            self.zoom = clamp(self.zoom * factor, 0.1, 10.0)

    def update_pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def reset(self):
        self.zoom = 1.0
        self.offset_x = self.screen_w / 2
        self.offset_y = self.screen_h / 2

    def tick(self, dt):
        self.time += dt * 0.0005

    def get_hovered(self, mouse_pos):
        mx, my = mouse_pos
        for i, planet in enumerate(self.solar_system.planets):
            px, py = self.planet_screen_pos(planet)
            r   = self._planet_radius_px(planet)

            distance = math.sqrt((mx - px) ** 2 + (my - py) ** 2)
            if distance <= r + 4:
                return i
        return None
    
    def draw(self, surface, fonts, selected_idx, show_labels):
        cx = int(self.offset_x)
        cy = int(self.offset_y)

        orbit_surf = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
        for planet in self.solar_system.planets[1:]:
            orbit_r = self._orbit_radius_px(planet.distance_au, self.zoom)

            if 3 < orbit_r < 4000:
                pygame.draw.circle(\
                    orbit_surf,
                    (40, 50, 80, 120),
                    (cx, cy),
                    int(orbit_r),
                    1
                )
        surface.blit(orbit_surf, (0, 0))

        for i, planet in enumerate(self.solar_system.planets):
            pos = self.planet_screen_pos(planet)
            r   = max(2, int(self._planet_radius_px(planet)))

            if not is_on_screen(pos, r, self.screen_w, self.screen_h):
                continue

            draw_planet(
                surface,
                planet,
                pos,
                r,
                selected=(i == selected_idx),
                font=fonts[0] if show_labels else None,
                show_label=show_labels
            )