import pygame

BASE_EARTH_PX = 30

def clamp(n, min_value, max_value): return max(min_value, min(n, max_value))

def SizeCompareMode():
    def __init__(self, solar_system, screen_w, screen_h):
        self.solar_system = solar_system
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.base_positions = []

        self._compute_layout()

    def compute_layout(self):
        x = 80
        cy = self.screen_h / 2

        for planet in self.solar_system.planets:
            r = self._radius_px(planet, self.zoom)
        
            if planet.name == "Sun":
                display_r = min(r, 90)
            else: 
                display_r = r

        
            x = x + display_r + 20 #padding before planet
            self.base_positions.append((x, cy, display_r))
            x = x + display_r + 20 #padding after planet

    def _radius_px(self, planet, zoom):
        ratio = planet.radius_km / self.solar_system.planets["earth"].radius_km
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
        for i, (bx, by, br) in enumerate(self.base_positions):
            (sx, sy) = world_to_screen(bx, by)
            r = br * self.zoom

            if (max(mouse_pos[0], sx) - min(mouse_pos[0], sx) <= r or \
                max(mouse_pos[1], sy) - min((mouse_pos[1], sy)) <= r):
                return i
        return None

    def draw(self, surface, fonts, selected_idx, show_labels):
        for i, (planet, base_pos) in enumerate(zip(self.solar_system.planets, self.base_positions)):
            (sx, sy) = world_to_screen(base_pos.x, base_pos.y)
            r = max(2, int(base_pos.radius * self.zoom))
            is_selected = (i == selected_idx)

            if planet.name == "Sun" and zoom < 3:
                true_radius_px = self._radius_px(planet, self.zoom)
                note = f"(True scale: {true_radius_px}px)"
                note_surf = fonts[3].render(note, True, (150, 120, 50))
                note_x = sx - note_surf.get_width() // 2
                note_y = sy - r - 30
                surface.blit(note_surf, (note_x, note_y))
            
            self.draw(surface, planet, (sx, sy), r, \
                      is_selected, fonts.label if show_labels else None, \
                        show_labels)

        earth_diameter_px = int(BASE_EARTH_PX * self.zoom * 2)
        bar_x = 20
        bar_y = self.screen_h - 40

        # Horizontal line
        pygame.draw.line(surface, (120, 140, 180), \
                         (bar_x, bar_y), \
                            (bar_x + earth_diameter_px, bar_y), \
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

