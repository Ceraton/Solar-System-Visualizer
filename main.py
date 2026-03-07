from pathlib import Path
import pygame, sys, math, random
from src.bodies import SolarSystem
from visuals.renderer import draw_starfield, draw_info_panel, draw_controls_hint
from visuals.size_compare import SizeCompareMode
from visuals.orrery import OrreryMode
from visuals.timeline import Timeline
import os

WIDTH, HEIGHT = 1280, 800
FPS           = 60
BG_COLOR      = (4, 6, 18)
PLANETS_PATH  = Path('data/planets.json')
MOONS_PATH    = Path('data/moons.json')

os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

def generate_stars(n=200, w=WIDTH, h=HEIGHT):
    stars = []
    for _ in range(n):
        x          = random.randint(0, w)
        y          = random.randint(0, h)
        r          = random.choices([1, 1, 1, 2], weights=[60, 20, 15, 5])[0]
        brightness = random.randint(100, 255)
        stars.append((x, y, r, brightness))
    return stars

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Solar System Visualizer")
    clock = pygame.time.Clock()

    font_label = pygame.font.SysFont(None, 18)
    font_large = pygame.font.SysFont(None, 28)
    font_small = pygame.font.SysFont(None, 20)
    font_hint  = pygame.font.SysFont(None, 16)
    fonts = (font_label, font_large, font_small, font_hint)

    solar_system = SolarSystem(PLANETS_PATH, MOONS_PATH)
    stars        = generate_stars()
    timeline     = Timeline()

    size_mode   = SizeCompareMode(solar_system, WIDTH, HEIGHT)
    orrery_mode = OrreryMode(solar_system, WIDTH, HEIGHT, timeline)
    active_mode = size_mode

    selected_idx = None
    show_labels  = True
    dragging     = False
    drag_start   = (0, 0)
    needs_redraw = True

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    active_mode = size_mode
                    needs_redraw = True
                if event.key == pygame.K_2:
                    active_mode = orrery_mode
                    needs_redraw = True
                if event.key == pygame.K_r:
                    active_mode.reset()
                    selected_idx = None
                    needs_redraw = True
                if event.key == pygame.K_l:
                    show_labels = not show_labels
                    needs_redraw = True
                if event.key == pygame.K_SPACE:
                    if timeline.playing:
                        timeline.pause()
                    else:
                        timeline.play()
                    needs_redraw = True
                if event.key == pygame.K_EQUALS:
                    timeline.speed *= 2
                    needs_redraw = True
                if event.key == pygame.K_MINUS:
                    timeline.speed /= 2
                    needs_redraw = True

            if event.type == pygame.MOUSEWHEEL:
                active_mode.handle_event(event)
                needs_redraw = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging     = True
                    drag_start   = pygame.mouse.get_pos()
                    hovered      = active_mode.get_hovered(drag_start)
                    selected_idx = hovered if hovered is not None else None
                    needs_redraw = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            if event.type == pygame.MOUSEMOTION:
                if dragging:
                    mx, my     = pygame.mouse.get_pos()
                    dx         = mx - drag_start[0]
                    dy         = my - drag_start[1]
                    active_mode.update_pan(dx, dy)
                    drag_start = (mx, my)
                    needs_redraw = True

        if active_mode is orrery_mode:
            orrery_mode.tick(dt)
            needs_redraw = True

        if needs_redraw:
            screen.fill(BG_COLOR)
            draw_starfield(screen, stars)
            active_mode.draw(screen, fonts, selected_idx, show_labels)
            if selected_idx is not None:
                planet = solar_system.planets[selected_idx]
                draw_info_panel(screen, planet, font_large, font_small, WIDTH, HEIGHT)
            draw_controls_hint(screen, font_hint, WIDTH)
            fps_surf = font_hint.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 255))
            screen.blit(fps_surf, (10, 10))
            pygame.display.flip()
            pygame.display.update()    # ← add this
            needs_redraw = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()