import pygame, math


def draw_starfield(surface,stars):
    for (x, y, r, brightness) in stars:
        pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), r)

_glow_cache = {}
def draw_glow(surface, color, pos, radius, intensity=80):
    glow_radius = min(radius, 150)
    key = (glow_radius, color[0], color[1], color[2], intensity)

    if key not in _glow_cache:
        glow_surf = pygame.Surface((radius * 6, radius * 6), pygame.SRCALPHA)
        glow_surf = glow_surf.convert_alpha()

        for i in range(3, 0, -1):
            alpha = int(intensity * (i / 3) ** 2)
            r = int(radius * (1 + i * 0.35))
            pygame.draw.circle(
                glow_surf,
                (color[0], color[1], color[2], alpha),
                (glow_radius * 3, glow_radius * 3),   # center of glow surface
                r
            )
        _glow_cache[key] = glow_surf

    cached = _glow_cache[key]
    surface.blit(cached, (pos[0] - radius * 3, pos[1] - radius * 3))

def draw_planet(surface, planet, pos, radius, selected=False, font=None, show_label=True):
    # Glow
    intensity = 120 if planet.name == "Sun" else 50
    draw_glow(surface, planet.glow_color, pos, radius, intensity=intensity)

    # Planet body
    pygame.draw.circle(surface, planet.color, pos, radius)

    # Highlight
    highlight_pos = (pos[0] - radius // 3, pos[1] - radius // 3)
    highlight_radius = max(2, radius // 4)
    highlight_color = (
        min(255, planet.color[0] + 80),
        min(255, planet.color[1] + 80),
        min(255, planet.color[2] + 80),
    )
    pygame.draw.circle(surface, highlight_color, highlight_pos, highlight_radius)

    # Saturn rings
    if planet.name == "Saturn":
        ring_surf = pygame.Surface((radius * 6, radius * 3), pygame.SRCALPHA)
        cx = radius * 3
        cy = radius * 3 // 2
        for i, stroke in enumerate([4, 3, 2]):
            ring_rx = int(radius * (1.8 + i * 0.25))
            ring_ry = int(radius * 0.45)
            alpha = 160 - i * 30
            pygame.draw.ellipse(
                ring_surf,
                (210, 195, 140, alpha),
                (cx - ring_rx, cy - ring_ry, ring_rx * 2, ring_ry * 2),
                stroke
            )
        surface.blit(ring_surf, (pos[0] - radius * 3, pos[1] - radius * 3 // 2))
        # Redraw planet on top so it overlaps inner rings
        pygame.draw.circle(surface, planet.color, pos, radius)

    # Selection ring
    if selected:
        pygame.draw.circle(surface, (255, 255, 255), pos, radius + 4, 2)

    # Label
    if show_label and font and radius >= 3:
        label = font.render(planet.name, True, (220, 220, 220))
        label_x = pos[0] - label.get_width() // 2
        label_y = pos[1] + radius + 6
        surface.blit(label, (label_x, label_y))

def draw_info_panel(surface, planet, font_large, font_small, screen_w, screen_h):
    panel_w, panel_h = 300, 175
    panel_x = screen_w - panel_w - 20
    panel_y = screen_h - panel_h - 20

    panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, (10, 15, 30, 210), (0, 0, panel_w, panel_h), border_radius=12)
    pygame.draw.rect(panel_surf, (80, 120, 200, 100), (0, 0, panel_w, panel_h), width=1, border_radius=12)
    surface.blit(panel_surf, (panel_x, panel_y))

    name_surf = font_large.render(planet.name, True, planet.color)
    surface.blit(name_surf, (panel_x + 16, panel_y + 14))

    lines = [
        f"Radius:   {planet.radius_km:,} km",
        f"Distance: {planet.distance_au} AU",
        f"Moons:    {planet.get_moon_count()}",
        f"Mass:     {planet.mass_kg:.2e} kg",
        "",
        planet.description
    ]

    for i, line in enumerate(lines):
        text_surf = font_small.render(line, True, (180, 200, 230))
        surface.blit(text_surf, (panel_x + 16, panel_y + 48 + i * 18))

def draw_controls_hint(surface, font, screen_w):
    hints = [
        "Scroll: zoom  |  Drag: pan  |  Click planet: info",
        "1: Size Compare  2: Orrery  R: Reset  L: Labels  Q: Quit"
    ]
    for i, hint in enumerate(hints):
        text_surf = font.render(hint, True, (100, 120, 160))
        x = screen_w // 2 - text_surf.get_width() // 2
        surface.blit(text_surf, (x, 10 + i * 18))

def is_on_screen(pos, radius, screen_w, screen_h):
    x, y = pos
    return (
        x + radius > 0 and
        x - radius < screen_w and
        y + radius > 0 and
        y - radius < screen_h
    )