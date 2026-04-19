import pygame
import random
import time

pygame.init() # initializes all the pygame sub-modules

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # creating a game window
# set_mode() takes a tuple as an argument

image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')
coin_image = pygame.image.load('resources/dollar.png').convert_alpha()

collected = 0

pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('resources/crash.wav')

font = pygame.font.SysFont("Verdana", 60)
fontt = pygame.font.SysFont("Verdana", 20)

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))
score = fontt.render(f"Score: {collected}", True, "black")
score_rect = score.get_rect(center = (325, 10)) 

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10
        # or
        # self.rect.midbottom = (WIDTH // 2, HEIGHT)

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_image
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  
        self.generate_random_rect()       

    def generate_random_rect(self):
        # random x, but keep it within screen width
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        # fixed y near the bottom where the player moves
        self.rect.top = HEIGHT - 80

running = True

# this object allows us to set the FPS
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)
while running: # game loop
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            running = False
    score = fontt.render(f"Score: {collected}", True, "black")
    player.move()
    screen.blit(image_background, (0, 0))
    screen.blit(score, score_rect)
    for entity in all_sprites:
        if not isinstance(entity, Coin):
            entity.move()
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, coin_sprites):
        collected +=1
        coin.generate_random_rect()

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)

        running = False
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()

        time.sleep(3)
        
    
    pygame.display.flip() # updates the screen
    clock.tick(FPS) # sets the FPS

pygame.quit()