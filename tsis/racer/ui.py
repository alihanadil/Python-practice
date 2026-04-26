import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (150, 150, 150)
DARK  = (40, 40, 40)

font_cache = {}

def get_font(size):
    if size not in font_cache:
        font_cache[size] = pygame.font.SysFont("Verdana", size)
    return font_cache[size]

def draw_button(screen, text, rect, hover=False):
    color = (80, 80, 80) if not hover else (120, 120, 120)
    pygame.draw.rect(screen, color, rect, border_radius=6)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=6)
    surf = get_font(20).render(text, True, WHITE)
    screen.blit(surf, surf.get_rect(center=rect.center))

def text_input_screen(screen, prompt):
    text = ""
    clock = pygame.time.Clock()
    W, H = screen.get_size()
    while True:
        screen.fill(BLACK)
        screen.blit(get_font(24).render(prompt, True, WHITE),
                    get_font(24).render(prompt, True, WHITE).get_rect(center=(W//2, H//2 - 40)))
        box = pygame.Rect(W//2 - 120, H//2, 240, 36)
        pygame.draw.rect(screen, DARK, box)
        pygame.draw.rect(screen, WHITE, box, 2)
        screen.blit(get_font(20).render(text + "|", True, (0,255,0)),
                    pygame.Rect(box.x+6, box.y+6, 0, 0))
        screen.blit(get_font(16).render("Press ENTER to confirm", True, GRAY),
                    get_font(16).render("Press ENTER to confirm", True, GRAY).get_rect(center=(W//2, H//2+60)))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and text.strip():
                    return text.strip()
                elif e.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 18 and e.unicode.isprintable():
                    text += e.unicode

def main_menu(screen):
    W, H = screen.get_size()
    buttons = {
        "Play":        pygame.Rect(W//2-90, 200, 180, 44),
        "Leaderboard": pygame.Rect(W//2-90, 260, 180, 44),
        "Settings":    pygame.Rect(W//2-90, 320, 180, 44),
        "Quit":        pygame.Rect(W//2-90, 380, 180, 44),
    }
    clock = pygame.time.Clock()
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BLACK)
        screen.blit(get_font(48).render("RACER", True, (255,200,0)),
                    get_font(48).render("RACER", True, (255,200,0)).get_rect(center=(W//2, 120)))
        for label, rect in buttons.items():
            draw_button(screen, label, rect, rect.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for label, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return label

def leaderboard_screen(screen):
    from persistence import load_leaderboard
    rows = load_leaderboard()
    W, H = screen.get_size()
    back = pygame.Rect(W//2-70, H-60, 140, 40)
    clock = pygame.time.Clock()
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BLACK)
        screen.blit(get_font(28).render("TOP 10", True, (255,200,0)),
                    get_font(28).render("TOP 10", True, (255,200,0)).get_rect(center=(W//2, 30)))
        if not rows:
            screen.blit(get_font(18).render("No scores yet", True, GRAY),
                        get_font(18).render("No scores yet", True, GRAY).get_rect(center=(W//2, H//2)))
        for i, entry in enumerate(rows):
            line = f"{i+1}. {entry['name']:<14} {entry['score']:<8} {entry['distance']}m"
            screen.blit(get_font(18).render(line, True, WHITE), (20, 70 + i*28))
        draw_button(screen, "Back", back, back.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if back.collidepoint(mx, my):
                    return

def settings_screen(screen):
    from persistence import load_settings, save_settings
    s = load_settings()
    W, H = screen.get_size()
    save_btn = pygame.Rect(W//2-80, H-70, 160, 40)
    clock = pygame.time.Clock()
    color_opts = [("Default",(255,255,255)), ("Red",(255,60,60)), ("Blue",(60,120,255)), ("Green",(60,220,60))]
    diff_opts = ["easy", "normal", "hard"]
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BLACK)
        screen.blit(get_font(28).render("SETTINGS", True, WHITE),
                    get_font(28).render("SETTINGS", True, WHITE).get_rect(center=(W//2, 36)))
        # sound toggle
        snd_btn = pygame.Rect(W//2-80, 100, 160, 36)
        draw_button(screen, f"Sound: {'ON' if s['sound'] else 'OFF'}", snd_btn, snd_btn.collidepoint(mx,my))
        # difficulty
        screen.blit(get_font(18).render("Difficulty:", True, GRAY), (20, 160))
        diff_rects = []
        for i, d in enumerate(diff_opts):
            r = pygame.Rect(20 + i*120, 185, 110, 32)
            diff_rects.append(r)
            pygame.draw.rect(screen, (80,80,80) if s["difficulty"]!=d else (0,160,0), r, border_radius=5)
            pygame.draw.rect(screen, WHITE, r, 1, border_radius=5)
            screen.blit(get_font(16).render(d, True, WHITE), get_font(16).render(d, True, WHITE).get_rect(center=r.center))
        # car color
        screen.blit(get_font(18).render("Car Color:", True, GRAY), (20, 240))
        color_rects = []
        for i, (name, rgb) in enumerate(color_opts):
            r = pygame.Rect(20 + i*90, 265, 82, 32)
            color_rects.append(r)
            pygame.draw.rect(screen, rgb, r, border_radius=5)
            if s["car_color"] == name:
                pygame.draw.rect(screen, WHITE, r, 3, border_radius=5)
        draw_button(screen, "Save & Back", save_btn, save_btn.collidepoint(mx,my))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if snd_btn.collidepoint(mx,my):
                    s["sound"] = not s["sound"]
                for i, r in enumerate(diff_rects):
                    if r.collidepoint(mx,my):
                        s["difficulty"] = diff_opts[i]
                for i, r in enumerate(color_rects):
                    if r.collidepoint(mx,my):
                        s["car_color"] = color_opts[i][0]
                if save_btn.collidepoint(mx,my):
                    save_settings(s)
                    return

def game_over_screen(screen, score, distance, coins):
    W, H = screen.get_size()
    retry_btn = pygame.Rect(W//2-100, 360, 180, 44)
    menu_btn  = pygame.Rect(W//2-100, 420, 180, 44)
    clock = pygame.time.Clock()
    while True:
        mx, my = pygame.mouse.get_pos()
        screen.fill(BLACK)
        screen.blit(get_font(48).render("GAME OVER", True, (255,0,0)),
                    get_font(48).render("GAME OVER", True, (255,0,0)).get_rect(center=(W//2, 160)))
        for i, line in enumerate([f"Score: {score}", f"Distance: {int(distance)}m", f"Coins: {coins}"]):
            surf = get_font(22).render(line, True, WHITE)
            screen.blit(surf, surf.get_rect(center=(W//2, 250 + i*38)))
        draw_button(screen, "Retry",     retry_btn, retry_btn.collidepoint(mx,my))
        draw_button(screen, "Main Menu", menu_btn,  menu_btn.collidepoint(mx,my))
        pygame.display.flip()
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if retry_btn.collidepoint(mx,my): return "retry"
                if menu_btn.collidepoint(mx,my):  return "menu"
