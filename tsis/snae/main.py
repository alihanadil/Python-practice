import pygame
import time
import random
from color_palette import *
from config import *
from game import (
    Snake, Food, PowerUp, Obstacle,
    draw_grid, draw_hud,
    generate_obstacles, load_settings, save_settings
)
import db

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS4")
font       = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 28)
font_big   = pygame.font.SysFont(None, 54)
clock = pygame.time.Clock()

# ── Try to init DB (silently fails if no Postgres available) ──────────────────
DB_OK = db.init_db()

# ── Shared helpers 

def draw_button(text, rect, hover=False):
    color = (80, 80, 80) if not hover else (120, 120, 120)
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, colorWHITE, rect, 2, border_radius=8)
    surf = font.render(text, True, colorWHITE)
    screen.blit(surf, surf.get_rect(center=rect.center))

def text_input_screen(prompt):
    """Simple text input screen. Returns the entered string."""
    text = ""
    while True:
        screen.fill(colorBLACK)
        title = font_big.render("SNAKE", True, colorGREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        p_surf = font.render(prompt, True, colorWHITE)
        screen.blit(p_surf, p_surf.get_rect(center=(WIDTH // 2, 240)))
        box = pygame.Rect(WIDTH // 2 - 150, 280, 300, 44)
        pygame.draw.rect(screen, (40, 40, 40), box)
        pygame.draw.rect(screen, colorWHITE, box, 2)
        t_surf = font.render(text + "|", True, colorGREEN)
        screen.blit(t_surf, t_surf.get_rect(center=box.center))
        hint = font_small.render("Press ENTER to confirm", True, colorGRAY)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 360)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and text.strip():
                    return text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 20 and event.unicode.isprintable():
                    text += event.unicode

# ── Main Menu ────

def main_menu():
    buttons = {
        "Play":        pygame.Rect(WIDTH // 2 - 100, 200, 200, 50),
        "Leaderboard": pygame.Rect(WIDTH // 2 - 100, 270, 200, 50),
        "Settings":    pygame.Rect(WIDTH // 2 - 100, 340, 200, 50),
        "Quit":        pygame.Rect(WIDTH // 2 - 100, 410, 200, 50),
    }
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(colorBLACK)
        title = font_big.render("SNAKE", True, colorGREEN)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        for label, rect in buttons.items():
            draw_button(label, rect, hover=rect.collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for label, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return label

# ── Leaderboard Screen ────────────────────────────────────────────────────────

def leaderboard_screen():
    rows = db.get_top10() if DB_OK else []
    back_btn = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 60, 160, 44)
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(colorBLACK)
        title = font.render("TOP 10 LEADERBOARD", True, colorYELLOW)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 30)))
        if not rows:
            msg = font_small.render("No scores yet (DB unavailable or empty)", True, colorGRAY)
            screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        else:
            header = font_small.render(f"{'#':<4} {'Name':<16} {'Score':<8} {'Lv':<5} {'Date'}", True, colorGRAY)
            screen.blit(header, (20, 65))
            pygame.draw.line(screen, colorGRAY, (20, 88), (WIDTH - 20, 88))
            for rank, username, score, level, date in rows:
                color = colorYELLOW if rank == 1 else colorWHITE
                line = font_small.render(f"{rank:<4} {username:<16} {score:<8} {level:<5} {date}", True, color)
                screen.blit(line, (20, 95 + (rank - 1) * 26))
        draw_button("Back", back_btn, hover=back_btn.collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.collidepoint(mx, my):
                    return

# ── Settings Screen 

COLOR_OPTIONS = [
    ("Green",  [0, 255, 0]),
    ("Blue",   [0, 0, 255]),
    ("Yellow", [255, 255, 0]),
    ("White",  [255, 255, 255]),
    ("Orange", [255, 165, 0]),
]

def settings_screen():
    settings = load_settings()
    save_btn = pygame.Rect(WIDTH // 2 - 90, HEIGHT - 70, 180, 44)

    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(colorBLACK)
        title = font.render("SETTINGS", True, colorWHITE)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 40)))

        # Grid toggle
        grid_btn = pygame.Rect(WIDTH // 2 - 80, 110, 160, 40)
        grid_label = "Grid: ON" if settings["grid"] else "Grid: OFF"
        draw_button(grid_label, grid_btn, hover=grid_btn.collidepoint(mx, my))

        # Sound toggle
        snd_btn = pygame.Rect(WIDTH // 2 - 80, 170, 160, 40)
        snd_label = "Sound: ON" if settings["sound"] else "Sound: OFF"
        draw_button(snd_label, snd_btn, hover=snd_btn.collidepoint(mx, my))

        # Snake color picker
        clr_lbl = font_small.render("Snake Color:", True, colorWHITE)
        screen.blit(clr_lbl, (40, 240))
        color_rects = []
        for idx, (name, rgb) in enumerate(COLOR_OPTIONS):
            r = pygame.Rect(40 + idx * 108, 270, 100, 36)
            color_rects.append(r)
            pygame.draw.rect(screen, tuple(rgb), r, border_radius=6)
            if settings["snake_color"] == rgb:
                pygame.draw.rect(screen, colorWHITE, r, 3, border_radius=6)
            nm = font_small.render(name, True, colorBLACK)
            screen.blit(nm, nm.get_rect(center=r.center))

        draw_button("Save & Back", save_btn, hover=save_btn.collidepoint(mx, my))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if grid_btn.collidepoint(mx, my):
                    settings["grid"] = not settings["grid"]
                elif snd_btn.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
                elif save_btn.collidepoint(mx, my):
                    save_settings(settings)
                    return
                for idx, r in enumerate(color_rects):
                    if r.collidepoint(mx, my):
                        settings["snake_color"] = COLOR_OPTIONS[idx][1]

# ── Game Over Screen ──────────────────────────────────────────────────────────

def game_over_screen(score, level, personal_best):
    retry_btn   = pygame.Rect(WIDTH // 2 - 110, 380, 200, 50)
    menu_btn    = pygame.Rect(WIDTH // 2 - 110, 450, 200, 50)
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(colorBLACK)
        go_surf = font_big.render("GAME OVER", True, colorRED)
        screen.blit(go_surf, go_surf.get_rect(center=(WIDTH // 2, 160)))
        for i, text in enumerate([
            f"Score: {score}",
            f"Level: {level}",
            f"Personal Best: {personal_best}",
        ]):
            s = font.render(text, True, colorWHITE)
            screen.blit(s, s.get_rect(center=(WIDTH // 2, 250 + i * 40)))
        draw_button("Retry",     retry_btn, hover=retry_btn.collidepoint(mx, my))
        draw_button("Main Menu", menu_btn,  hover=menu_btn.collidepoint(mx, my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_btn.collidepoint(mx, my):
                    return "retry"
                if menu_btn.collidepoint(mx, my):
                    return "menu"

# ── Main Game Loop ────────────────────────────────────────────────────────────

def play_game(username):
    settings = load_settings()
    personal_best = db.get_personal_best(username) if DB_OK else 0

    snake    = Snake(color=settings["snake_color"])
    food     = Food()
    obstacles = []
    powerup  = None
    last_powerup_spawn = pygame.time.get_ticks()
    POWERUP_SPAWN_INTERVAL = 10000  # try to spawn every 10 s

    food.generate_random_pos(snake.body, obstacles)
    current_time = pygame.time.get_ticks()
    last_level = snake.level

    running = True
    while running:
        now = pygame.time.get_ticks()

        # ── Level-up: add obstacles ─────────────────────────────────────────
        if snake.level != last_level:
            last_level = snake.level
            if snake.level >= OBSTACLE_START_LEVEL:
                obstacles = generate_obstacles(snake.level, snake.body)
                food.generate_random_pos(snake.body, obstacles)

        # ── Spawn power-up if none active ───────────────────────────────────
        if powerup is None and now - last_powerup_spawn > POWERUP_SPAWN_INTERVAL:
            powerup = PowerUp(snake.body, obstacles)
            last_powerup_spawn = now

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1;  snake.dy = 0
                elif event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1; snake.dy = 0
                elif event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0;  snake.dy = 1
                elif event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0;  snake.dy = -1

        # ── Update ──────────────────────────────────────────────────────────
        snake.move()
        snake.check_self_collision()
        snake.check_collision(food, obstacles)

        # check obstacle collision
        for obs in obstacles:
            if snake.body[0].x == obs.x and snake.body[0].y == obs.y:
                if snake.shield_active:
                    snake.shield_active = False
                else:
                    snake.alive = False

        # food timer (original logic)
        if abs(now - food.cooldown_start) > COOLDOWN_TIME:
            food.generate_random_pos(snake.body, obstacles)
            current_time = now

        # power-up pickup
        if powerup:
            head = snake.body[0]
            if head.x == powerup.pos.x and head.y == powerup.pos.y:
                powerup.apply(snake)
                powerup = None
                last_powerup_spawn = now
            elif powerup.is_expired():
                powerup = None
                last_powerup_spawn = now

        # ── Draw ────────────────────────────────────────────────────────────
        screen.fill(colorBLACK)
        if settings["grid"]:
            draw_grid(screen)
        for obs in obstacles:
            obs.draw(screen)
        food.draw(screen)
        if powerup:
            powerup.draw(screen)
        snake.draw(screen)
        draw_hud(screen, font, snake, personal_best, powerup)
        pygame.display.flip()

        clock.tick(snake.get_speed_fps())

        # ── Game Over check ─────────────────────────────────────────────────
        if not snake.alive:
            if DB_OK:
                db.save_session(username, snake.score, snake.level)
                personal_best = max(personal_best, snake.score)
            return snake.score, snake.level, personal_best

    return snake.score, snake.level, personal_best

# ── Entry Point ──

def main():
    username = text_input_screen("Enter your username:")
    while True:
        choice = main_menu()
        if choice == "Play":
            while True:
                score, level, pb = play_game(username)
                action = game_over_screen(score, level, pb)
                if action == "menu":
                    break
                # action == "retry" → loop back
        elif choice == "Leaderboard":
            leaderboard_screen()
        elif choice == "Settings":
            settings_screen()
        elif choice == "Quit":
            break
    pygame.quit()

if __name__ == "__main__":
    main()
