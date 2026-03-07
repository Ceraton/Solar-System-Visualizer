import pygame, math
from visuals.renderer import draw_planet, is_on_screen

BASE_EARTH_PX = 30
EARTH_RADIUS_KM = 6371.0

def clamp(n, min_value, max_value): return max(min_value, min(n, max_value))

class SizeCompareMode:
    def __init__(self, solar_system, screen_w, screen_h):
        self.solar_system = solar_system
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.base_positions = []
        
        self._compute_layout()

    def _compute_layout(self):
        x  = 80
        cy = self.screen_h / 2

        for planet in self.solar_system.planets:
            r = self._radius_px(planet, zoom=1.0)

            if planet.name == "Sun":
                r = min(r, 90)          # cap at layout time using zoom=1.0

            x = x + r + 20             # padding before
            self.base_positions.append((x, cy, r))
            x = x + r + 20             # padding after

    def _radius_px(self, planet, zoom):
        ratio = planet.radius_km / EARTH_RADIUS_KM
        return max(2, int(ratio * BASE_EARTH_PX * zoom))

    def world_to_screen(self, wx, wy):
        sx = wx * self.zoom + self.offset_x
        sy = wy * self.zoom + self.offset_y
        return (sx, sy)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            factor = 1.1 if event.y == 1 else 0.9
        
        mx, my = pygame.mouse.get_pos()
        self.offset_x = mx - (mx - self.offset_x) * factor
        self.offset_y = my - (my - self.offset_y) * factor
        self.zoom = clamp(self.zoom * factor, 0.1, 10.0)

    def update_pan(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def reset(self):
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

    def get_hovered(self, mouse_pos):
        mx, my = mouse_pos
        for i, (bx, by, br) in enumerate(self.base_positions):
            (sx, sy) = self.world_to_screen(bx, by)
            r = br * self.zoom
            distance = math.sqrt((mx - sx) ** 2 + (my - sy) ** 2)
            if distance <= r:
                return i
        return None

    def draw(self, surface, fonts, selected_idx, show_labels):
        for i, (planet, (bx, by, br)) in enumerate(zip(self.solar_system.planets, self.base_positions)):
            sx, sy = self.world_to_screen(bx, by)
            r = max(2, int(br * self.zoom))

            if planet.name == "Sun" and self.zoom < 3:
                true_radius_px = self._radius_px(planet, self.zoom)
                r = min(true_radius_px, int(90 * self.zoom))
                note = f"(True scale: {true_radius_px}px)"
                note_surf = fonts[3].render(note, True, (150, 120, 50))
                note_x = int(sx) - note_surf.get_width() // 2
                note_y = int(sy) - r - 30
                surface.blit(note_surf, (note_x, note_y))

            if not is_on_screen((int(sx), int(sy)), r, self.screen_w, self.screen_h):
                continue

            is_selected = (i == selected_idx)      # ← define it before using it

            draw_planet(
                surface,
                planet,
                (int(sx), int(sy)),
                r,
                selected=is_selected,
                font=fonts[0] if show_labels else None,
                show_label=show_labels
            )

        earth_diameter_px = int(BASE_EARTH_PX * self.zoom * 2)
        bar_x = 20
        bar_y = self.screen_h - 40

        # Horizontal line
        pygame.draw.line(surface, (120, 140, 180), \
                        (bar_x, bar_y),
                        (bar_x + earth_diameter_px, bar_y),
                        2)
        
        # Left tick
        pygame.draw.line(surface, (120, 140, 180),
                        (bar_x, bar_y - 5),
                        (bar_x, bar_y + 5),
                        2)

        # Right tick
        pygame.draw.line(surface, (120, 140, 180),
                        (bar_x + earth_diameter_px, bar_y - 5),
                        (bar_x + earth_diameter_px, bar_y + 5),
                        2)

        # Label
        label_surf = fonts[3].render("= Earth diameter", True, (120, 140, 180))
        surface.blit(label_surf, (bar_x + earth_diameter_px + 8, bar_y - label_surf.get_height() // 2))

