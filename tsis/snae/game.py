import pygame
import random
import json
from color_palette import *
from config import *

# ── Settings helpers ─────────────

def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except Exception:
        return {"snake_color": [0, 255, 0], "grid": True, "sound": False}

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

# ── Grid drawing (original, unchanged) 

def draw_grid(screen):
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            if j != 0:
                pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)

# ── Point (original, unchanged) ──

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x}, {self.y}"

# ── Snake (original + shield/color support) ───────────────

class Snake:
    def __init__(self, color=None):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.score = 0
        self.level = 1
        self.alive = True
        self.color = tuple(color) if color else colorGREEN
        # power-up state
        self.shield_active = False
        self.speed_boost_end = 0    # ms timestamp when effect ends (0 = inactive)
        self.slow_motion_end = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        hit_wall = (
            self.body[0].x > WIDTH // CELL - 1 or
            self.body[0].x < 0 or
            self.body[0].y > HEIGHT // CELL - 1 or
            self.body[0].y == 0
        )
        if hit_wall:
            if self.shield_active:
                # wrap back inside arena instead of dying
                self.body[0].x = max(0, min(self.body[0].x, WIDTH // CELL - 1))
                self.body[0].y = max(1, min(self.body[0].y, HEIGHT // CELL - 1))
                self.shield_active = False
            else:
                self.alive = False

    def check_self_collision(self):
        head = self.body[0]
        for seg in self.body[1:]:
            if head.x == seg.x and head.y == seg.y:
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.alive = False
                return

    def draw(self, screen):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, self.color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food, obstacles):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            if food.food_type == "poison":
                # shorten by 2
                for _ in range(2):
                    if len(self.body) > 1:
                        self.body.pop()
                if len(self.body) <= 1:
                    self.alive = False
            else:
                self.score += (food.n + 1)
                self.body.append(Point(head.x, head.y))
                self.level = 1 + self.score // 3
            food.generate_random_pos(self.body, obstacles)

    def get_speed_fps(self):
        now = pygame.time.get_ticks()
        base = FPS_BASE + self.level
        if self.speed_boost_end and now < self.speed_boost_end:
            return base + 5
        if self.slow_motion_end and now < self.slow_motion_end:
            return max(2, base - 3)
        return base

# ── Food (original + poison type) 

class Food:
    NORMAL_COLORS = [colorGREEN, colorBLUE, colorRED]
    POISON_COLOR = (139, 0, 0)   # dark red

    def __init__(self):
        self.n = random.randint(0, 2)
        self.pos = Point(9, 9)
        self.cooldown_start = pygame.time.get_ticks()
        self.food_type = "normal"

    def _pick_type(self):
        self.food_type = "poison" if random.random() < 0.2 else "normal"
        self.n = random.randint(0, 2)

    def draw(self, screen):
        color = self.POISON_COLOR if self.food_type == "poison" else self.NORMAL_COLORS[self.n]
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake_body, obstacles=None):
        self._pick_type()
        self.cooldown_start = pygame.time.get_ticks()
        blocked = {(s.x, s.y) for s in snake_body}
        if obstacles:
            blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(1, HEIGHT // CELL - 1)
            if (x, y) not in blocked:
                self.pos.x = x
                self.pos.y = y
                break

# ── Power-ups 

POWERUP_TYPES = ["speed", "slow", "shield"]
POWERUP_COLORS = {
    "speed":  (255, 165, 0),   # orange
    "slow":   (0, 200, 255),   # cyan
    "shield": (180, 0, 255),   # purple
}

class PowerUp:
    def __init__(self, snake_body, obstacles=None):
        self.kind = random.choice(POWERUP_TYPES)
        self.spawned_at = pygame.time.get_ticks()
        blocked = {(s.x, s.y) for s in snake_body}
        if obstacles:
            blocked |= {(o.x, o.y) for o in obstacles}
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(1, HEIGHT // CELL - 1)
            if (x, y) not in blocked:
                self.pos = Point(x, y)
                break

    def draw(self, screen):
        color = POWERUP_COLORS[self.kind]
        rect = (self.pos.x * CELL + 4, self.pos.y * CELL + 4, CELL - 8, CELL - 8)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, colorWHITE, rect, 2)

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawned_at > POWERUP_FIELD_TIME

    def apply(self, snake):
        now = pygame.time.get_ticks()
        if self.kind == "speed":
            snake.speed_boost_end = now + POWERUP_DURATION
        elif self.kind == "slow":
            snake.slow_motion_end = now + POWERUP_DURATION
        elif self.kind == "shield":
            snake.shield_active = True

# ── Obstacles 

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, colorGRAY, (self.x * CELL, self.y * CELL, CELL, CELL))
        pygame.draw.rect(screen, colorWHITE, (self.x * CELL, self.y * CELL, CELL, CELL), 2)

def generate_obstacles(level, snake_body, count=None):
    if count is None:
        count = min(3 + level - OBSTACLE_START_LEVEL, 12)
    blocked = {(s.x, s.y) for s in snake_body}
    # keep a safe zone around snake head
    head = snake_body[0]
    safe = {(head.x + dx, head.y + dy) for dx in range(-3, 4) for dy in range(-3, 4)}
    obstacles = []
    attempts = 0
    while len(obstacles) < count and attempts < 500:
        attempts += 1
        x = random.randint(0, WIDTH // CELL - 1)
        y = random.randint(1, HEIGHT // CELL - 1)
        if (x, y) not in blocked and (x, y) not in safe:
            obstacles.append(Obstacle(x, y))
            blocked.add((x, y))
    return obstacles

# ── HUD ──────

def draw_hud(screen, font, snake, personal_best, powerup=None):
    now = pygame.time.get_ticks()
    sc   = font.render(f'Score:{snake.score}', True, colorWHITE)
    lv   = font.render(f'Lv:{snake.level}',   True, colorWHITE)
    pb   = font.render(f'Best:{personal_best}', True, colorYELLOW)
    screen.blit(sc, (2, 2))
    screen.blit(lv, (140, 2))
    screen.blit(pb, (240, 2))
    # active power-up label
    labels = []
    if snake.speed_boost_end and now < snake.speed_boost_end:
        remaining = (snake.speed_boost_end - now) // 1000 + 1
        labels.append(f"SPEED {remaining}s")
    if snake.slow_motion_end and now < snake.slow_motion_end:
        remaining = (snake.slow_motion_end - now) // 1000 + 1
        labels.append(f"SLOW {remaining}s")
    if snake.shield_active:
        labels.append("SHIELD")
    if labels:
        pu_surf = font.render(" | ".join(labels), True, (255, 165, 0))
        screen.blit(pu_surf, (400, 2))
