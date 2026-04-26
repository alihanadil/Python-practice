import pygame
import random
import time
from persistence import load_settings

#  constants 
WIDTH  = 400
HEIGHT = 600
FPS    = 60

# difficulty multipliers for spawn intervals (lower = harder)
DIFF_MULT = {"easy": 1.6, "normal": 1.0, "hard": 0.55}

#  color tints for car_color setting 
CAR_TINTS = {
    "Default": None,
    "Red":     (255, 60,  60),
    "Blue":    (60,  120, 255),
    "Green":   (60,  220, 60),
}

#  original sprites (unchanged) 

class Player(pygame.sprite.Sprite):
    def __init__(self, image, tint=None):
        super().__init__()
        self.image = image.copy()
        if tint:
            tint_surf = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surf.fill((*tint, 120))
            self.image.blit(tint_surf, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom   = HEIGHT
        self.speed  = 5
        self.shield = False   # set by Shield power-up

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left  < 0:     self.rect.left  = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect  = self.image.get_rect()
        self.speed = 10

    def generate_random_rect(self):
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.base_image = image
        self.size = random.randint(1, 3)
        self._apply_size()
        self.generate_random_rect()

    def _apply_size(self):
        w = int(30 * self.size * 0.5)
        self.image = pygame.transform.scale(self.base_image, (w, w))
        self.rect  = self.image.get_rect()

    def generate_random_rect(self):
        self.size = random.randint(1, 3)
        self._apply_size()
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.top  = random.randint(HEIGHT - 80, HEIGHT - 20)

# road obstacle (oil spill / pothole) 

class Obstacle(pygame.sprite.Sprite):
    # kinds: "oil" slows, "barrier" instant game-over (like enemy)
    KINDS = ["oil", "barrier"]

    def __init__(self):
        super().__init__()
        self.kind  = random.choice(self.KINDS)
        self.speed = 4
        w, h = (50, 20) if self.kind == "oil" else (40, 30)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.kind == "oil":
            pygame.draw.ellipse(self.image, (20, 20, 80, 200), (0, 0, w, h))
        else:
            pygame.draw.rect(self.image, (180, 30, 30), (0, 0, w, h))
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, w, h), 2)
        self.rect = self.image.get_rect()
        self._spawn()

    def _spawn(self):
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self._spawn()

# nitro strip (speed boost lane event) 

class NitroStrip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, 14), pygame.SRCALPHA)
        self.image.fill((255, 220, 0, 160))
        self.rect  = self.image.get_rect()
        self.rect.bottom = 0
        self.speed = 5

    def move(self):
        self.rect.move_ip(0, self.speed)

# collectible power-up sprite 

POWERUP_COLORS = {"nitro": (255, 160, 0), "shield": (80, 80, 255), "repair": (0, 200, 80)}

class PowerUp(pygame.sprite.Sprite):
    TIMEOUT = 7000  # ms before it disappears

    def __init__(self, kind):
        super().__init__()
        self.kind  = kind
        self.speed = 4
        self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.circle(self.image, POWERUP_COLORS[kind], (14, 14), 14)
        label = pygame.font.SysFont("Verdana", 11).render(kind[0].upper(), True, (0,0,0))
        self.image.blit(label, label.get_rect(center=(14, 14)))
        self.rect  = self.image.get_rect()
        self.rect.left   = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0
        self.spawned_at  = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, self.speed)

    def expired(self):
        return pygame.time.get_ticks() - self.spawned_at > self.TIMEOUT or self.rect.top > HEIGHT

#  HUD helper 

def draw_hud(screen, fontt, collected, distance, active_pu, pu_end):
    screen.blit(fontt.render(f"Score:{collected}  Dist:{int(distance)}m", True, "black"), (5, 5))
    if active_pu:
        remaining = max(0, (pu_end - pygame.time.get_ticks()) // 1000)
        label = f"{active_pu.upper()} {remaining}s" if remaining else active_pu.upper()
        screen.blit(fontt.render(label, True, POWERUP_COLORS[active_pu]), (5, 25))

#  main play function 

def play_game(screen, username):
    settings   = load_settings()
    diff_mult  = DIFF_MULT.get(settings.get("difficulty", "normal"), 1.0)
    tint       = CAR_TINTS.get(settings.get("car_color", "Default"))

    # load assets
    image_background = pygame.image.load('assets/AnimatedStreet.png')
    image_player     = pygame.image.load('assets/Player.png')
    image_enemy      = pygame.image.load('assets/Enemy.png')
    coin_image       = pygame.image.load('assets/dollar.png').convert_alpha()

    if settings.get("sound", True):
        pygame.mixer.music.load('assets/background.wav')
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
    sound_crash = pygame.mixer.Sound('assets/crash.wav')

    fontt = pygame.font.SysFont("Verdana", 20)

    # sprites
    player = Player(image_player, tint)
    enemy  = Enemy(image_enemy)
    coin   = Coin(coin_image)
    enemy.generate_random_rect()

    all_sprites   = pygame.sprite.Group(player, enemy, coin)
    enemy_sprites = pygame.sprite.Group(enemy)
    coin_sprites  = pygame.sprite.Group(coin)
    obstacle_sprites = pygame.sprite.Group()
    powerup_sprites  = pygame.sprite.Group()
    nitro_sprites    = pygame.sprite.Group()

    clock      = pygame.time.Clock()
    collected  = 0
    distance   = 0.0
    last_speedup = 0
    N = 5  # original speed-up interval

    # timers for new spawns
    last_obstacle = pygame.time.get_ticks()
    last_powerup  = pygame.time.get_ticks()
    last_nitro    = pygame.time.get_ticks()
    OBSTACLE_INTERVAL = int(3000 * diff_mult)
    POWERUP_INTERVAL  = int(8000 * diff_mult)
    NITRO_INTERVAL    = int(12000 * diff_mult)

    # active power-up state
    active_pu  = None   # "nitro" | "shield" | "repair" | None
    pu_end     = 0
    base_speed = player.speed
    oil_slow   = False
    oil_slow_end = 0

    bg_y = 0  # scrolling background offset

    running = True
    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); raise SystemExit

        #  spawn obstacles 
        if now - last_obstacle > OBSTACLE_INTERVAL:
            obs = Obstacle()
            # safe spawn: don't place on player x-range
            attempts = 0
            while abs(obs.rect.centerx - player.rect.centerx) < 40 and attempts < 10:
                obs._spawn(); attempts += 1
            obstacle_sprites.add(obs)
            all_sprites.add(obs)
            last_obstacle = now
            # scale difficulty
            OBSTACLE_INTERVAL = max(800, OBSTACLE_INTERVAL - 40)

        #  spawn power-up 
        if now - last_powerup > POWERUP_INTERVAL and len(powerup_sprites) == 0:
            kind = random.choice(["nitro", "shield", "repair"])
            pu = PowerUp(kind)
            powerup_sprites.add(pu)
            all_sprites.add(pu)
            last_powerup = now

        #  spawn nitro strip 
        if now - last_nitro > NITRO_INTERVAL:
            ns = NitroStrip()
            nitro_sprites.add(ns)
            all_sprites.add(ns)
            last_nitro = now

        #  expire power-ups that time out 
        for pu in list(powerup_sprites):
            if pu.expired():
                pu.kill()

        #  expire active power-up effect 
        if active_pu in ("nitro",) and now > pu_end:
            player.speed = base_speed
            active_pu = None
        if oil_slow and now > oil_slow_end:
            player.speed = base_speed if active_pu != "nitro" else base_speed + 4
            oil_slow = False

        #  move everything 
        player.move()
        enemy.move()
        for obs in obstacle_sprites: obs.move()
        for pu  in powerup_sprites:  pu.move()
        for ns  in list(nitro_sprites):
            ns.move()
            if ns.rect.top > HEIGHT:
                ns.kill()

        #  coin collision (original) 
        if pygame.sprite.spritecollideany(player, coin_sprites):
            collected += coin.size
            if collected // N > last_speedup:
                enemy.speed += 3
                last_speedup = collected // N
            coin.generate_random_rect()

        #  obstacle collision 
        hit_obs = pygame.sprite.spritecollideany(player, obstacle_sprites)
        if hit_obs:
            if hit_obs.kind == "barrier":
                if player.shield:
                    player.shield = False
                    active_pu = None
                    hit_obs.kill()
                else:
                    running = False
            elif hit_obs.kind == "oil":
                if not oil_slow:
                    oil_slow = True
                    oil_slow_end = now + 2000
                    player.speed = max(2, player.speed - 2)
                hit_obs.kill()

        #  enemy collision (original logic + shield) 
        if pygame.sprite.spritecollideany(player, enemy_sprites):
            if player.shield:
                player.shield = False
                active_pu = None
                enemy.generate_random_rect()
            else:
                running = False

        #  power-up pickup 
        hit_pu = pygame.sprite.spritecollideany(player, powerup_sprites)
        if hit_pu:
            if hit_pu.kind == "nitro":
                active_pu  = "nitro"
                pu_end     = now + 4000
                player.speed = base_speed + 4
            elif hit_pu.kind == "shield":
                active_pu     = "shield"
                player.shield = True
            elif hit_pu.kind == "repair":
                # clears one obstacle from field
                for obs in list(obstacle_sprites)[:1]:
                    obs.kill()
            hit_pu.kill()

        #  nitro strip (road event) 
        if pygame.sprite.spritecollideany(player, nitro_strips := nitro_sprites):
            if active_pu != "nitro":
                player.speed = base_speed + 3
                pygame.time.set_timer(pygame.USEREVENT + 1, 1500, 1)  # one-shot reset

        for e in pygame.event.get(pygame.USEREVENT + 1):
            if active_pu != "nitro":
                player.speed = base_speed

        #  distance 
        distance += player.speed * 0.05

        #  draw 
        bg_y = (bg_y + 5) % HEIGHT
        screen.blit(image_background, (0, bg_y - HEIGHT))
        screen.blit(image_background, (0, bg_y))

        for ns in nitro_sprites:
            screen.blit(ns.image, ns.rect)
        for obs in obstacle_sprites:
            screen.blit(obs.image, obs.rect)
        for pu in powerup_sprites:
            screen.blit(pu.image, pu.rect)
        screen.blit(coin.image, coin.rect)
        screen.blit(enemy.image, enemy.rect)
        screen.blit(player.image, player.rect)

        draw_hud(screen, fontt, collected, distance, active_pu, pu_end)
        pygame.display.flip()
        clock.tick(FPS)

        if not running:
            if settings.get("sound", True):
                sound_crash.play()
            pygame.mixer.music.stop()
            time.sleep(0.5)

    return collected, distance
